
import sqlite3

from src.extract import extract_all
from src.transform import transform_data
from src.load import load_data


def test_pipeline_loads_orders_without_duplicates():
    orders, deliveries, events = extract_all()
    result = transform_data(orders, deliveries, events)

    load_data(result)
    load_data(result)

    connection = sqlite3.connect("data/retail.db")

    try:
        total_rows = connection.execute(
            "SELECT COUNT(*) FROM sales_report"
        ).fetchone()[0]

        unique_orders = connection.execute(
            "SELECT COUNT(DISTINCT order_id) FROM sales_report"
        ).fetchone()[0]

        assert total_rows == len(result)
        assert unique_orders == len(result)
    finally:
        connection.close()



def test_pipeline_preserves_orders_without_delivery():
    orders, deliveries, events = extract_all()
    result = transform_data(orders, deliveries, events)
    load_data(result)

    expected_missing = int(
        (result["delivery_status"] == "unknown").sum()
    )

    connection = sqlite3.connect("data/retail.db")

    try:
        actual_missing = connection.execute(
            """
            SELECT COUNT(*)
            FROM sales_report
            WHERE delivery_status = 'unknown'
            """
        ).fetchone()[0]

        assert actual_missing == expected_missing
    finally:
        connection.close()
