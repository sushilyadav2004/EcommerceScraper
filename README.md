# E-commerce Product Scraper

A FastAPI application that scrapes product details from a product page and stores them in Microsoft SQL Server. The web interface lets you scrape products and view saved records.

## Requirements

- Python 3.10 or newer
- Microsoft SQL Server
- An ODBC driver for SQL Server

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your database settings:

   ```dotenv
   DB_SERVER=your_sql_server
   DB_NAME=your_database
   DB_DRIVER=ODBC Driver 18 for SQL Server
   ```

   The application uses Windows trusted authentication and trusts the SQL Server certificate. Do not commit your `.env` file.

4. Start the application from the project root:

   ```powershell
   uvicorn app.main:app --reload
   ```

5. Open <http://127.0.0.1:8000>. Interactive API documentation is available at <http://127.0.0.1:8000/docs>.

## API

- `POST /products/scrape` — scrape and save a product. JSON body: `{"url": "https://..."}`
- `GET /products` — list saved products
- `GET /products/{product_id}` — get one product
- `PUT /products/{product_id}` — update a product
- `DELETE /products/{product_id}` — delete a product
