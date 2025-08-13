from sqlalchemy import create_engine
from pathlib import Path
import sqlite3

# Path to SQLite DB
DB_PATH = Path(__file__).resolve().parents[1] / "data" / "warehouse.db"

# SQLAlchemy engine (used by pandas .to_sql and general DB ops)
ENGINE = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)

def init_db():
    """
    Initialize the database schema from sql/schema.sql.
    Use native sqlite3 here because the schema file has multiple statements.
    """
    schema_path = Path(__file__).resolve().parents[1] / "sql" / "schema.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(schema_sql)
