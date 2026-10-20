

\# Retail ETL Pipeline



A reproducible data engineering project that integrates retail orders,

delivery information, and product-view events into a unified SQL report.



\## Overview



This project demonstrates how to build a small ETL pipeline using Python,

pandas, and SQLite. It extracts data from CSV and JSON sources, validates

and transforms records, aggregates product-view events, and loads the

results into a relational database.



All demonstration data is synthetic.



\## Architecture



```text

Orders CSV ───────┐

&#x20;                 │

Deliveries CSV ───┼──> Extraction

&#x20;                 │        |

Events JSON ──────┘        v

&#x20;                    Transformation

&#x20;                         |

&#x20;                         v

&#x20;                   SQLite Loading

&#x20;                         |

&#x20;                         v

&#x20;                    sales\_report

```



\## Features



\- Multi-source data extraction

\- Data cleaning and validation

\- Product-view aggregation by order

\- Handling of missing delivery records

\- SQL loading with conflict handling

\- Logging and automated tests

\- Reproducible synthetic data generation



\## Tech Stack



\- Python

\- pandas

\- SQLite

\- SQL

\- pytest

\- Git



\## Project Structure



```text

Retail-ETL-Pipeline/

├── data/

│   └── raw/

├── logs/

├── reports/

├── sql/

│   └── schema.sql

├── src/

│   ├── extract.py

│   ├── generate\_data.py

│   ├── load.py

│   ├── pipeline.py

│   └── transform.py

├── tests/

│   ├── test\_pipeline.py

│   └── test\_transform.py

├── .gitignore

├── README.md

└── requirements.txt

```



\## Getting Started



\### Requirements



\- Python 3.13 or a compatible Python version

\- Git



\### Installation



Clone the repository and enter the project directory:



```bash

git clone <YOUR\_REPOSITORY\_URL>

cd Retail-ETL-Pipeline

```



Create and activate a virtual environment on Windows:



```bat

python -m venv .venv

.venv\\Scripts\\activate

```



Install dependencies:



```bash

python -m pip install -r requirements.txt

```



Generate the synthetic source data:



```bash

python src/generate\_data.py

```



Run the ETL pipeline:



```bash

python -m src.pipeline

```



Run automated tests:



```bash

python -m pytest -v

```



\## Output



The pipeline creates a local SQLite database at `data/retail.db`.

Its `sales\_report` table contains one record per order, including

the customer, order date, amount, delivery status, carrier, and

product-view count.



The database and runtime logs are generated locally and are not

committed to the repository.



\## Data Quality and Testing



The test suite covers output uniqueness, missing delivery handling,

product-view aggregation, invalid amounts, and required columns.



The current test suite contains seven passing tests in the development

environment. Results should be revalidated after code changes.



\## Limitations and Future Improvements



\- Add explicit source-data quality metrics.

\- Improve integration-test isolation.

\- Add incremental processing and data lineage.

\- Add support for PostgreSQL.

\- Automate continuous integration with GitHub Actions.



\## Author



Add your name, LinkedIn profile, and GitHub profile here.



