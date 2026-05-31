CREATE TABLE IF NOT EXISTS cars (
                                    id            BIGSERIAL PRIMARY KEY,
                                    brand         VARCHAR(100)   NOT NULL,
    model         VARCHAR(100)   NOT NULL,
    year          INT            NOT NULL,
    plate_number  VARCHAR(20)    NOT NULL UNIQUE,
    price_per_day DECIMAL(10, 2) NOT NULL,
    status        VARCHAR(30)    NOT NULL DEFAULT 'AVAILABLE',
    image_url     VARCHAR(500),
    created_at    TIMESTAMP      NOT NULL DEFAULT NOW()
    );

--test data
INSERT INTO cars (brand, model, year, plate_number, price_per_day, image_url)
VALUES
    ('Toyota',  'Camry',   2021, 'AA1234BB', 1200.00, 'https://example.com/camry.jpg'),
    ('BMW',     '3 Series',2022, 'BB5678CC', 2500.00, 'https://example.com/bmw3.jpg'),
    ('Renault', 'Clio',    2020, 'CC9999DD',  800.00, 'https://example.com/clio.jpg');