from os import getenv

import psycopg2
from dotenv import load_dotenv
from faker import Faker
import random
from datetime import datetime, timedelta
from tqdm import tqdm

# Конфігурація
fake = Faker('uk_UA')
PRODUCTS_COUNT = 100_000
PRICE_HISTORY_PER_PRODUCT = 5

# Підключення до PostgreSQL
load_dotenv()
conn = psycopg2.connect(
    dbname=getenv("DB_NAME"),
    user=getenv("DB_USER"),
    password=getenv("DB_PASSWORD"),
    host=getenv("DB_HOST"),
    port=getenv("DB_PORT")
)
cur = conn.cursor()

# Категорії товарів
PRODUCT_CATEGORIES = {
    'Електроніка': ['Ноутбуки', 'Телефони', 'Планшети', 'Навушники', 'Смарт-годинники'],
    'Одяг': ['Футболки', 'Джинси', 'Куртки', 'Взуття', 'Аксесуари'],
    'Продукти': ['Молочні', 'М\'ясні', 'Овочі', 'Фрукти', 'Напої'],
    'Дім': ['Меблі', 'Посуд', 'Декор', 'Текстиль', 'Освітлення'],
    'Спорт': ['Тренажери', 'Одяг для спорту', 'Взуття спортивне', 'Аксесуари'],
}

DEPARTMENTS = {
    1: 'Електроніка',
    2: 'Одяг та взуття',
    3: 'Продукти харчування'
}

def get_existing_ids():
    """Отримати існуючі ID з бази"""
    cur.execute("SELECT DepartmentID FROM Departments")
    dept_ids = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT SupplierID FROM Suppliers")
    supplier_ids = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT ManufacturerID FROM Manufacturers")
    manufacturer_ids = [row[0] for row in cur.fetchall()]

    return dept_ids, supplier_ids, manufacturer_ids


def generate_products(count=PRODUCTS_COUNT):
    """Генерація продуктів"""
    print(f"\n🏭 Генерація {count:,} продуктів...")

    # Отримуємо реальні ID з бази
    dept_ids, supplier_ids, manufacturer_ids = get_existing_ids()

    print(f"   Знайдено відділів: {len(dept_ids)}")
    print(f"   Знайдено постачальників: {len(supplier_ids)}")
    print(f"   Знайдено виробників: {len(manufacturer_ids)}")

    if not dept_ids or not supplier_ids or not manufacturer_ids:
        print("❌ ПОМИЛКА: Немає відділів/постачальників/виробників у базі!")
        return

    products_data = []
    used_names = set()  # Відстеження унікальних назв

    for i in tqdm(range(count), desc="Продукти"):
        dept_id = random.choice(dept_ids)
        supplier_id = random.choice(supplier_ids)
        manufacturer_id = random.choice(manufacturer_ids)

        # Генеруємо унікальні назви
        while True:
            category = random.choice(list(PRODUCT_CATEGORIES.keys()))
            subcategory = random.choice(PRODUCT_CATEGORIES[category])
            brand = fake.company()

            # Додаємо унікальний ID до назви
            name = f"{subcategory} {brand} {fake.word().capitalize()} #{i+1}"

            # Перевіряємо унікальність
            if name not in used_names:
                used_names.add(name)
                break

        description = fake.text(max_nb_chars=200)

        products_data.append((
            name,
            description,
            dept_id,
            supplier_id,
            manufacturer_id,
            False,  # is_deleted
            1  # updated_by
        ))

    # Batch insert (швидше)
    cur.executemany("""
        INSERT INTO Products (Name, Description, DepartmentID, SupplierID, ManufacturerID, is_deleted, updated_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, products_data)

    conn.commit()
    print(f"✅ Створено {count:,} продуктів")


def generate_inventory():
    """Генерація інвентарю для продуктів"""
    print("\n📦 Генерація інвентарю...")

    cur.execute("SELECT ProductID FROM Products WHERE is_deleted = FALSE")
    product_ids = [row[0] for row in cur.fetchall()]

    inventory_data = []

    for product_id in tqdm(product_ids, desc="Інвентар"):
        quantity = random.choices(
            [0, random.randint(1, 10), random.randint(10, 100), random.randint(100, 1000)],
            weights=[5, 20, 50, 25]  # 5% немає в наявності, 20% мало, 50% середньо, 25% багато
        )[0]

        shelf = f"{random.choice(['A', 'B', 'C', 'D'])}-{random.randint(1, 50)}-{random.randint(1, 10)}"

        inventory_data.append((
            product_id,
            quantity,
            shelf,
            1  # updated_by
        ))

    cur.executemany("""
        INSERT INTO Inventory (ProductID, Quantity, ShelfLocation, updated_by)
        VALUES (%s, %s, %s, %s)
    """, inventory_data)

    conn.commit()
    print(f"✅ Створено {len(inventory_data):,} записів інвентарю")


def generate_pricing_history():
    """Генерація історії цін"""
    print("\n💰 Генерація історії цін...")

    cur.execute("SELECT ProductID FROM Products WHERE is_deleted = FALSE")
    product_ids = [row[0] for row in cur.fetchall()]

    pricing_data = []

    for product_id in tqdm(product_ids, desc="Ціни"):
        # Базова ціна залежить від категорії
        base_price = random.choice([
            random.uniform(50, 500),      # Дешеві товари
            random.uniform(500, 5000),    # Середня цінова категорія
            random.uniform(5000, 50000),  # Дорогі товари
        ])

        # Генеруємо історію цін (зміни кожні 1-2 місяці)
        for j in range(PRICE_HISTORY_PER_PRODUCT):
            days_ago = (PRICE_HISTORY_PER_PRODUCT - j - 1) * random.randint(30, 60)
            effective_date = datetime.now() - timedelta(days=days_ago)

            # Ціна змінюється ±10%
            price_variation = random.uniform(0.9, 1.1)
            price = round(base_price * price_variation, 2)

            pricing_data.append((
                product_id,
                price,
                effective_date.date()
            ))

    cur.executemany("""
        INSERT INTO PricingHistory (ProductID, Price, EffectiveDate)
        VALUES (%s, %s, %s)
    """, pricing_data)

    conn.commit()
    print(f"✅ Створено {len(pricing_data):,} записів історії цін")


def generate_orders(count=10_000):
    """Генерація замовлень"""
    print(f"\n🛒 Генерація {count:,} замовлень...")

    cur.execute("SELECT ProductID FROM Products WHERE is_deleted = FALSE LIMIT 1000")
    popular_products = [row[0] for row in cur.fetchall()]  # Популярні товари

    for i in tqdm(range(count), desc="Замовлення"):
        customer_id = random.choice([1, 2])
        cashier_id = random.choice([2, 3, 4])
        order_date = datetime.now() - timedelta(days=random.randint(0, 365))

        # Створюємо замовлення
        cur.execute("""
            INSERT INTO Orders (CustomerID, CashierID, OrderDate, TotalAmount)
            VALUES (%s, %s, %s, 0)
            RETURNING OrderID
        """, (customer_id, cashier_id, order_date))

        order_id = cur.fetchone()[0]

        # Додаємо товари до замовлення (1-5 товарів)
        num_items = random.randint(1, 5)
        total_amount = 0

        for _ in range(num_items):
            product_id = random.choice(popular_products)
            quantity = random.randint(1, 3)

            # Отримуємо актуальну ціну
            cur.execute("""
                SELECT Price FROM PricingHistory
                WHERE ProductID = %s AND EffectiveDate <= %s
                ORDER BY EffectiveDate DESC LIMIT 1
            """, (product_id, order_date.date()))

            price_row = cur.fetchone()
            if price_row:
                price = price_row[0]

                cur.execute("""
                    INSERT INTO OrderItems (OrderID, ProductID, Quantity, PricePerUnit)
                    VALUES (%s, %s, %s, %s)
                """, (order_id, product_id, quantity, price))

                total_amount += price * quantity

        # Оновлюємо загальну суму
        cur.execute("""
            UPDATE Orders SET TotalAmount = %s WHERE OrderID = %s
        """, (total_amount, order_id))

        if i % 100 == 0:
            conn.commit()

    conn.commit()
    print(f"✅ Створено {count:,} замовлень")


def cleanup_tables():
    """Очищення таблиць перед генерацією"""
    print("\n🗑️  Очищення існуючих даних...")

    try:
        # Видаляємо залежні дані
        cur.execute("TRUNCATE TABLE OrderItems CASCADE")
        cur.execute("TRUNCATE TABLE Orders CASCADE")
        cur.execute("TRUNCATE TABLE Returns CASCADE")
        cur.execute("TRUNCATE TABLE PricingHistory CASCADE")
        cur.execute("TRUNCATE TABLE ProductCategories CASCADE")
        cur.execute("TRUNCATE TABLE Inventory CASCADE")

        # Видаляємо тестові продукти (залишаємо перші 4 оригінальні)
        cur.execute("DELETE FROM Products WHERE ProductID > 4")
        # Або повністю:
        # cur.execute("TRUNCATE TABLE Products CASCADE")

        conn.commit()
        print("✅ Таблиці очищено")

    except Exception as e:
        print(f"⚠️  Помилка очищення (можливо таблиці вже пусті): {e}")
        conn.rollback()


def verify_prerequisites():
    """Перевірка обов'язкових даних"""
    print("\n🔍 Перевірка довідкових таблиць...")

    errors = []

    # Ролі
    cur.execute("SELECT COUNT(*) FROM Roles")
    roles_count = cur.fetchone()[0]
    if roles_count == 0:
        errors.append("Roles - немає жодної ролі!")
    else:
        print(f"   ✓ Roles: {roles_count}")

    # Відділи
    cur.execute("SELECT COUNT(*) FROM Departments")
    dept_count = cur.fetchone()[0]
    if dept_count == 0:
        errors.append("Departments - немає жодного відділу!")
    else:
        print(f"   ✓ Departments: {dept_count}")

    # Постачальники
    cur.execute("SELECT COUNT(*) FROM Suppliers")
    suppliers_count = cur.fetchone()[0]
    if suppliers_count == 0:
        errors.append("Suppliers - немає жодного постачальника!")
    else:
        print(f"   ✓ Suppliers: {suppliers_count}")

    # Виробники
    cur.execute("SELECT COUNT(*) FROM Manufacturers")
    manufacturers_count = cur.fetchone()[0]
    if manufacturers_count == 0:
        errors.append("Manufacturers - немає жодного виробника!")
    else:
        print(f"   ✓ Manufacturers: {manufacturers_count}")

    # Користувачі
    cur.execute("SELECT COUNT(*) FROM Users")
    users_count = cur.fetchone()[0]
    if users_count == 0:
        errors.append("Users - немає жодного користувача!")
    else:
        print(f"   ✓ Users: {users_count}")

    # Категорії (не обов'язково, але бажано)
    cur.execute("SELECT COUNT(*) FROM Categories")
    categories_count = cur.fetchone()[0]
    if categories_count == 0:
        print(f"   ⚠️  Categories: 0 (не обов'язково, але рекомендується)")
    else:
        print(f"   ✓ Categories: {categories_count}")

    if errors:
        print("\n❌ КРИТИЧНІ ПОМИЛКИ:")
        for error in errors:
            print(f"   - {error}")
        print("\nСпочатку заповніть довідкові таблиці!")
        return False

    print("✅ Всі обов'язкові дані присутні\n")
    return True


def main():
    """Основна функція"""
    print("=" * 60)
    print("🚀 ГЕНЕРАТОР ТЕСТОВИХ ДАНИХ ДЛЯ POSTGRESQL")
    print("=" * 60)

    try:
        # 0. Перевірка передумов
        if not verify_prerequisites():
            return

        # 1. Очищення
        cleanup_tables()

        # 2. Продукти
        generate_products(PRODUCTS_COUNT)

        # 2. Інвентар
        generate_inventory()

        # 3. Історія цін
        generate_pricing_history()

        # 4. Замовлення (опціонально, можна закоментувати)
        # generate_orders(10_000)

        print("\n" + "=" * 60)
        print("✅ ГЕНЕРАЦІЯ ЗАВЕРШЕНА УСПІШНО!")
        print("=" * 60)

        # Статистика
        cur.execute("SELECT COUNT(*) FROM Products")
        print(f"📊 Продуктів: {cur.fetchone()[0]:,}")

        cur.execute("SELECT COUNT(*) FROM Inventory")
        print(f"📦 Інвентар: {cur.fetchone()[0]:,}")

        cur.execute("SELECT COUNT(*) FROM PricingHistory")
        print(f"💰 Історія цін: {cur.fetchone()[0]:,}")

        cur.execute("SELECT COUNT(*) FROM Orders")
        print(f"🛒 Замовлень: {cur.fetchone()[0]:,}")

    except Exception as e:
        print(f"\n❌ ПОМИЛКА: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()