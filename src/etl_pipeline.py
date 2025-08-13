from pathlib import Path
import pandas as pd
from src.db import ENGINE, init_db

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

def read_raw() -> pd.DataFrame:
    files = sorted(RAW_DIR.glob("*.csv"))
    if not files:
        print("No raw files found. Run: python -m src.generate_transactions --n 5000")
        return pd.DataFrame()
    dfs = [pd.read_csv(fp) for fp in files]
    return pd.concat(dfs, ignore_index=True)

def transform(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if df.empty:
        return df, pd.DataFrame(columns=["txn_id", "account_id", "reason", "ts_utc"])

    # Enforce schema & basic cleaning
    cols = ["txn_id", "account_id", "merchant", "merchant_category", "amount_inr", "currency", "ts_utc"]
    df = df[cols].copy()

    df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="coerce")
    df["ts_utc"] = pd.to_datetime(df["ts_utc"], errors="coerce", utc=True)

    # Drop critical nulls
    df = df.dropna(subset=["txn_id", "account_id", "merchant", "amount_inr", "ts_utc"])

    # Derived features
    df["txn_hour"] = df["ts_utc"].dt.hour
    df["is_high_value"] = (df["amount_inr"] > 50_000).astype(int)

    # ---- Anomaly detection ----
    anomalies = []

    # Rule 1: HIGH_VALUE
    hv = df[df["is_high_value"] == 1]
    if not hv.empty:
        anomalies.extend([
            {"txn_id": r.txn_id, "account_id": r.account_id, "reason": "HIGH_VALUE", "ts_utc": r.ts_utc}
            for r in hv.itertuples(index=False)
        ])

    # Rule 2: RAPID_REPEAT (>=3 txns within 60s by same account)
    df_sorted = df.sort_values(["account_id", "ts_utc"]).copy()
    # Convert timestamp to epoch seconds (int)
    df_sorted["ts_epoch"] = (df_sorted["ts_utc"].astype("int64") // 1_000_000_000)

    # For each account, compare current ts to ts two rows before (window size = 3)
    delta2 = df_sorted.groupby("account_id")["ts_epoch"].transform(lambda s: s - s.shift(2))
    rapid_mask = (delta2 <= 60).fillna(False)

    rapid_rows = df_sorted[rapid_mask]
    if not rapid_rows.empty:
        anomalies.extend([
            {"txn_id": r.txn_id, "account_id": r.account_id, "reason": "RAPID_REPEAT", "ts_utc": r.ts_utc}
            for r in rapid_rows.itertuples(index=False)
        ])

    # Rule 3: NON_POSITIVE_AMOUNT
    nonpos = df[df["amount_inr"] <= 0]
    if not nonpos.empty:
        anomalies.extend([
            {"txn_id": r.txn_id, "account_id": r.account_id, "reason": "NON_POSITIVE_AMOUNT", "ts_utc": r.ts_utc}
            for r in nonpos.itertuples(index=False)
        ])

    anomalies_df = pd.DataFrame(anomalies, columns=["txn_id", "account_id", "reason", "ts_utc"])
    return df.drop(columns=["is_high_value"]).assign(is_high_value=(df["amount_inr"] > 50_000).astype(int)), anomalies_df

def load(clean: pd.DataFrame, anomalies: pd.DataFrame):
    init_db()
    with ENGINE.begin() as conn:
        clean.to_sql("transactions_clean", conn, if_exists="append", index=False)
        if not anomalies.empty:
            anomalies.to_sql("transaction_anomalies", conn, if_exists="append", index=False)
    print(f"Loaded {len(clean)} clean rows, {len(anomalies)} anomalies")

if __name__ == "__main__":
    df = read_raw()
    clean, anomalies = transform(df)
    load(clean, anomalies)
