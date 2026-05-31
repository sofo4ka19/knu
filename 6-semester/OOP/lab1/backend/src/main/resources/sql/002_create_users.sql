CREATE TABLE IF NOT EXISTS users (
                                     id         BIGSERIAL    PRIMARY KEY,
                                     auth0_id   VARCHAR(100) NOT NULL UNIQUE,
                                     email      VARCHAR(200) NOT NULL,
                                     full_name  VARCHAR(200),
                                     role       VARCHAR(20)  NOT NULL DEFAULT 'CLIENT',
                                     created_at TIMESTAMP    NOT NULL DEFAULT NOW()
);