PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Users (
    user_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    username   TEXT NOT NULL UNIQUE,
    password   TEXT NOT NULL,
    full_name  TEXT NOT NULL,
    role       TEXT NOT NULL CHECK(role IN ('admin','cashier')),
    is_active  INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS Categories (
    category_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Products (
    product_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category_id  INTEGER NOT NULL REFERENCES Categories(category_id),
    price        REAL NOT NULL CHECK(price >= 0),
    stock_qty    INTEGER NOT NULL DEFAULT 0 CHECK(stock_qty >= 0),
    unit         TEXT NOT NULL DEFAULT 'pcs',
    is_active    INTEGER NOT NULL DEFAULT 1,
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS Sales (
    sale_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    cashier_id     INTEGER NOT NULL REFERENCES Users(user_id),
    subtotal       REAL NOT NULL DEFAULT 0,
    discount_pct   REAL NOT NULL DEFAULT 0,
    discount_amt   REAL NOT NULL DEFAULT 0,
    tax_pct        REAL NOT NULL DEFAULT 0,
    tax_amt        REAL NOT NULL DEFAULT 0,
    grand_total    REAL NOT NULL DEFAULT 0,
    amount_paid    REAL NOT NULL DEFAULT 0,
    change_due     REAL NOT NULL DEFAULT 0,
    payment_method TEXT NOT NULL DEFAULT 'cash',
    sale_date      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS Sale_Items (
    item_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id    INTEGER NOT NULL REFERENCES Sales(sale_id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES Products(product_id),
    quantity   INTEGER NOT NULL CHECK(quantity > 0),
    unit_price REAL NOT NULL,
    line_total REAL NOT NULL
);

INSERT OR IGNORE INTO Users (username, password, full_name, role)
VALUES ('admin', 'admin123', 'System Administrator', 'admin');

INSERT OR IGNORE INTO Users (username, password, full_name, role)
VALUES ('cashier1', 'cash123', 'Ali Cashier', 'cashier');

INSERT OR IGNORE INTO Categories (category_name)
VALUES ('Beverages'),('Snacks'),('Dairy'),('Bakery'),('Household'),('Personal Care');

INSERT OR IGNORE INTO Products (product_name, category_id, price, stock_qty, unit)
VALUES
('Mineral Water 500ml', 1, 1.50, 200, 'pcs'),
('Orange Juice 1L',     1, 3.25,  80, 'pcs'),
('Potato Chips 100g',   2, 2.00, 150, 'pcs'),
('Whole Milk 1L',       3, 2.75,  60, 'pcs'),
('White Bread Loaf',    4, 1.80,  40, 'pcs'),
('Laundry Detergent',   5, 7.50,  30, 'pcs'),
('Shampoo 200ml',       6, 4.99,  50, 'pcs');
