
import json
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"


def extract_orders() -> pd.DataFrame:
    """Load orders from the CSV source."""
    path = RAW_DIR / "orders.csv"

    if not path.exists():
        raise FileNotFoundError(f"Orders file not found: {path}")

    df = pd.read_csv(path)

    required = {"order_id", "customer_id", "order_date", "amount"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns in orders.csv: {sorted(missing)}")

    return df


def extract_deliveries() -> pd.DataFrame:
    """Load delivery information from the CSV source."""
    path = RAW_DIR / "deliveries.csv"

    if not path.exists():
        raise FileNotFoundError(f"Deliveries file not found: {path}")

    df = pd.read_csv(path)

    required = {"order_id", "carrier", "status"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing columns in deliveries.csv: {sorted(missing)}"
        )

    return df


def extract_events() -> pd.DataFrame:
    """Load product-view events from the JSON source."""
    path = RAW_DIR / "events.json"

    if not path.exists():
        raise FileNotFoundError(f"Events file not found: {path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in events.json: {exc}") from exc

    if not isinstance(data, list):
        raise ValueError("events.json must contain a JSON list")

    df = pd.DataFrame(data)

    required = {"event_id", "order_id", "event_type", "product_id"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing columns in events.json: {sorted(missing)}"
        )

    return df


def extract_all() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Extract all sources and return orders, deliveries, and events."""
    orders = extract_orders()
    deliveries = extract_deliveries()
    events = extract_events()

    return orders, deliveries, events
