
import pandas as pd


def transform_data(
    orders: pd.DataFrame,
    deliveries: pd.DataFrame,
    events: pd.DataFrame,
) -> pd.DataFrame:
    """Clean and aggregate retail data into one row per order."""

    required_orders = {
        "order_id", "customer_id", "order_date", "amount"
    }
    required_deliveries = {"order_id", "carrier", "status"}
    required_events = {
        "event_id", "order_id", "event_type", "product_id"
    }

    for name, df, required in [
        ("orders", orders, required_orders),
        ("deliveries", deliveries, required_deliveries),
        ("events", events, required_events),
    ]:
        missing = required - set(df.columns)
        if missing:
            raise ValueError(
                f"{name} is missing required columns: {sorted(missing)}"
            )

    # Clean orders.
    orders = orders.copy()
    orders["order_id"] = orders["order_id"].astype("string").str.strip()
    orders["customer_id"] = (
        orders["customer_id"].astype("string").str.strip()
    )
    orders["order_date"] = pd.to_datetime(
        orders["order_date"], errors="coerce"
    )
    orders["amount"] = pd.to_numeric(
        orders["amount"], errors="coerce"
    )

    orders = orders.dropna(
        subset=["order_id", "customer_id", "order_date", "amount"]
    )
    orders = orders[
        (orders["order_id"] != "")
        & (orders["customer_id"] != "")
        & (orders["amount"] >= 0)
    ]

    # Keep the first valid record for each order.
    orders = orders.drop_duplicates(subset=["order_id"], keep="first")

    # Clean deliveries and keep one record per order.
    deliveries = deliveries.copy()
    deliveries["order_id"] = (
        deliveries["order_id"].astype("string").str.strip()
    )
    deliveries["status"] = (
        deliveries["status"].astype("string").str.strip().str.lower()
    )
    deliveries["carrier"] = (
        deliveries["carrier"].astype("string").str.strip()
    )

    valid_statuses = {
        "shipped", "delivered", "in_transit", "cancelled"
    }
    deliveries = deliveries[
        deliveries["order_id"].notna()
        & (deliveries["order_id"] != "")
        & deliveries["status"].isin(valid_statuses)
    ]
    deliveries = deliveries.drop_duplicates(
        subset=["order_id"], keep="last"
    )

    # Count valid product-view events for known orders only.
    events = events.copy()
    events["order_id"] = (
        events["order_id"].astype("string").str.strip()
    )
    events["event_type"] = (
        events["event_type"].astype("string").str.strip().str.lower()
    )
    events = events[
        events["order_id"].notna()
        & (events["order_id"] != "")
        & (events["event_type"] == "product_view")
    ]
    events = events.drop_duplicates(subset=["event_id"])

    known_order_ids = set(orders["order_id"])
    events = events[events["order_id"].isin(known_order_ids)]

    view_counts = (
        events.groupby("order_id")
        .size()
        .rename("product_view_count")
        .reset_index()
    )

    # Preserve orders even when no delivery or product view exists.
    result = orders.merge(
        deliveries[["order_id", "carrier", "status"]],
        on="order_id",
        how="left",
        validate="one_to_one",
    )

    result = result.rename(columns={"status": "delivery_status"})
    result["delivery_status"] = result["delivery_status"].fillna("unknown")
    result["carrier"] = result["carrier"].fillna("unknown")

    result = result.merge(
        view_counts,
        on="order_id",
        how="left",
        validate="one_to_one",
    )
    result["product_view_count"] = (
        result["product_view_count"].fillna(0).astype("int64")
    )

    result = result.sort_values("order_id").reset_index(drop=True)

    if result["order_id"].duplicated().any():
        raise ValueError("The transformed output contains duplicate order IDs.")

    return result
