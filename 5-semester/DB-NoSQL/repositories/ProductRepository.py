from typing import List, Optional
from decimal import Decimal
from models import ProductWithPrice


class ProductRepository:

    def __init__(self, connection, cursor):
        self.conn = connection
        self.cursor = cursor

    def get_all_active_products(self) -> List[ProductWithPrice]:
        self.cursor.execute("SELECT * FROM vw_ActiveProductsWithPrices")
        rows = self.cursor.fetchall()
        return [self._map_to_product_with_price(row) for row in rows]

    def get_product_by_id(self, product_id: int) -> Optional[ProductWithPrice]:
        self.cursor.execute(
            "SELECT * FROM vw_ActiveProductsWithPrices WHERE productid = %s",
            (product_id,)
        )
        row = self.cursor.fetchone()
        return self._map_to_product_with_price(row) if row else None

    def create_product(
            self,
            name: str,
            description: str,
            department_id: int,
            supplier_id: int,
            manufacturer_id: int,
            initial_price: Decimal,
            initial_quantity: int,
            shelf_location: str,
            user_id: int
    ) -> None:
        self.cursor.execute(
            "CALL CreateProduct(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (name, description, department_id, supplier_id, manufacturer_id,
             initial_price, initial_quantity, shelf_location, user_id)
        )

    def update_product(
            self,
            product_id: int,
            name: str,
            description: str,
            department_id: int,
            user_id: int
    ) -> None:
        self.cursor.execute(
            "CALL UpdateProduct(%s, %s, %s, %s, %s)",
            (product_id, name, description, department_id, user_id)
        )

    def delete_product(self, product_id: int, user_id: int) -> None:
        self.cursor.execute(
            "CALL sp_SoftDelete_Product(%s, %s)",
            (product_id, user_id)
        )

    def get_low_stock_products(self) -> List[ProductWithPrice]:
        self.cursor.execute("SELECT * FROM vw_LowStockProducts")
        rows = self.cursor.fetchall()
        return [ProductWithPrice(
            product_id=row['productid'],
            name=row['name'],
            description=None,
            department=row['deptname'],
            supplier=None,
            manufacturer=None,
            current_price=Decimal('0'),
            discount=Decimal('0'),
            final_price=Decimal('0'),
            stock_quantity=row['quantity'],
            shelf_location=row['shelflocation']
        ) for row in rows]

    def _map_to_product_with_price(self, row: dict) -> ProductWithPrice:
        return ProductWithPrice(
            product_id=row['productid'],
            name=row['name'],
            description=row['description'],
            department=row['department'],
            supplier=row['supplier'],
            manufacturer=row['manufacturer'],
            current_price=row['currentprice'],
            discount=row['discount'],
            final_price=row['finalprice'],
            stock_quantity=row['stockquantity'] or 0,
            shelf_location=row['shelflocation']
        )