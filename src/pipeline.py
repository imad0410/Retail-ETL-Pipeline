
import logging
import sys
from pathlib import Path

from src.extract import extract_all
from src.transform import transform_data
from src.load import load_data


BASE_DIR = Path(__file__).resolve().parents[1]
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "pipeline.log",
            encoding="utf-8",
        ),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Execute the complete retail ETL pipeline."""
    try:
        logger.info("Starting retail ETL pipeline.")

        orders, deliveries, events = extract_all()
        logger.info(
            "Extraction completed: %d orders, %d deliveries, %d events.",
            len(orders),
            len(deliveries),
            len(events),
        )

        final_df = transform_data(orders, deliveries, events)
        logger.info(
            "Transformation completed: %d unique orders.",
            len(final_df),
        )

        load_data(final_df)
        logger.info("Retail ETL pipeline completed successfully.")

    except Exception:
        logger.exception("Retail ETL pipeline failed.")
        raise


if __name__ == "__main__":
    main()
