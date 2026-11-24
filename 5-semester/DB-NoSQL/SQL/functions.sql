-- ФУНКЦІЇ
----------------------------------------------------------------------

-- 1. Функція отримання поточної ціни товару
CREATE OR REPLACE FUNCTION GetCurrentPrice(p_ProductID INT)
RETURNS NUMERIC(10, 2)
LANGUAGE sql
AS $$
    SELECT COALESCE(Price, 0)
    FROM PricingHistory
    WHERE ProductID = p_ProductID
      AND EffectiveDate <= CURRENT_DATE
    ORDER BY EffectiveDate DESC
    LIMIT 1;
$$;


-- 2. Функція отримання знижки на продукт
CREATE OR REPLACE FUNCTION GetProductDiscount(p_ProductID INT)
RETURNS NUMERIC(5,2) AS $$
DECLARE
    v_Discount NUMERIC(5,2);
BEGIN
    SELECT MAX(pr.DiscountPercentage) INTO v_Discount
    FROM ProductPromotions pp
    JOIN Promotions pr ON pp.PromotionID = pr.PromotionID
    WHERE pp.ProductID = p_ProductID
        AND pr.is_deleted = FALSE
        AND CURRENT_DATE BETWEEN pr.StartDate AND pr.EndDate;

    RETURN COALESCE(v_Discount, 0);
END;
$$ LANGUAGE plpgsql;


-- 3. Функція розрахунку фінальної ціни з знижкою
CREATE OR REPLACE FUNCTION CalculateFinalPrice(p_ProductID INT)
RETURNS NUMERIC(10,2) AS $$
DECLARE
    v_BasePrice NUMERIC(10,2);
    v_Discount NUMERIC(5,2);
BEGIN
    v_BasePrice := GetCurrentPrice(p_ProductID);
    v_Discount := GetProductDiscount(p_ProductID);

    -- Якщо немає ціни, повертаємо 0
    IF v_BasePrice IS NULL THEN
        RETURN 0;
    END IF;

    RETURN v_BasePrice * (1 - v_Discount / 100);
END;
$$ LANGUAGE plpgsql;