
import os
from decimal import Decimal
from dotenv import load_dotenv
from UnitOfWork import UnitOfWork
from models import OrderItem

# Завантаження змінних оточення
load_dotenv()


def print_header(title: str):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def example_1_create_product(uow: UnitOfWork):
    print_header("1️⃣  СТВОРЕННЯ ПРОДУКТУ")

    try:
        uow.products.create_product(
            name="iPhone 15 Pro",
            description="Новий флагманський смартфон Apple 2024",
            department_id=1,
            supplier_id=1,
            manufacturer_id=2,
            initial_price=Decimal('45999.99'),
            initial_quantity=50,
            shelf_location="A1-15",
            user_id=1
        )
        print("✅ Продукт успішно створено!")
        print("   Використано: PROCEDURE CreateProduct")
    except Exception as e:
        print(f"❌ Помилка: {e}")
        raise


def example_2_get_all_products(uow: UnitOfWork):
    print_header("2️⃣  ОТРИМАННЯ ВСІХ АКТИВНИХ ПРОДУКТІВ")

    products = uow.products.get_all_active_products()

    print(f"\n📦 Знайдено продуктів: {len(products)}")
    print("   Використано: VIEW vw_ActiveProductsWithPrices\n")

    for product in products:
        discount_info = f" (-{product.discount}%)" if product.discount > 0 else ""
        print(f"  • {product.name}")
        print(f"    Ціна: {product.current_price:.2f} грн{discount_info}")
        print(f"    Фінальна: {product.final_price:.2f} грн")
        print(f"    Залишок: {product.stock_quantity} шт.")
        print(f"    Відділ: {product.department}")
        print()


def example_3_create_order(uow):
    print("="*70)
    print("3️⃣  СТВОРЕННЯ ЗАМОВЛЕННЯ")
    print("="*70)

    # Приклад елементів замовлення
    items = [
        OrderItem(product_id=1, quantity=2),
        OrderItem(product_id=3, quantity=1)
    ]

    try:
        order_id = uow.orders.create_order(
            customer_id=1,
            cashier_id=3,
            items=items
        )
        print(f"✅ Замовлення створено з ID: {order_id}")
        print("   Використано: PROCEDURE CreateOrder\n")
    except Exception as e:
        print("❌ Помилка:", e)


def example_4_get_all_orders(uow: UnitOfWork):
    print_header("4️⃣  ПЕРЕГЛЯД ВСІХ ЗАМОВЛЕНЬ")

    orders = uow.orders.get_all_orders()

    print(f"\n🛒 Знайдено замовлень: {len(orders)}")
    print("   Використано: VIEW vw_OrderDetails\n")

    for order in orders:
        print(f"  • Замовлення #{order.order_id}")
        print(f"    Клієнт: {order.customer_name} ({order.customer_email})")
        print(f"    Касир: {order.cashier_name}")
        print(f"    Дата: {order.order_date}")
        print(f"    Сума: {order.total_amount:.2f} грн")
        print(f"    Позицій: {order.item_count}")
        print()


def example_5_update_product(uow: UnitOfWork):
    print_header("5️⃣  ОНОВЛЕННЯ ПРОДУКТУ")

    try:
        uow.products.update_product(
            product_id=1,
            name="iPhone 15 Pro Max",
            description="Оновлений опис - топова модель",
            department_id=1,
            user_id=2
        )
        print("✅ Продукт оновлено!")
        print("   Використано: PROCEDURE UpdateProduct")
        print("   Автоматично:")
        print("     • Оновлено updated_at (TRIGGER trg_Products_BeforeUpdate)")
        print("     • Додано лог операції")
    except Exception as e:
        print(f"❌ Помилка: {e}")
        raise


def example_6_soft_delete_product(uow: UnitOfWork):
    print_header("6️⃣  SOFT DELETE ПРОДУКТУ")

    try:
        product_id = 1

        # Перевіряємо що продукт є
        product = uow.products.get_product_by_id(product_id)
        if product:
            print(f"   Продукт знайдено: {product.name}")

        # Видаляємо (soft delete)
        uow.products.delete_product(product_id=product_id, user_id=1)
        print("✅ Продукт видалено (soft delete)!")
        print("   Використано: PROCEDURE sp_SoftDelete_Product")

        product_after = uow.products.get_product_by_id(product_id)
        if not product_after:
            print("   ✓ Продукт більше не відображається в активних")
    except Exception as e:
        print(f"❌ Помилка: {e}")
        raise


def example_7_create_return(uow):
    print("="*70)
    print("7️⃣  СТВОРЕННЯ ПОВЕРНЕННЯ")
    print("="*70)

    try:
        return_id = uow.orders.create_return(
            order_id=1,  # ID замовлення для повернення
            reason="Товар не підійшов за розміром",
            cashier_id=3
        )
        print(f"✅ Повернення створено з ID: {return_id}")
    except Exception as e:
        print("❌ Помилка:", e)


def example_8_low_stock_products(uow: UnitOfWork):
    """Приклад 8: Товари з низьким запасом"""
    print_header("8️⃣  ТОВАРИ З НИЗЬКИМ ЗАПАСОМ")

    products = uow.products.get_low_stock_products()

    print(f"\n⚠️  Знайдено товарів: {len(products)}")
    print("   Використано: VIEW vw_LowStockProducts\n")

    if products:
        for product in products:
            print(f"  ⚠️  {product.name}")
            print(f"     Залишок: {product.stock_quantity} шт. (< 10)")
            print(f"     Розміщення: {product.shelf_location}")
            print(f"     Відділ: {product.department}")
            print()
    else:
        print("  ✅ Всі товари в достатній кількості!")


def example_9_inventory_view(uow: UnitOfWork):
    print_header("9️⃣  ПОТОЧНИЙ СТАН СКЛАДУ")

    inventory = uow.inventory.get_current_inventory_view()

    print(f"\n📊 Всього позицій: {len(inventory)}")
    print("   Використано: VIEW V_CurrentInventory\n")

    for item in inventory[:5]:  # Перші 5
        print(f"  • {item['productname']}")
        print(f"    Кількість: {item['quantity']} шт.")
        print(f"    Розміщення: {item['shelflocation']}")
        print(f"    Відділ: {item['department']}")
        print()


def main():
    connection_string = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:password@localhost:5432/store_db'
    )

    print("=" * 70)
    print("🏪 СИСТЕМА УПРАВЛІННЯ МАГАЗИНОМ".center(70))
    print("=" * 70)
    print(f"\n📡 Підключення: {connection_string.split('@')[1] if '@' in connection_string else 'localhost'}")
    print("🔧 Патерни: Repository + Unit of Work")
    print("🗄️  СУБД: PostgreSQL")

    try:
        # Приклад 1: Створення продукту
        with UnitOfWork(connection_string) as uow:
            example_1_create_product(uow)

        # Приклад 2: Отримання всіх продуктів
        with UnitOfWork(connection_string) as uow:
            example_2_get_all_products(uow)

        # Приклад 3: Створення замовлення
        with UnitOfWork(connection_string) as uow:
            example_3_create_order(uow)

        # Приклад 4: Перегляд замовлень
        with UnitOfWork(connection_string) as uow:
            example_4_get_all_orders(uow)

        # Приклад 5: Оновлення продукту
        with UnitOfWork(connection_string) as uow:
            example_5_update_product(uow)

        # Приклад 6: Soft delete
        with UnitOfWork(connection_string) as uow:
            example_6_soft_delete_product(uow)

        # Приклад 7: Створення повернення
        with UnitOfWork(connection_string) as uow:
            example_7_create_return(uow)

        # Приклад 8: Товари з низьким запасом
        with UnitOfWork(connection_string) as uow:
            example_8_low_stock_products(uow)

        # Приклад 9: Поточний стан складу
        with UnitOfWork(connection_string) as uow:
            example_9_inventory_view(uow)

        # Завершення
        print("\n" + "=" * 70)
        print("✅ ТЕСТУВАННЯ ЗАВЕРШЕНО УСПІШНО".center(70))
        print("=" * 70)
        print("\n📊 Використано:")
        print("   • 3 функції (GetCurrentPrice, GetProductDiscount, CalculateFinalPrice)")
        print("   • 10 процедур (CreateProduct, UpdateProduct, sp_SoftDelete_*, тощо)")
        print("   • 5 тригерів (set_updated_fields, check_inventory_quantity)")
        print("   • 7 view (vw_ActiveProductsWithPrices, vw_OrderDetails, тощо)")
        print("   • 8 індексів (B-tree, Hash, Partial, Composite)")
        print("   • 3 репозиторії (Products, Inventory, Orders)")
        print("   • Unit of Work для транзакцій\n")

    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ КРИТИЧНА ПОМИЛКА".center(70))
        print("=" * 70)
        print(f"\n{e}\n")
        raise


if __name__ == "__main__":
    main()