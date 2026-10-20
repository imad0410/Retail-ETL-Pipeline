
import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "retail.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def load_data(df: pd.DataFrame) -> None:
    """Load transformed order data into SQLite idempotently."""

    required_columns = [
        "order_id",
        "customer_id",
        "order_date",
        "amount",
        "carrier",
        "delivery_status",
        "product_view_count",
    ]

    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(
            f"Transformed data is missing columns: {sorted(missing)}"
        )

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)

        query = """
        INSERT INTO sales_report (
            order_id,
            customer_id,
            order_date,
            amount,
            carrier,
            delivery_status,
            product_view_count
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(order_id) DO UPDATE SET
            customer_id = excluded.customer_id,
            order_date = excluded.order_date,
            amount = excluded.amount,
            carrier = excluded.carrier,
            delivery_status = excluded.delivery_status,
            product_view_count = excluded.product_view_count,
            loaded_at = CURRENT_TIMESTAMP
        """

        records = []
        for row in df[required_columns].itertuples(index=False, name=None):
            order_id, customer_id, order_date, amount, carrier, status, views = row

            records.append((
                str(order_id),
                str(customer_id),
                pd.Timestamp(order_date).date().isoformat(),
                float(amount),
                str(carrier),
                str(status),
                int(views),
            ))

        connection.executemany(query, records)

    print(f"Loaded {len(records)} order records into {DB_PATH.name}.")
