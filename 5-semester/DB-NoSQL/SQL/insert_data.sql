TRUNCATE TABLE
    Log_DataChanges,
    OrderItems,
    Orders,
    Returns,
    Inventory,
    PricingHistory,
    ProductCategories,
    Products,
    Customers,
    Categories,
    Departments,
    Suppliers,
    Manufacturers,
    Users,
    Roles
RESTART IDENTITY CASCADE;

-- 7.1. Roles
INSERT INTO Roles (RoleName) VALUES
('Адміністратор'),
('Касир'),
('Менеджер Складу');

-- 7.2. Users
INSERT INTO Users (Username, PasswordHash, RoleID, updated_by) VALUES
('admin_user', 'hashed_admin_pass', 1, 1),
('cashier_anna', 'hashed_anna_pass', 2, 1),
('manager_ivan', 'hashed_ivan_pass', 3, 1),
('cashier_petro', 'hashed_petro_pass', 2, 1);

-- 7.3. Departments
INSERT INTO Departments (DeptName, ManagerID) VALUES
('Електроніка', 3),
('Побутова Хімія', 3),
('Продукти харчування', 3);

-- 7.4. Suppliers
INSERT INTO Suppliers (Name, ContactPerson, Phone) VALUES
('Global Tech Supply', 'Олександр Коваль', '380671234567'),
('Eco Clean Ltd.', 'Ірина Лисенко', '380997654321');

-- 7.5. Manufacturers
INSERT INTO Manufacturers (Name, Country) VALUES
('TechGiant Inc.', 'США'),
('BioProduct UA', 'Україна');

-- 7.6. Products
INSERT INTO Products (Name, Description, DepartmentID, SupplierID, ManufacturerID, updated_by) VALUES
('Смартфон X1', 'Флагманський смартфон з OLED-екраном', 1, 1, 1, 3),
('Пральний Порошок "Свіжість"', 'Екологічний порошок для кольорових тканин', 2, 2, 2, 3),
('Монітор 27 дюймів', 'Монітор 4K для професійної роботи', 1, 1, 1, 3);

-- 7.7. Categories
INSERT INTO Categories (CategoryName, DepartmentID) VALUES
('Телефони', 1),
('Прання', 2),
('Периферия', 1);

-- 7.8. ProductCategories
INSERT INTO ProductCategories (ProductID, CategoryID) VALUES
(1, 1),
(3, 3),
(2, 2);

-- 7.9. PricingHistory
INSERT INTO PricingHistory (ProductID, Price, EffectiveDate) VALUES
(1, 15000.00, CURRENT_DATE - INTERVAL '3 months'),
(1, 15500.00, CURRENT_DATE - INTERVAL '1 month'),
(2, 250.50, CURRENT_DATE),
(3, 8900.00, CURRENT_DATE);

-- 7.10. Inventory
INSERT INTO Inventory (ProductID, Quantity, ShelfLocation, updated_by) VALUES
(1, 50, 'A1-01', 3),
(2, 120, 'B3-05', 3),
(3, 30, 'A1-02', 3);

-- 7.11. Customers
INSERT INTO Customers (FirstName, LastName, Email) VALUES
('Олег', 'Мельник', 'oleg.m@example.com'),
('Марія', 'Павленко', 'maria.p@example.com');
