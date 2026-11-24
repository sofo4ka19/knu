
-- Для пошуку продуктів по відділу
CREATE INDEX idx_products_department
ON Products(DepartmentID)
WHERE is_deleted = FALSE;

-- Для пошуку замовлень по клієнту
CREATE INDEX idx_orders_customer
ON Orders(CustomerID);

-- Для сортування замовлень по даті (DESC для останніх спочатку)
CREATE INDEX idx_orders_date
ON Orders(OrderDate DESC);

-- Для пошуку позицій замовлення
CREATE INDEX idx_orderitems_order
ON OrderItems(OrderID);

-- Для пошуку продуктів по постачальнику
CREATE INDEX idx_products_supplier
ON Products(SupplierID);

-- Для швидкого пошуку клієнта по email (точне співпадіння)
CREATE INDEX idx_customers_email
ON Customers USING HASH(Email);

-- Тільки для активних продуктів (економія місця)
CREATE INDEX idx_active_products
ON Products(ProductID)
WHERE is_deleted = FALSE;

-- Для швидкого пошуку історії цін
CREATE INDEX idx_pricing_product_date
ON PricingHistory(ProductID, EffectiveDate DESC);