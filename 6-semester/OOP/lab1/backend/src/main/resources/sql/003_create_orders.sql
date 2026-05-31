CREATE TABLE IF NOT EXISTS orders (
                                      id               BIGSERIAL      PRIMARY KEY,
                                      car_id           BIGINT         NOT NULL REFERENCES cars(id),
                                      user_id          BIGINT         NOT NULL REFERENCES users(id),
                                      passport_data    VARCHAR(200)   NOT NULL,
                                      start_date       DATE           NOT NULL,
                                      end_date         DATE           NOT NULL,
                                      total_price      DECIMAL(10, 2) NOT NULL,
                                      status           VARCHAR(30)    NOT NULL DEFAULT 'PENDING',
                                      rejection_reason TEXT,
                                      created_at       TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status  ON orders(status);