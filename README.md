# Banking Transactions ETL & Dashboard

A **fresher-friendly data engineering project** that simulates banking transactions, processes them via an **ETL pipeline**, stores them in a **SQLite warehouse**, and visualizes insights with a **Streamlit dashboard**.

---

## 📌 Overview
This project demonstrates:
- **ETL pipeline** (Extract → Transform → Load)
- **Data cleaning & enrichment**
- **Anomaly detection** (fraud indicators)
- **Data warehousing** concepts
- **Interactive analytics dashboard** with Streamlit

It is designed to be **simple to run locally**, yet follows patterns similar to **real-world banking/fintech pipelines**.

---

## ⚙️ Features
- **Synthetic transaction generation** (with edge cases for anomalies)
- **ETL pipeline**:
  - **Extract**: Read all raw CSVs
  - **Transform**: Fix types, derive features (`txn_hour`, `is_high_value`)
  - **Anomaly detection rules**:
    - `HIGH_VALUE`: amount > ₹50,000
    - `RAPID_REPEAT`: ≥3 txns by same account within 60 seconds
    - `NON_POSITIVE_AMOUNT`: amount ≤ 0
  - **Load**: Append clean + anomaly data into SQLite warehouse
- **Streamlit dashboard**:
  - KPIs (total transactions, anomalies, unique accounts)
  - Anomalies by reason (bar chart)
  - Top merchant categories (table)
  - Hourly transaction trends (line chart)
  - Expanders for raw data preview
- **Unit test** for transform logic
- **GitHub Actions CI** to run tests on push/PR

---

## 🗂 File Structure
banking-etl/
├─ src/
│ ├─ init.py
│ ├─ db.py # DB engine + schema init
│ ├─ generate_transactions.py
│ ├─ etl_pipeline.py
│ └─ dashboard.py
│
├─ data/
│ ├─ raw/ # Generated CSV batches
│ └─ warehouse.db # SQLite data warehouse
│
├─ sql/
│ ├─ schema.sql
│ └─ queries.sql
│
├─ tests/
│ └─ test_transform.py
│
├─ .github/workflows/ci.yml
├─ requirements.txt
├─ .gitignore
└─ README.md

yaml
Copy
Edit

---

## 📸 Architecture
![ETL Pipeline Diagram](docs/etl_pipeline.png)

---

## 🚀 Setup & Run

```bash
# 1️⃣ Clone repo & enter folder
git clone https://github.com/yourusername/banking-etl.git
cd banking-etl

# 2️⃣ Create & activate virtual environment
# Windows PowerShell
python -m venv venv
venv\Scripts\Activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Generate transactions
python -m src.generate_transactions --n 5000

# 5️⃣ Run ETL
python -m src.etl_pipeline

# 6️⃣ View dashboard
streamlit run src/dashboard.py
📊 Example Dashboard Screenshots
(Add screenshots here after running the dashboard)

📈 Future Scope & Scaling
This project is intentionally lightweight but can scale to production-level pipelines by:

Storage upgrade: SQLite → PostgreSQL, MySQL, or cloud warehouses (Snowflake, Redshift, BigQuery)

Processing upgrade: Pandas → PySpark/Dask for large datasets

Orchestration: Manual run → Apache Airflow or Prefect DAG

Streaming: Batch → Real-time ingestion with Kafka, AWS Kinesis

Data lake: Store raw/processed in AWS S3, Azure Data Lake, or GCP Cloud Storage

Monitoring & alerts: Auto-detect anomalies and send alerts via email/Slack

Dashboards: Streamlit → Tableau, Power BI, Looker