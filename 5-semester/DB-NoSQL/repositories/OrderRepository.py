from typing import List, Optional
import json
from models import OrderDetail, OrderItem


class OrderRepository:

    def __init__(self, connection, cursor):
        self.conn = connection
        self.cursor = cursor

    def create_order(
        self,
        customer_id: int,
        cashier_id: int,
        items: List[OrderItem]
    ) -> int:
        # Конвертуємо items в JSON
        items_json = json.dumps([
            {"ProductID": item.product_id, "Quantity": item.quantity}
            for item in items
        ])

        # Викликаємо процедуру
        self.cursor.execute(
            "CALL CreateOrder(%s, %s, %s::jsonb, NULL)",
            (customer_id, cashier_id, items_json)
        )

        # Отримуємо ID створеного замовлення з послідовності
        self.cursor.execute("SELECT currval('orders_orderid_seq') AS orderid")
        row = self.cursor.fetchone()
        return row['orderid']

    def get_all_orders(self) -> List[OrderDetail]:
        self.cursor.execute(
            "SELECT * FROM vw_OrderDetails ORDER BY orderdate DESC"
        )
        rows = self.cursor.fetchall()
        return [self._map_to_order_detail(row) for row in rows]

    def get_order_by_id(self, order_id: int) -> Optional[OrderDetail]:
        self.cursor.execute(
            "SELECT * FROM vw_OrderDetails WHERE orderid = %s",
            (order_id,)
        )
        row = self.cursor.fetchone()
        return self._map_to_order_detail(row) if row else None

    def create_return(
        self,
        order_id: int,
        reason: str,
        cashier_id: int
    ) -> int:
        # Викликаємо процедуру
        self.cursor.execute(
            "CALL CreateReturn(%s, %s, %s, NULL)",
            (order_id, reason, cashier_id)
        )

        # Отримуємо ID створеного повернення з послідовності
        self.cursor.execute("SELECT currval('returns_returnid_seq') AS returnid")
        row = self.cursor.fetchone()
        return row['returnid']

    def get_return_details_view(self) -> list:
        self.cursor.execute("SELECT * FROM V_ReturnDetails")
        return self.cursor.fetchall()

    def _map_to_order_detail(self, row: dict) -> OrderDetail:
        return OrderDetail(
            order_id=row['orderid'],
            order_date=row['orderdate'],
            customer_name=row['customername'],
            customer_email=row['customeremail'],
            cashier_name=row['cashiername'],
            total_amount=row['totalamount'],
            item_count=row['itemcount']
        )