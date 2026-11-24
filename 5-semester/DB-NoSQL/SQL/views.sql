----------------------------------------------------------------------
-- 1. View активних продуктів з поточними цінами
----------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_ActiveProductsWithPrices AS
SELECT
    p.ProductID,
    p.Name,
    p.Description,
    d.DeptName AS Department,
    s.Name AS Supplier,
    m.Name AS Manufacturer,
    GetCurrentPrice(p.ProductID) AS CurrentPrice,
    GetProductDiscount(p.ProductID) AS Discount,
    CalculateFinalPrice(p.ProductID) AS FinalPrice,
    COALESCE(i.Quantity, 0) AS StockQuantity,
    i.ShelfLocation
FROM Products p
LEFT JOIN Departments d ON p.DepartmentID = d.DepartmentID
LEFT JOIN Suppliers s ON p.SupplierID = s.SupplierID
LEFT JOIN Manufacturers m ON p.ManufacturerID = m.ManufacturerID
LEFT JOIN Inventory i ON p.ProductID = i.ProductID
WHERE p.is_deleted = FALSE;

----------------------------------------------------------------------
-- 2. View продуктів з низьким запасом (< 10)
----------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_LowStockProducts AS
SELECT
    p.ProductID,
    p.Name,
    i.Quantity,
    i.ShelfLocation,
    d.DeptName
FROM Products p
JOIN Inventory i ON p.ProductID = i.ProductID
JOIN Departments d ON p.DepartmentID = d.DepartmentID
WHERE p.is_deleted = FALSE
  AND i.Quantity < 10
ORDER BY i.Quantity ASC;

----------------------------------------------------------------------
-- 3. View детальної інформації про замовлення
----------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_OrderDetails AS
SELECT
    o.OrderID,
    o.OrderDate,
    c.FirstName || ' ' || c.LastName AS CustomerName,
    c.Email AS CustomerEmail,
    u.Username AS CashierName,
    o.TotalAmount,
    COUNT(oi.OrderItemID) AS ItemCount
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
JOIN Users u ON o.CashierID = u.UserID
LEFT JOIN OrderItems oi ON o.OrderID = oi.OrderID
GROUP BY o.OrderID, o.OrderDate, c.FirstName, c.LastName, c.Email, u.Username, o.TotalAmount;

----------------------------------------------------------------------
-- 4. View продажів по відділам
----------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_SalesByDepartment AS
SELECT
    d.DeptName,
    COUNT(DISTINCT o.OrderID) AS TotalOrders,
    COALESCE(SUM(oi.Quantity), 0) AS TotalItemsSold,
    COALESCE(SUM(oi.Quantity * oi.PricePerUnit), 0) AS TotalRevenue
FROM Departments d
LEFT JOIN Products p ON d.DepartmentID = p.DepartmentID
LEFT JOIN OrderItems oi ON p.ProductID = oi.ProductID
LEFT JOIN Orders o ON oi.OrderID = o.OrderID
GROUP BY d.DeptName
ORDER BY TotalRevenue DESC;

----------------------------------------------------------------------
-- 5. View поточних запасів (інвентарь)
----------------------------------------------------------------------
CREATE OR REPLACE VIEW V_CurrentInventory AS
SELECT
    p.ProductID,
    p.Name AS ProductName,
    COALESCE(i.Quantity, 0) AS Quantity,
    i.ShelfLocation,
    d.DeptName AS Department
FROM Products p
LEFT JOIN Inventory i ON p.ProductID = i.ProductID
LEFT JOIN Departments d ON p.DepartmentID = d.DepartmentID
WHERE p.is_deleted = FALSE
ORDER BY p.Name;

----------------------------------------------------------------------
-- 6. View історії змін
----------------------------------------------------------------------
DROP VIEW IF EXISTS V_User_Audit_Trail;

CREATE VIEW V_User_Audit_Trail AS
SELECT
    l.ChangeDate   AS change_date,
    u.Username     AS username,
    l.TableName    AS table_name,
    l.RecordID     AS record_id,
    l.ChangeType   AS change_type
FROM Log_DataChanges l
JOIN Users u ON l.ChangedByUserID = u.UserID
WHERE l.TableName IN ('Users', 'Products', 'Inventory', 'Returns', 'Orders')
ORDER BY l.ChangeDate DESC;

----------------------------------------------------------------------
-- 7. View деталей повернень
----------------------------------------------------------------------
DROP VIEW IF EXISTS V_ReturnDetails;

CREATE OR REPLACE VIEW V_ReturnDetails AS
SELECT
    r.ReturnID,
    r.ReturnDate,
    o.OrderID,
    c.FirstName || ' ' || c.LastName AS CustomerName,
    u.Username AS CashierName,
    r.Reason,
    o.TotalAmount AS RefundAmount
FROM Returns r
JOIN Orders o ON r.OrderID = o.OrderID
JOIN Customers c ON o.CustomerID = c.CustomerID
JOIN Users u ON r.CashierID = u.UserID
ORDER BY r.ReturnDate DESC;
-----------------------------------------------------------
