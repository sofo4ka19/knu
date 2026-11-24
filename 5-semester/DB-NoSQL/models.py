from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal


@dataclass
class Product:
    product_id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    department_id: Optional[int] = None
    supplier_id: Optional[int] = None
    manufacturer_id: Optional[int] = None
    is_deleted: bool = False
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None


@dataclass
class ProductWithPrice:
    product_id: int
    name: str
    description: Optional[str]
    department: Optional[str]
    supplier: Optional[str]
    manufacturer: Optional[str]
    current_price: Decimal
    discount: Decimal
    final_price: Decimal
    stock_quantity: int
    shelf_location: Optional[str]


@dataclass
class Inventory:
    inventory_id: Optional[int] = None
    product_id: int = 0
    quantity: int = 0
    shelf_location: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None


@dataclass
class Order:
    order_id: Optional[int] = None
    customer_id: int = 0
    order_date: Optional[datetime] = None
    total_amount: Decimal = Decimal('0')
    cashier_id: int = 0


@dataclass
class OrderDetail:
    order_id: int
    order_date: datetime
    customer_name: str
    customer_email: Optional[str]
    cashier_name: str
    total_amount: Decimal
    item_count: int


@dataclass
class OrderItem:
    product_id: int
    quantity: int


@dataclass
class Customer:
    customer_id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    email: Optional[str] = None
    is_deleted: bool = False


@dataclass
class User:
    user_id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    role_id: int = 0
    is_deleted: bool = False
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None