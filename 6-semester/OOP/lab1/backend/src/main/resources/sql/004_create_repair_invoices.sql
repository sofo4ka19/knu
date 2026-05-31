CREATE TABLE IF NOT EXISTS repair_invoices (
                                               id                 BIGSERIAL      PRIMARY KEY,
                                               order_id           BIGINT         NOT NULL UNIQUE REFERENCES orders(id),
                                               damage_description TEXT           NOT NULL,
                                               repair_cost        DECIMAL(10, 2) NOT NULL,
                                               created_at         TIMESTAMP      NOT NULL DEFAULT NOW()
);