"""
Порівняльні тести швидкодії PostgreSQL vs MongoDB
Тестування реальних сценаріїв роботи з продуктами
"""
import os

import psycopg2
from dotenv import load_dotenv
from pymongo import MongoClient
import time
import statistics
import random
from tabulate import tabulate
import matplotlib.pyplot as plt
from datetime import datetime

# Конфігурації
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


class PerformanceTester:
    """Клас для тестування швидкодії"""

    def __init__(self):
        self.results = []
        self.product_ids = self._get_sample_products()

    def _get_sample_products(self, count=1000):
        """Отримати випадкові ID продуктів для тестів"""
        pg_cur.execute("SELECT ProductID FROM Products WHERE is_deleted = FALSE ORDER BY RANDOM() LIMIT %s", (count,))
        return [row[0] for row in pg_cur.fetchall()]

    def run_test(self, name, pg_func, mongo_func, iterations=100):
        """Запуск одного тесту"""

        print(f"\n🧪 Тест: {name}")
        print(f"   Ітерацій: {iterations}")

        # PostgreSQL
        pg_times = []
        print("   PostgreSQL: ", end="", flush=True)
        for _ in range(iterations):
            start = time.time()
            pg_func()
            pg_times.append((time.time() - start) * 1000)  # В мілісекундах
            if _ % 10 == 0:
                print(".", end="", flush=True)
        print(" ✓")

        # MongoDB
        mongo_times = []
        print("   MongoDB: ", end="", flush=True)
        for _ in range(iterations):
            start = time.time()
            mongo_func()
            mongo_times.append((time.time() - start) * 1000)
            if _ % 10 == 0:
                print(".", end="", flush=True)
        print(" ✓")

        # Статистика
        pg_avg = statistics.mean(pg_times)
        mongo_avg = statistics.mean(mongo_times)
        speedup = pg_avg / mongo_avg

        result = {
            'test': name,
            'pg_avg': pg_avg,
            'pg_median': statistics.median(pg_times),
            'pg_min': min(pg_times),
            'pg_max': max(pg_times),
            'mongo_avg': mongo_avg,
            'mongo_median': statistics.median(mongo_times),
            'mongo_min': min(mongo_times),
            'mongo_max': max(mongo_times),
            'speedup': speedup,
            'winner': 'MongoDB' if speedup > 1 else 'PostgreSQL'
        }

        self.results.append(result)

        print(f"   Результат: MongoDB {'швидше' if speedup > 1 else 'повільніше'} в {abs(speedup):.2f}x")

        return result

    # ==================== ТЕСТИ ====================

    def test_1_single_product_full_info(self):
        """Тест 1: Отримання повної інформації про продукт"""

        def pg_query():
            product_id = random.choice(self.product_ids)

            pg_cur.execute("""
                           SELECT p.ProductID,
                                  p.Name,
                                  p.Description,
                                  d.DeptName,
                                  s.Name as                    SupplierName,
                                  m.Name as                    ManufacturerName,
                                  i.Quantity,
                                  i.ShelfLocation,
                                  (SELECT Price
                                   FROM PricingHistory
                                   WHERE ProductID = p.ProductID
                                   ORDER BY EffectiveDate DESC LIMIT 1) as CurrentPrice
                           FROM Products p
                               LEFT JOIN Departments d
                           ON p.DepartmentID = d.DepartmentID
                               LEFT JOIN Suppliers s ON p.SupplierID = s.SupplierID
                               LEFT JOIN Manufacturers m ON p.ManufacturerID = m.ManufacturerID
                               LEFT JOIN Inventory i ON p.ProductID = i.ProductID
                           WHERE p.ProductID = %s
                           """, (product_id,))

            return pg_cur.fetchone()

        def mongo_query():
            product_id = random.choice(self.product_ids)
            return products_collection.find_one({'_id': product_id})

        return self.run_test(
            "1. Отримання повної інформації про 1 продукт (з JOIN'ами)",
            pg_query,
            mongo_query
        )

    def test_2_price_history(self):
        """Тест 2: Отримання історії цін продукту"""

        def pg_query():
            product_id = random.choice(self.product_ids)

            pg_cur.execute("""
                           SELECT Price, EffectiveDate
                           FROM PricingHistory
                           WHERE ProductID = %s
                           ORDER BY EffectiveDate DESC
                           """, (product_id,))

            return pg_cur.fetchall()

        def mongo_query():
            product_id = random.choice(self.product_ids)
            result = products_collection.find_one(
                {'_id': product_id},
                {'priceHistory': 1}
            )
            return result['priceHistory'] if result else []

        return self.run_test(
            "2. Історія цін продукту",
            pg_query,
            mongo_query
        )

    def test_3_catalog_page(self):
        """Тест 3: Отримання сторінки каталогу (20 продуктів)"""

        def pg_query():
            page = random.randint(0, 100)
            offset = page * 20

            pg_cur.execute("""
                           SELECT p.ProductID,
                                  p.Name,
                                  d.DeptName,
                                  i.Quantity,
                                  (SELECT Price
                                   FROM PricingHistory
                                   WHERE ProductID = p.ProductID
                                   ORDER BY EffectiveDate DESC LIMIT 1) as CurrentPrice
                           FROM Products p
                               LEFT JOIN Departments d
                           ON p.DepartmentID = d.DepartmentID
                               LEFT JOIN Inventory i ON p.ProductID = i.ProductID
                           WHERE p.is_deleted = FALSE
                           ORDER BY p.ProductID
                               LIMIT 20
                           OFFSET %s
                           """, (offset,))

            return pg_cur.fetchall()

        def mongo_query():
            page = random.randint(0, 100)
            skip = page * 20

            return list(products_collection.find(
                {'isDeleted': False},
                {
                    'name': 1,
                    'department.name': 1,
                    'inventory.quantity': 1,
                    'currentPrice': 1
                }
            ).skip(skip).limit(20))

        return self.run_test(
            "3. Сторінка каталогу (20 продуктів з пагінацією)",
            pg_query,
            mongo_query
        )

    def test_4_text_search(self):
        """Тест 4: Текстовий пошук"""

        search_terms = ['ноутбук', 'телефон', 'футболка', 'меблі', 'взуття']

        def pg_query():
            term = random.choice(search_terms)

            pg_cur.execute("""
                           SELECT ProductID, Name, Description
                           FROM Products
                           WHERE (Name ILIKE %s OR Description ILIKE %s)
                             AND is_deleted = FALSE LIMIT 20
                           """, (f'%{term}%', f'%{term}%'))

            return pg_cur.fetchall()

        def mongo_query():
            term = random.choice(search_terms)

            return list(products_collection.find(
                {
                    '$text': {'$search': term},
                    'isDeleted': False
                },
                {'name': 1, 'description': 1}
            ).limit(20))

        return self.run_test(
            "4. Текстовий пошук по назві/опису",
            pg_query,
            mongo_query,
            iterations=50  # Менше ітерацій для тексту
        )

    def test_5_filter_by_price_range(self):
        """Тест 5: Фільтр за діапазоном цін"""

        def pg_query():
            min_price = random.randint(100, 1000)
            max_price = min_price + random.randint(1000, 5000)

            pg_cur.execute("""
                           SELECT p.ProductID, p.Name
                           FROM Products p
                           WHERE p.ProductID IN (SELECT ProductID
                                                 FROM PricingHistory ph1
                                                 WHERE ph1.EffectiveDate = (SELECT MAX(EffectiveDate)
                                                                            FROM PricingHistory ph2
                                                                            WHERE ph2.ProductID = ph1.ProductID)
                                                   AND ph1.Price BETWEEN %s AND %s)
                             AND p.is_deleted = FALSE LIMIT 50
                           """, (min_price, max_price))

            return pg_cur.fetchall()

        def mongo_query():
            min_price = random.randint(100, 1000)
            max_price = min_price + random.randint(1000, 5000)

            return list(products_collection.find(
                {
                    'currentPrice': {'$gte': min_price, '$lte': max_price},
                    'isDeleted': False
                },
                {'name': 1, 'currentPrice': 1}
            ).limit(50))

        return self.run_test(
            "5. Фільтр за діапазоном цін",
            pg_query,
            mongo_query
        )

    def test_6_in_stock_products(self):
        """Тест 6: Продукти в наявності"""

        def pg_query():
            pg_cur.execute("""
                           SELECT p.ProductID, p.Name, i.Quantity
                           FROM Products p
                                    JOIN Inventory i ON p.ProductID = i.ProductID
                           WHERE i.Quantity > 0
                             AND p.is_deleted = FALSE
                           ORDER BY i.Quantity DESC LIMIT 100
                           """)

            return pg_cur.fetchall()

        def mongo_query():
            return list(products_collection.find(
                {
                    'inventory.inStock': True,
                    'isDeleted': False
                },
                {'name': 1, 'inventory.quantity': 1}
            ).sort('inventory.quantity', -1).limit(100))

        return self.run_test(
            "6. Продукти в наявності (сортування за кількістю)",
            pg_query,
            mongo_query
        )

    def test_7_complex_aggregation(self):
        """Тест 7: Складна агрегація - середня ціна по відділам"""

        def pg_query():
            pg_cur.execute("""
                           SELECT d.DeptName,
                                  COUNT(p.ProductID) as ProductCount,
                                  AVG(ph.Price)      as AvgPrice
                           FROM Departments d
                                    JOIN Products p ON d.DepartmentID = p.DepartmentID
                                    JOIN LATERAL (
                               SELECT Price
                               FROM PricingHistory
                               WHERE ProductID = p.ProductID
                               ORDER BY EffectiveDate DESC
                                   LIMIT 1
                ) ph
                           ON TRUE
                           WHERE p.is_deleted = FALSE
                           GROUP BY d.DeptName
                           """)

            return pg_cur.fetchall()

        def mongo_query():
            pipeline = [
                {'$match': {'isDeleted': False}},
                {'$group': {
                    '_id': '$department.name',
                    'productCount': {'$sum': 1},
                    'avgPrice': {'$avg': '$currentPrice'}
                }}
            ]

            return list(products_collection.aggregate(pipeline))

        return self.run_test(
            "7. Агрегація: середня ціна по відділам",
            pg_query,
            mongo_query,
            iterations=20
        )


def print_results(results):
    """Виведення результатів у вигляді таблиці"""

    print("\n" + "=" * 100)
    print("📊 РЕЗУЛЬТАТИ ТЕСТУВАННЯ ШВИДКОДІЇ")
    print("=" * 100)

    table_data = []
    for r in results:
        table_data.append([
            r['test'][:40],
            f"{r['pg_avg']:.2f} ms",
            f"{r['mongo_avg']:.2f} ms",
            f"{r['speedup']:.2f}x",
            r['winner']
        ])

    headers = ['Тест', 'PostgreSQL (avg)', 'MongoDB (avg)', 'Прискорення', 'Переможець']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))

    # Підсумок
    mongo_wins = sum(1 for r in results if r['winner'] == 'MongoDB')
    total_speedup = statistics.mean([r['speedup'] for r in results])

    print(f"\n🏆 MongoDB переміг у {mongo_wins}/{len(results)} тестах")
    print(f"📈 Середнє прискорення: {total_speedup:.2f}x")


def main():
    """Основна функція"""

    print("=" * 100)
    print("🚀 BENCHMARK: POSTGRESQL VS MONGODB")
    print("=" * 100)

    tester = PerformanceTester()

    # Запуск тестів
    tester.test_1_single_product_full_info()
    tester.test_2_price_history()
    tester.test_3_catalog_page()
    tester.test_4_text_search()
    tester.test_5_filter_by_price_range()
    tester.test_6_in_stock_products()
    tester.test_7_complex_aggregation()

    # Виведення результатів
    print_results(tester.results)

    print("\n" + "=" * 100)
    print("✅ ТЕСТУВАННЯ ЗАВЕРШЕНО")
    print("=" * 100)

    # Закриття з'єднань
    pg_cur.close()
    pg_conn.close()
    mongo_client.close()


if __name__ == "__main__":
    main()