"""
Unit of Work патерн для управління транзакціями
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from repositories.ProductRepository import ProductRepository
from repositories.InventoryRepository import InventoryRepository
from repositories.OrderRepository import OrderRepository


class UnitOfWork:

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.conn = None
        self.cursor = None
        self._products = None
        self._inventory = None
        self._orders = None

    def _connect(self):
        """Встановити з'єднання з БД"""
        if not self.conn:
            self.conn = psycopg2.connect(self.connection_string)
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    @property
    def products(self) -> ProductRepository:
        """Репозиторій продуктів"""
        self._connect()
        if not self._products:
            self._products = ProductRepository(self.conn, self.cursor)
        return self._products

    @property
    def inventory(self) -> InventoryRepository:
        """Репозиторій інвентарю"""
        self._connect()
        if not self._inventory:
            self._inventory = InventoryRepository(self.conn, self.cursor)
        return self._inventory

    @property
    def orders(self) -> OrderRepository:
        """Репозиторій замовлень"""
        self._connect()
        if not self._orders:
            self._orders = OrderRepository(self.conn, self.cursor)
        return self._orders

    def begin_transaction(self) -> None:
        """Почати транзакцію (PostgreSQL автоматично починає)"""
        self._connect()

    def commit(self) -> None:
        """Застосувати зміни"""
        if self.conn:
            self.conn.commit()

    def rollback(self) -> None:
        """Відкатити зміни"""
        if self.conn:
            self.conn.rollback()

    def __enter__(self):
        """Контекстний менеджер - початок"""
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Контекстний менеджер - кінець"""
        try:
            if exc_type:
                # Якщо була помилка - rollback
                self.rollback()
            else:
                # Якщо все ОК - commit
                self.commit()
        finally:
            # Завжди закриваємо з'єднання
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

        # Не придушуємо виключення
        return False