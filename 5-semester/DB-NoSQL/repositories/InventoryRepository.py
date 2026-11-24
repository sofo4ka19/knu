from typing import Optional
from models import Inventory


class InventoryRepository:

    def __init__(self, connection, cursor):
        self.conn = connection
        self.cursor = cursor

    def get_by_product_id(self, product_id: int) -> Optional[Inventory]:
        self.cursor.execute(
            """
            SELECT i.*
            FROM Inventory i
            WHERE i.productid = %s
            """,
            (product_id,)
        )
        row = self.cursor.fetchone()

        if not row:
            return None

        return Inventory(
            inventory_id=row['inventoryid'],
            product_id=row['productid'],
            quantity=row['quantity'],
            shelf_location=row['shelflocation'],
            updated_at=row['updated_at'],
            updated_by=row['updated_by']
        )

    def update_inventory(
            self,
            product_id: int,
            quantity_change: int,
            user_id: int
    ) -> None:
        self.cursor.execute(
            "CALL UpdateInventory(%s, %s, %s)",
            (product_id, quantity_change, user_id)
        )

    def get_current_inventory_view(self) -> list:
        self.cursor.execute("SELECT * FROM V_CurrentInventory")
        return self.cursor.fetchall()