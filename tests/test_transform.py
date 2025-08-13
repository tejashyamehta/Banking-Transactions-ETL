import pandas as pd
from src.etl_pipeline import transform

def test_transform_basic():
    df = pd.DataFrame({
        "txn_id": ["t1","t2","t3"],
        "account_id": ["a1","a1","a1"],
        "merchant": ["m1","m1","m1"],
        "merchant_category": ["Food","Food","Food"],
        "amount_inr": [10, 60000, -5],
        "currency": ["INR","INR","INR"],
        "ts_utc": pd.to_datetime(["2024-01-01T00:00:00Z","2024-01-01T00:00:10Z","2024-01-01T00:00:20Z"], utc=True)
    })
    clean, anomalies = transform(df)
    assert len(clean) == 3
    reasons = set(anomalies["reason"].tolist())
    assert "HIGH_VALUE" in reasons
    assert "NON_POSITIVE_AMOUNT" in reasons
    assert "RAPID_REPEAT" in reasons
