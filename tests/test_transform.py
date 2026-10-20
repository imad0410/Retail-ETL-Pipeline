
import pandas as pd
import pytest

from src.transform import transform_data


@pytest.fixture
def sample_data():
    orders = pd.DataFrame([
        {
            "order_id": "ORD001",
            "customer_id": "CUST001",
            "order_date": "2026-09-01",
            "amount": 120.50,
        },
        {
            "order_id": "ORD002",
            "customer_id": "CUST002",
            "order_date": "2026-09-02",
            "amount": 75.00,
        },
    ])

    deliveries = pd.DataFrame([
        {
            "order_id": "ORD001",
            "carrier": "DHL",
            "status": "delivered",
        }
    ])

    events = pd.DataFrame([
        {
            "event_id": 1,
            "order_id": "ORD001",
            "event_type": "product_view",
            "product_id": "PROD001",
        },
        {
            "event_id": 2,
            "order_id": "ORD001",
            "event_type": "product_view",
            "product_id": "PROD002",
        },
        {
            "event_id": 3,
            "order_id": "ORD002",
            "event_type": "product_view",
            "product_id": "PROD003",
        },
    ])

    return orders, deliveries, events


def test_output_contains_one_row_per_order(sample_data):
    orders, deliveries, events = sample_data

    result = transform_data(orders, deliveries, events)

    assert len(result) == 2
    assert result["order_id"].nunique() == 2


def test_missing_delivery_is_preserved(sample_data):
    orders, deliveries, events = sample_data

    result = transform_data(orders, deliveries, events)
    order = result.loc[result["order_id"] == "ORD002"].iloc[0]

    assert order["delivery_status"] == "unknown"
    assert order["carrier"] == "unknown"


def test_product_views_are_aggregated(sample_data):
    orders, deliveries, events = sample_data

    result = transform_data(orders, deliveries, events)
    order = result.loc[result["order_id"] == "ORD001"].iloc[0]

    assert order["product_view_count"] == 2


def test_negative_amount_is_excluded(sample_data):
    orders, deliveries, events = sample_data
    orders.loc[0, "amount"] = -10

    result = transform_data(orders, deliveries, events)

    assert "ORD001" not in result["order_id"].tolist()
    assert len(result) == 1


def test_missing_required_column_raises_error(sample_data):
    orders, deliveries, events = sample_data
    orders = orders.drop(columns=["amount"])

    with pytest.raises(ValueError, match="missing required columns"):
        transform_data(orders, deliveries, events)
