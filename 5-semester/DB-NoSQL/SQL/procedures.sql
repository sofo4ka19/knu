-- Soft Delete
----------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE sp_SoftDelete_User(
    p_UserID INT,
    p_UpdatedBy INT
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE Users
    SET is_deleted = TRUE,
        updated_by = p_UpdatedBy,
        updated_at = CURRENT_TIMESTAMP
    WHERE UserID = p_UserID AND is_deleted = FALSE;

    IF NOT FOUND THEN
        RAISE NOTICE 'User % not found or already deleted', p_UserID;
    END IF;

    INSERT INTO Log_DataChanges (TableName, RecordID, ChangeType, ChangedByUserID)
    VALUES ('Users', p_UserID, 'DELETE', p_UpdatedBy);
END;
$$;


CREATE OR REPLACE PROCEDURE sp_SoftDelete_Product(
    p_ProductID INT,
    p_UpdatedBy INT
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE Products
    SET is_deleted = TRUE,
        updated_by = p_UpdatedBy,
        updated_at = CURRENT_TIMESTAMP
    WHERE ProductID = p_ProductID AND is_deleted = FALSE;

    IF NOT FOUND THEN
        RAISE NOTICE 'Product % not found or already deleted', p_ProductID;
    END IF;

    INSERT INTO Log_DataChanges (TableName, RecordID, ChangeType, ChangedByUserID)
    VALUES ('Products', p_ProductID, 'DELETE', p_UpdatedBy);
END;
$$;


CREATE OR REPLACE PROCEDURE sp_SoftDelete_Customer(
    p_CustomerID INT
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE Customers
    SET is_deleted = TRUE
    WHERE CustomerID = p_CustomerID AND is_deleted = FALSE;

    IF NOT FOUND THEN
        RAISE NOTICE 'Customer % not found or already deleted', p_CustomerID;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_SoftDelete_Promotion(
    p_PromotionID INT
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE Promotions
    SET is_deleted = TRUE
    WHERE PromotionID = p_PromotionID AND is_deleted = FALSE;

    IF NOT FOUND THEN
        RAISE NOTICE 'Promotion % not found or already deleted', p_PromotionID;
    END IF;
END;
$$;

-- Взаємодія із сутністю продуктів
----------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE CreateProduct(
    p_Name VARCHAR(100),
    p_Description TEXT,
    p_DepartmentID INT,
    p_SupplierID INT,
    p_ManufacturerID INT,
    p_InitialPrice NUMERIC(10,2),
    p_InitialQuantity INT,
    p_ShelfLocation VARCHAR(50),
    p_UserID INT
)
LANGUAGE plpgsql AS $$
DECLARE
    v_ProductID INT;
BEGIN
    INSERT INTO Products (Name, Description, DepartmentID, SupplierID, ManufacturerID, updated_by)
    VALUES (p_Name, p_Description, p_DepartmentID, p_SupplierID, p_ManufacturerID, p_UserID)
    RETURNING ProductID INTO v_ProductID;

    INSERT INTO Inventory (ProductID, Quantity, ShelfLocation, updated_by)
    VALUES (v_ProductID, p_InitialQuantity, p_ShelfLocation, p_UserID);

    INSERT INTO PricingHistory (ProductID, Price, EffectiveDate)
    VALUES (v_ProductID, p_InitialPrice, CURRENT_DATE);

    INSERT INTO Log_DataChanges (TableName, RecordID, ChangeType, ChangedByUserID)
    VALUES ('Products', v_ProductID, 'INSERT', p_UserID);

    RAISE NOTICE 'Product created with ID: %', v_ProductID;
END;
$$;

CREATE OR REPLACE PROCEDURE UpdateProduct(
    p_ProductID INT,
    p_Name VARCHAR(100),
    p_Description TEXT,
    p_DepartmentID INT,
    p_UserID INT
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE Products
    SET Name = p_Name,
        Description = p_Description,
        DepartmentID = p_DepartmentID,
        updated_by = p_UserID,
        updated_at = CURRENT_TIMESTAMP
    WHERE ProductID = p_ProductID AND is_deleted = FALSE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Product % not found or deleted', p_ProductID;
    END IF;

    INSERT INTO Log_DataChanges (TableName, RecordID, ChangeType, ChangedByUserID)
    VALUES ('Products', p_ProductID, 'UPDATE', p_UserID);
END;
$$;

-- Взаємодія із сутністю INVENTORY
----------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE UpdateInventory(
    p_ProductID INT,
    p_QuantityChange INT,
    p_UserID INT
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE Inventory
    SET Quantity = Quantity + p_QuantityChange,
        updated_at = CURRENT_TIMESTAMP,
        updated_by = p_UserID
    WHERE ProductID = p_ProductID;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Product % not found in inventory', p_ProductID;
    END IF;

    INSERT INTO Log_DataChanges (TableName, RecordID, ChangeType, ChangedByUserID)
    VALUES ('Inventory', p_ProductID, 'UPDATE', p_UserID);
END;
$$;

-- Взаємодія із сутністю ORDERS
----------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE CreateOrder(
    p_CustomerID INT,
    p_CashierID INT,
    p_OrderItems JSONB,
    OUT p_OrderID BIGINT
)
LANGUAGE plpgsql AS $$
DECLARE
    v_TotalAmount NUMERIC(10,2) := 0;
    v_Item JSONB;
    v_Price NUMERIC(10,2);
    v_Quantity INT;
    v_ProductID INT;
BEGIN
    INSERT INTO Orders (CustomerID, CashierID, TotalAmount)
    VALUES (p_CustomerID, p_CashierID, 0)
    RETURNING OrderID INTO p_OrderID;

    FOR v_Item IN SELECT * FROM jsonb_array_elements(p_OrderItems)
    LOOP
        v_ProductID := (v_Item->>'ProductID')::INT;
        v_Quantity := (v_Item->>'Quantity')::INT;
        v_Price := CalculateFinalPrice(v_ProductID);

        -- Перевірка що товар існує
        IF v_Price = 0 THEN
            RAISE EXCEPTION 'Product % not found or has no price', v_ProductID;
        END IF;

        INSERT INTO OrderItems (OrderID, ProductID, Quantity, PricePerUnit)
        VALUES (p_OrderID, v_ProductID, v_Quantity, v_Price);

        v_TotalAmount := v_TotalAmount + (v_Price * v_Quantity);

        -- Зменшення кількості на складі
        CALL UpdateInventory(v_ProductID, -v_Quantity, p_CashierID);
    END LOOP;

    -- Оновлення загальної суми
    UPDATE Orders SET TotalAmount = v_TotalAmount WHERE OrderID = p_OrderID;

    -- Логування
    INSERT INTO Log_DataChanges (TableName, RecordID, ChangeType, ChangedByUserID)
    VALUES ('Orders', p_OrderID::INT, 'INSERT', p_CashierID);

    RETURN v_OrderID;
END;
$$;

-- Взаємодія із сутністю RETURNS
----------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE CreateReturn(
    p_OrderID BIGINT,
    p_Reason TEXT,
    p_CashierID INT,
    OUT p_ReturnID BIGINT
)
LANGUAGE plpgsql AS $$
DECLARE
    v_Item RECORD;
BEGIN
    INSERT INTO Returns (OrderID, Reason, CashierID, updated_by)
    VALUES (p_OrderID, p_Reason, p_CashierID, p_CashierID)
    RETURNING ReturnID INTO p_ReturnID;

    FOR v_Item IN
        SELECT ProductID, Quantity
        FROM OrderItems
        WHERE OrderID = p_OrderID
    LOOP
        CALL UpdateInventory(v_Item.ProductID, v_Item.Quantity, p_CashierID);
    END LOOP;

    INSERT INTO Log_DataChanges (TableName, RecordID, ChangeType, ChangedByUserID)
    VALUES ('Returns', p_ReturnID::INT, 'INSERT', p_CashierID);

    RAISE NOTICE 'Return created with ID: %', p_ReturnID;
END;
$$;

-- Створення нової ціни
----------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE AddPriceHistory(
    p_ProductID INT,
    p_Price NUMERIC(10,2),
    p_EffectiveDate DATE
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO PricingHistory (ProductID, Price, EffectiveDate)
    VALUES (p_ProductID, p_Price, p_EffectiveDate);

    RAISE NOTICE 'Price history added for Product %', p_ProductID;
END;
$$;