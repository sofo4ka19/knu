CREATE OR REPLACE FUNCTION set_updated_fields()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    IF NEW.updated_by IS NULL THEN
        NEW.updated_by = 0;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_Users_BeforeUpdate
BEFORE UPDATE ON Users
FOR EACH ROW
EXECUTE FUNCTION set_updated_fields();

CREATE TRIGGER trg_Products_BeforeUpdate
BEFORE UPDATE ON Products
FOR EACH ROW
EXECUTE FUNCTION set_updated_fields();

CREATE TRIGGER trg_Inventory_BeforeUpdate
BEFORE UPDATE ON Inventory
FOR EACH ROW
EXECUTE FUNCTION set_updated_fields();

CREATE TRIGGER trg_Returns_BeforeUpdate
BEFORE UPDATE ON Returns
FOR EACH ROW
EXECUTE FUNCTION set_updated_fields();


----------------------------------------------------------------------
-- Перевірка кількості товару
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION check_inventory_quantity()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.Quantity < 0 THEN
        RAISE EXCEPTION 'Inventory quantity cannot be negative for ProductID %', NEW.ProductID;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_inventory
    BEFORE INSERT OR UPDATE ON Inventory
    FOR EACH ROW
    EXECUTE FUNCTION check_inventory_quantity();