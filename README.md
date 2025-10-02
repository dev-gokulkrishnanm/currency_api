# Currency Conversion API

## Overview
This project is a Flask-based API that provides currency conversion functionality. It fetches exchange rates from an external API, stores them in a SQLite database, and allows users to convert amounts between different currencies.
## Project Structure

- **currency_api.py**: Flask application that handles HTTP requests for currency conversion.
- **pipeline.py**: Script to fetch exchange rate data from an external API and store it in a SQLite database.
- **currency.db**: SQLite database file storing exchange rates (created automatically).

## Prerequisites

- Python 3.8+
- Required Python packages:
  - flask
  - sqlalchemy
  - requests

Install dependencies using:
```bash
pip install flask sqlalchemy requests
```

## Setup Instructions

### Clone the Repository:
```bash
git clone https://github.com/dev-gokulkrishnanm/currency_api/
cd currency_api
```

### Run the Data Pipeline:
Execute pipeline.py to fetch the latest exchange rates and populate the SQLite database:
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

The `pipeline.py` script fetches exchange rates from https://api.exchangerate-api.com/v4/latest/usd.

It stores the rates in a SQLite database (`currency.db`) with the following schema:

**Table**: `exchange_rates`

**Columns**:
- `currency` (String, primary key): Currency code (e.g., USD, EUR).
- `rate` (Float): Exchange rate relative to the base currency.
- `base` (String): Base currency (e.g., USD).
- `last_update` (Date): Date of the last update.

## Running the Application

1. Ensure the database is populated by running `pipeline.py`.
2. Start the Flask server with `currency_api.py`.
3. Send GET requests to the `/convert` endpoint to perform currency conversions.

## Notes

- The external API used in `pipeline.py` is https://api.exchangerate-api.com/v4/latest/usd.
- The SQLite database (`currency.db`) is created automatically when running `pipeline.py`.

## Future Improvements

- Add support for multiple base currencies.
- Implement caching to reduce external API calls.
- Add authentication for secure API access.
- Include error handling for external API failures.
