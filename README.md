# BigQuery Analytics Web App 

This project is a cloud-based analytics web application built with **Flask** and
**Google BigQuery**, deployed on **Google Cloud Run**. The application executes
analytical SQL queries on a public e-commerce dataset and displays
results in a structured HTML table.

---

## 🌐 Live Application Link

The application is deployed on Google Cloud Run and is accessible here:

🔗 https://task-b-cloud-run-1023861211173.europe-west2.run.app/

Dashboard:

🔗 https://datastudio.google.com/u/0/reporting/a094a2c8-bbcc-49d8-91a1-51b846bd13d0/page/tkwdF

---

## Business Aim

The primary business aim of this project is to support **data-driven decision
making in an e-commerce context** by providing insights into product profitability
and distribution centre performance.

Specifically, the application aims to:
- Identify **high-profit products** to support pricing, inventory, and marketing decisions
- Analyse **sales performance across distribution centres and regions** to evaluate
  operational efficiency and logistics effectiveness
- Demonstrate how large-scale transactional data can be queried efficiently using
  a cloud-native analytics platform

These insights reflect common real-world business intelligence use cases in retail
and e-commerce organisations.

---

## What the Application Does

- Provides a simple web interface to run predefined BigQuery queries
- Executes analytical SQL queries using the Google BigQuery client library
- Displays query results in a structured, readable table format
- Uses parameterized queries with a `LIMIT` value to control result size

---


## Dataset Used

This application uses the public Google BigQuery dataset:

**`bigquery-public-data.thelook_ecommerce`**

The dataset represents a fictional e-commerce business and contains tables such as:
- `products`
- `order_items`
- `distribution_centers`
- `orders`

It is commonly used for analytics and business intelligence demonstrations and supports large-scale analytical queries without requiring data ingestion.

---

## Query Formation

The SQL queries were designed to answer realistic business questions using the
`thelook_ecommerce` dataset:

- Joins are performed between `order_items`, `products`, and `distribution_centers`
  to combine sales, cost, and logistics information.
- Aggregations such as `SUM()` and `COUNT()` are used to compute revenue, profit,
  and sales volume.
- Filters are applied to focus on relevant transactions (e.g. completed sales).
- Results are ordered by key performance metrics such as total profit or units sold.
- A parameterized `LIMIT` clause is used to control the number of rows returned,
  improving usability and performance.

All SQL queries are stored separately in the `sql/` directory for clarity and reuse.

---


## Implemented Queries

### Query 1 – Top Profit Products
Identifies products with the highest total profit by calculating profit as:

**(sale_price − product cost)**

Products are ranked by total profit to highlight the most valuable items from a
business perspective.

### Query 2 – Distribution Centre Sales
Aggregates performance by distribution centre (and region where applicable),
summarising total revenue and/or items sold. This supports evaluation of regional
and operational performance.

Both queries are parameterized using a `LIMIT` value to control the number of rows
returned.

> SQL files are stored in the `sql/` directory.

---

## Architecture

User → Flask Web Application (Cloud Run)  
→ Google BigQuery (SQL execution on `thelook_ecommerce`)  
→ Results returned to Flask and displayed in the browser  

Authentication in the deployed environment is handled automatically using the
Cloud Run service account.

---

## Project Structure

```text
bigquery-project-b5/
├─ app.py
├─ Dockerfile
├─ requirements.txt
├─ templates/
│  └─ index.html
├─ static/
│  └─ styles.css
├─ sql/
│  ├─ query_1_top_profit_products.sql &  query_2_distribution_center_sales.sql
└─ README.md
```


## How to Run the Application

### Running Locally (Optional)

Local execution is useful for development and testing. When running locally,
BigQuery authentication must be configured manually.

#### Prerequisites
- Python 3.10 or higher
- A Google Cloud project
- A service account key with BigQuery access

#### Step 1: Configure credentials
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
