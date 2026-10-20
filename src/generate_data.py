
import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"


def main():
    random.seed(42)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    orders = []
    for i in range(1, 101):
        orders.append({
            "order_id": f"ORD{i:04d}",
            "customer_id": f"CUST{random.randint(1, 40):03d}",
            "order_date": (
                date(2026, 9, 1)
                + timedelta(days=random.randint(0, 29))
            ).isoformat(),
            "amount": round(random.uniform(20, 800), 2),
        })

    with (RAW_DIR / "orders.csv").open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=orders[0].keys())
        writer.writeheader()
        writer.writerows(orders)

    deliveries = []
    statuses = ["shipped", "delivered", "in_transit", "cancelled"]

    for order in orders:
        if random.random() < 0.90:
            deliveries.append({
                "order_id": order["order_id"],
                "carrier": random.choice(["DHL", "UPS", "FedEx"]),
                "status": random.choice(statuses),
            })

    with (RAW_DIR / "deliveries.csv").open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=["order_id", "carrier", "status"]
        )
        writer.writeheader()
        writer.writerows(deliveries)

    events = []
    for event_id in range(1, 301):
        events.append({
            "event_id": event_id,
            "order_id": random.choice(orders)["order_id"],
            "event_type": "product_view",
            "product_id": f"PROD{random.randint(1, 50):03d}",
        })

    with (RAW_DIR / "events.json").open(
        "w", encoding="utf-8"
    ) as file:
        json.dump(events, file, indent=2)

    print(f"Orders generated: {len(orders)}")
    print(f"Deliveries generated: {len(deliveries)}")
    print(f"Events generated: {len(events)}")
    print(f"Output directory: {RAW_DIR}")


if __name__ == "__main__":
    main()
