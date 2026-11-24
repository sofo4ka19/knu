import os

import psycopg2
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, TEXT
from datetime import datetime
from tqdm import tqdm
import time

# Конфігурація PostgreSQL
load_dotenv()
PG_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Конфігурація MongoDB
MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB = os.getenv('MONGO_DB')

# Підключення
pg_conn = psycopg2.connect(**PG_CONFIG)
pg_cur = pg_conn.cursor()

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB]
products_collection = mongo_db['products']


def migrate_products():

    print("\n" + "=" * 60)
    print("🔄 МІГРАЦІЯ POSTGRESQL → MONGODB")
    print("=" * 60)

    start_time = time.time()

    # Очищаємо колекцію перед міграцією
    products_collection.drop()
    print("🗑️  Очищено колекцію products")

    # Отримуємо всі продукти з JOIN'ами
    query = """
            SELECT p.ProductID,
                   p.Name,
                   p.Description,
                   p.is_deleted,
                   p.updated_at,

                   -- Відділ
                   d.DepartmentID,
                   d.DeptName,

                   -- Постачальник
                   s.SupplierID,
                   s.Name       as SupplierName,
                   s.ContactPerson,
                   s.Phone,

                   -- Виробник
                   m.ManufacturerID,
                   m.Name       as ManufacturerName,
                   m.Country,

                   -- Інвентар
                   i.Quantity,
                   i.ShelfLocation,
                   i.updated_at as InventoryUpdatedAt

            FROM Products p
                     LEFT JOIN Departments d ON p.DepartmentID = d.DepartmentID
                     LEFT JOIN Suppliers s ON p.SupplierID = s.SupplierID
                     LEFT JOIN Manufacturers m ON p.ManufacturerID = m.ManufacturerID
                     LEFT JOIN Inventory i ON p.ProductID = i.ProductID
            WHERE p.is_deleted = FALSE
            ORDER BY p.ProductID
            """

    pg_cur.execute(query)
    products = pg_cur.fetchall()

    print(f"📦 Знайдено {len(products):,} продуктів для міграції")

    # Підготовка документів для batch insert
    batch_size = 1000
    documents = []

    for product in tqdm(products, desc="Міграція"):
        product_id = product[0]

        # Отримуємо історію цін для цього продукту
        pg_cur.execute("""
                       SELECT Price, EffectiveDate
                       FROM PricingHistory
                       WHERE ProductID = %s
                       ORDER BY EffectiveDate DESC
                       """, (product_id,))

        price_history = [
            {
                'price': float(row[0]),
                'effectiveDate': row[1].isoformat()
            }
            for row in pg_cur.fetchall()
        ]

        # Актуальна ціна (остання в історії)
        current_price = price_history[0]['price'] if price_history else 0

        # Отримуємо категорії
        pg_cur.execute("""
                       SELECT c.CategoryID, c.CategoryName
                       FROM ProductCategories pc
                                JOIN Categories c ON pc.CategoryID = c.CategoryID
                       WHERE pc.ProductID = %s
                       """, (product_id,))

        categories = [
            {
                'id': row[0],
                'name': row[1]
            }
            for row in pg_cur.fetchall()
        ]

        # Формуємо MongoDB документ
        document = {
            '_id': product_id,  # Використовуємо оригінальний ID
            'name': product[1],
            'description': product[2],
            'isDeleted': product[3],
            'updatedAt': product[4].isoformat() if product[4] else None,

            # Вкладені об'єкти (денормалізація!)
            'department': {
                'id': product[5],
                'name': product[6]
            } if product[5] else None,

            'supplier': {
                'id': product[7],
                'name': product[8],
                'contactPerson': product[9],
                'phone': product[10]
            } if product[7] else None,

            'manufacturer': {
                'id': product[11],
                'name': product[12],
                'country': product[13]
            } if product[11] else None,

            'inventory': {
                'quantity': product[14] if product[14] is not None else 0,
                'shelfLocation': product[15],
                'updatedAt': product[16].isoformat() if product[16] else None,
                'inStock': (product[14] or 0) > 0
            },

            # Історія цін як масив
            'priceHistory': price_history,
            'currentPrice': current_price,

            # Категорії як масив
            'categories': categories,

            # Метадані для аналітики
            'metadata': {
                'migratedAt': datetime.now().isoformat(),
                'source': 'PostgreSQL'
            }
        }

        documents.append(document)

        # Batch insert кожні 1000 документів
        if len(documents) >= batch_size:
            products_collection.insert_many(documents)
            documents = []

    # Вставляємо залишок
    if documents:
        products_collection.insert_many(documents)

    migration_time = time.time() - start_time

    print(f"\n✅ Міграція завершена за {migration_time:.2f} секунд")
    print(f"📊 Середня швидкість: {len(products) / migration_time:.0f} продуктів/сек")


def create_indexes():
    """Створення індексів для оптимізації"""

    print("\n🔍 Створення індексів...")

    indexes_created = 0

    # 1. Текстовий пошук (name + description)
    products_collection.create_index([
        ('name', TEXT),
        ('description', TEXT)
    ], name='text_search')
    indexes_created += 1
    print("  ✓ Текстовий пошук (name, description)")

    # 2. Пошук за відділом
    products_collection.create_index([('department.id', ASCENDING)])
    indexes_created += 1
    print("  ✓ Відділ")

    # 3. Пошук за наявністю
    products_collection.create_index([('inventory.inStock', ASCENDING)])
    indexes_created += 1
    print("  ✓ Наявність")

    # 4. Сортування за ціною
    products_collection.create_index([('currentPrice', ASCENDING)])
    indexes_created += 1
    print("  ✓ Ціна")

    # 5. Складений індекс для каталогу
    products_collection.create_index([
        ('department.id', ASCENDING),
        ('currentPrice', ASCENDING),
        ('inventory.inStock', ASCENDING)
    ], name='catalog_filter')
    indexes_created += 1
    print("  ✓ Фільтр каталогу (відділ + ціна + наявність)")

    # 6. Індекс для категорій
    products_collection.create_index([('categories.id', ASCENDING)])
    indexes_created += 1
    print("  ✓ Категорії")

    print(f"\n✅ Створено {indexes_created} індексів")


def verify_migration():
    """Перевірка результатів міграції"""

    print("\n📊 СТАТИСТИКА МІГРАЦІЇ:")
    print("-" * 60)

    # Кількість документів
    total_docs = products_collection.count_documents({})
    print(f"Всього продуктів: {total_docs:,}")

    # Продукти в наявності
    in_stock = products_collection.count_documents({'inventory.inStock': True})
    print(f"В наявності: {in_stock:,} ({in_stock / total_docs * 100:.1f}%)")

    # Продукти без історії цін
    no_price = products_collection.count_documents({'priceHistory': []})
    print(f"Без історії цін: {no_price:,}")

    # Середня ціна
    pipeline = [
        {'$match': {'currentPrice': {'$gt': 0}}},
        {'$group': {
            '_id': None,
            'avgPrice': {'$avg': '$currentPrice'},
            'minPrice': {'$min': '$currentPrice'},
            'maxPrice': {'$max': '$currentPrice'}
        }}
    ]

    result = list(products_collection.aggregate(pipeline))
    if result:
        stats = result[0]
        print(f"Середня ціна: {stats['avgPrice']:.2f} грн")
        print(f"Мін. ціна: {stats['minPrice']:.2f} грн")
        print(f"Макс. ціна: {stats['maxPrice']:.2f} грн")

    # Розмір колекції
    db_stats = mongo_db.command('collstats', 'products')
    size_mb = db_stats['size'] / (1024 * 1024)
    avg_doc_size = db_stats['avgObjSize']

    print(f"\nРозмір колекції: {size_mb:.2f} MB")
    print(f"Середній розмір документа: {avg_doc_size:,} байт")

    # Приклад документа
    print("\n📄 Приклад документа:")
    sample = products_collection.find_one()
    if sample:
        import json
        print(json.dumps(sample, indent=2, ensure_ascii=False, default=str)[:500] + "...")


def main():
    """Основна функція"""

    try:
        # 1. Міграція
        migrate_products()

        # 2. Індекси
        create_indexes()

        # 3. Перевірка
        verify_migration()

        print("\n" + "=" * 60)
        print("🎉 МІГРАЦІЯ УСПІШНО ЗАВЕРШЕНА!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ ПОМИЛКА: {e}")
        import traceback
        traceback.print_exc()

    finally:
        pg_cur.close()
        pg_conn.close()
        mongo_client.close()


if __name__ == "__main__":
    main()