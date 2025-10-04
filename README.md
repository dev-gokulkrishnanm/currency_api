# Currency Conversion API

## Overview
This project is a Flask-based API that provides currency conversion functionality. It fetches exchange rates from an external API, stores them in a SQLite database, and allows users to convert amounts between different currencies. The data pipeline is orchestrated using Apache Airflow DAGs for automated and scheduled data processing.
## Project Structure

- **currency_api.py**: Flask application that handles HTTP requests for currency conversion.
- **pipeline.py**: Script to fetch exchange rate data from an external API and store it in a SQLite database (orchestrated via Airflow DAGs).
- **currency.db**: SQLite database file storing exchange rates (created automatically).
- **dags/**: Directory containing Airflow DAG definitions for automated data pipeline orchestration.

## Prerequisites

- Python 3.8+
- Apache Airflow 2.0+
- Required Python packages:
  - flask
  - sqlalchemy
  - requests
  - apache-airflow

Install dependencies using:
```bash
pip install flask sqlalchemy requests apache-airflow
```

## Setup Instructions

### Clone the Repository:
```bash
git clone https://github.com/dev-gokulkrishnanm/currency_api/
cd currency_api
```

### Set up Airflow:
Initialize Airflow database and create admin user:
```bash
airflow db standalone
```

### Start Airflow Services:
Start the Airflow webserver and scheduler:
```bash
# Terminal 1 - Start webserver
airflow api-server --port 8080

# Terminal 2 - Start scheduler
airflow scheduler
```

### Run the Data Pipeline:
The data pipeline is now orchestrated via Airflow DAGs. You can:

**Option 1: Trigger via Airflow UI**
- Access Airflow UI at http://localhost:8080
- Enable and trigger the currency exchange rate DAG

**Option 2: Trigger via CLI**
```bash
airflow dags trigger currency_exchange_dag
```

**Option 3: Manual execution (legacy)**
```bash
python pipeline.py
```

### Run the Flask API:
Start the Flask server to handle currency conversion requests:
```bash
python currency_api.py
```

The API will be available at http://127.0.0.1:5000.

## Usage

### API Endpoint

- **Endpoint**: `/convert`
- **Method**: GET
- **Parameters**:
  - `amount`: The amount to convert (float).
  - `from`: The source currency code (e.g., USD, EUR).
  - `to`: The target currency code (e.g., USD, EUR).

### Example Request:
```bash
curl "http://127.0.0.1:5000/convert?amount=100&from=USD&to=EUR"
```

### Example Response:
```json
{
    "amount": 100.0,
    "from": "USD",
    "to": "EUR",
    "converted_amount": 94.1234
}
```

### Error Responses:
- **Missing parameters**: `{"error": "Missing 'from', 'to', or 'amount' parameter"}` (HTTP 400)
- **Invalid amount**: `{"error": "'amount' must be a number"}` (HTTP 400)
- **Unsupported currency**: `{"error": "Currency pair USD->EUR not found"}` (HTTP 400)

## Data Pipeline

The data pipeline is orchestrated using **Apache Airflow DAGs** for automated and scheduled execution. The `pipeline.py` script fetches exchange rates from https://api.exchangerate-api.com/v4/latest/usd.

### Airflow DAG Features:
- **Scheduled execution**: Automatically runs at configured intervals
- **Retry logic**: Built-in retry mechanisms for failed tasks
- **Monitoring**: Real-time monitoring via Airflow UI
- **Logging**: Comprehensive logging for debugging
- **Dependencies**: Manages task dependencies and execution order

The pipeline stores the rates in a SQLite database (`currency.db`) with the following schema:

**Table**: `exchange_rates`

**Columns**:
- `currency` (String, primary key): Currency code (e.g., USD, EUR).
- `rate` (Float): Exchange rate relative to the base currency.
- `base` (String): Base currency (e.g., USD).
- `last_update` (Date): Date of the last update.

## Running the Application

1. **Start Airflow services** (webserver and scheduler)
2. **Configure and trigger the data pipeline DAG** via Airflow UI or CLI
3. **Start the Flask server** with `currency_api.py`
4. **Send GET requests** to the `/convert` endpoint to perform currency conversions

### Airflow UI Access:
- **URL**: http://localhost:8080
- **Username**: admin (or as configured during setup)

### API Access:
- **URL**: http://127.0.0.1:5000

## Notes

- The external API used in `pipeline.py` is https://api.exchangerate-api.com/v4/latest/usd.
- The SQLite database (`currency.db`) is created automatically when running the data pipeline.
- **Airflow DAGs** provide automated scheduling and monitoring of the data pipeline.
- Access the **Airflow UI** at http://localhost:8080 for pipeline monitoring and management.

## Future Improvements

- Add support for multiple base currencies.
- Implement caching to reduce external API calls.
- Add authentication for secure API access.
- Include error handling for external API failures.
- **Enhanced Airflow features**: Add email notifications, SLA monitoring, and advanced scheduling.
- **Data quality checks**: Implement data validation tasks in the Airflow DAG.
