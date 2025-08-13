PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS transactions_clean (
    txn_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    merchant TEXT NOT NULL,
    merchant_category TEXT,
    amount_inr REAL NOT NULL,
    currency TEXT NOT NULL,
    ts_utc TEXT NOT NULL,
    txn_hour INTEGER,
    is_high_value INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS transaction_anomalies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    txn_id TEXT NOT NULL,
    account_id TEXT NOT NULL,
    reason TEXT NOT NULL,
    ts_utc TEXT NOT NULL
);
