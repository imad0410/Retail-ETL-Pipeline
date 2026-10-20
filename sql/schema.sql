
CREATE TABLE IF NOT EXISTS sales_report (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0),
    carrier TEXT NOT NULL DEFAULT 'unknown',
    delivery_status TEXT NOT NULL DEFAULT 'unknown',
    product_view_count INTEGER NOT NULL DEFAULT 0
        CHECK (product_view_count >= 0),
    loaded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
