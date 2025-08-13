import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "warehouse.db"

st.set_page_config(page_title="Banking ETL Dashboard", layout="wide")
st.title("🏦 Banking Transactions Dashboard")

# --- Load Data ---
@st.cache_data
def load_data():
    with sqlite3.connect(DB_PATH) as conn:
        clean_df = pd.read_sql("SELECT * FROM transactions_clean", conn, parse_dates=["ts_utc"])
        anomalies_df = pd.read_sql("SELECT * FROM transaction_anomalies", conn, parse_dates=["ts_utc"])
    return clean_df, anomalies_df

clean_df, anomalies_df = load_data()

# --- Summary Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Clean Transactions", len(clean_df))
col2.metric("Total Anomalies", len(anomalies_df))
col3.metric("Unique Accounts", clean_df["account_id"].nunique())

# --- Anomalies by Reason ---
st.subheader("Anomalies by Reason")
anomaly_counts = anomalies_df["reason"].value_counts().reset_index()
anomaly_counts.columns = ["Reason", "Count"]
st.bar_chart(anomaly_counts.set_index("Reason"))

# --- Top Merchant Categories ---
st.subheader("Top Merchant Categories")
top_cats = clean_df["merchant_category"].value_counts().head(10).reset_index()
top_cats.columns = ["Merchant Category", "Transactions"]
st.table(top_cats)

# --- Hourly Transaction Volume ---
st.subheader("Hourly Transaction Volume")
hourly_counts = clean_df.groupby("txn_hour").size().reset_index(name="Transactions")
st.line_chart(hourly_counts.set_index("txn_hour"))

# --- Raw Data View ---
st.subheader("Raw Data Preview")
with st.expander("View Clean Transactions"):
    st.dataframe(clean_df.head(50))
with st.expander("View Anomalies"):
    st.dataframe(anomalies_df.head(50))
