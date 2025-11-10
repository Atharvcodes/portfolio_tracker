DROP DATABASE IF EXISTS wealthwise;
CREATE DATABASE wealthwise;

\c wealthwise;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    symbol VARCHAR(20) NOT NULL,
    transaction_type VARCHAR(4) NOT NULL CHECK (transaction_type IN ('BUY', 'SELL')),
    units INTEGER NOT NULL CHECK (units > 0),
    price DECIMAL(15, 2) NOT NULL CHECK (price > 0),
    transaction_date DATE NOT NULL CHECK (transaction_date <= CURRENT_DATE),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE prices (
    symbol VARCHAR(20) PRIMARY KEY,
    current_price DECIMAL(15, 2) NOT NULL CHECK (current_price > 0),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_symbol ON transactions(symbol);
CREATE INDEX idx_transactions_user_symbol ON transactions(user_id, symbol);
CREATE INDEX idx_transactions_date ON transactions(transaction_date DESC);
CREATE INDEX idx_users_email ON users(email);

INSERT INTO prices (symbol, current_price, updated_at) VALUES
    ('TCS', 3400.00, NOW()),
    ('INFY', 1500.00, NOW()),
    ('RELIANCE', 2600.00, NOW()),
    ('HDFC', 1650.00, NOW()),
    ('WIPRO', 450.00, NOW()),
    ('ICICI', 950.00, NOW()),
    ('SBIN', 620.00, NOW()),
    ('HDFCBANK', 1580.00, NOW()),
    ('BHARTIARTL', 890.00, NOW()),
    ('ITC', 410.00, NOW()),
    ('KOTAKBANK', 1720.00, NOW()),
    ('LT', 3350.00, NOW()),
    ('AXISBANK', 1050.00, NOW()),
    ('MARUTI', 11200.00, NOW()),
    ('SUNPHARMA', 1480.00, NOW());

SELECT 'Database setup completed' as status;
SELECT COUNT(*) as price_count FROM prices;
