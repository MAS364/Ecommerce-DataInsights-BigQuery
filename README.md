# BigQuery E-commerce Analytics Web App

A cloud-native business intelligence application that runs on-demand SQL analytics against a public e-commerce dataset and presents decision-ready insights through a responsive Flask interface and Looker Studio dashboard.

## Live Project

| Resource | Link |
| --- | --- |
| Cloud Run web application | [Launch live application](https://task-b-cloud-run-1023861211173.europe-west2.run.app/) |
| Looker Studio dashboard | [Open interactive dashboard](https://datastudio.google.com/u/0/reporting/a094a2c8-bbcc-49d8-91a1-51b846bd13d0/page/tkwdF) |

## Business Problem

E-commerce teams need rapid access to product, revenue and fulfilment insights without repeatedly writing one-off queries. This project provides a deployed analytics interface that allows users to run predefined business analyses against BigQuery and review the results through a web application.

The system supports decisions such as:

- Which products generate the greatest total profit?
- Which distribution centres handle the highest sales volume?
- How is revenue changing month over month?

## Dataset

The application queries the public [`bigquery-public-data.thelook_ecommerce`](https://console.cloud.google.com/marketplace/product/bigquery-public-data/thelook-ecommerce) dataset.

The analysis uses the following tables:

- `orders`
- `order_items`
- `products`
- `distribution_centers`

Only non-returned items with a status of `Complete` or `Shipped` are included in the reported sales metrics.

## Architecture

The Flask application runs inside a Docker container on Google Cloud Run. When a user selects an analysis, the application submits the corresponding predefined GoogleSQL query to BigQuery and renders the returned results as a responsive HTML table.

Looker Studio provides a separate interactive reporting layer connected to the analytics data.

```text
User → Cloud Run-hosted Flask application → BigQuery → HTML results

User → Looker Studio dashboard → BigQuery
```

Cloud Run uses its assigned service account to authenticate with BigQuery, avoiding embedded service-account credentials in the application code.

## Analytics Implemented

### 1. Top 10 Most Profitable Products

Ranks products by total profit and reports:

- Units sold
- Total revenue
- Total profit
- Profit-margin percentage
- Brand and product category

Profit is calculated as the difference between item sale price and product cost.

### 2. Distribution Centre Performance

Compares distribution centres using:

- Units sold
- Distinct orders
- Total revenue
- Total profit
- Profit-margin percentage

Products are joined directly to their assigned distribution centres to prevent the duplicated counts that can result from joining inventory records only by product ID.

### 3. Monthly Revenue Growth

Calculates chronological month-over-month revenue performance using:

- Common table expressions
- Monthly aggregation
- The `LAG()` window function
- `SAFE_DIVIDE()` for zero-safe growth calculations
- Current- and previous-month revenue
- Month-over-month growth percentage

## SQL Techniques Demonstrated

- Multi-table `JOIN` operations
- Common table expressions
- `SUM`, `COUNT` and `COUNT(DISTINCT ...)` aggregations
- `LAG()` window functions
- Date truncation and monthly time-series analysis
- Profit and margin calculations
- `SAFE_DIVIDE()` for robust KPI calculation
- Filtering, grouping, ranking and chronological ordering
- Business-focused KPI design

## Application Features

- Three selectable business analyses
- Responsive desktop and mobile interface
- On-demand BigQuery execution
- Structured tabular results
- Clear query errors without exposing arbitrary SQL execution
- `/health` endpoint for deployment monitoring
- Serverless container deployment

## Technology Stack

`Python` `Flask` `Google BigQuery` `GoogleSQL` `Google Cloud Run` `Docker` `Gunicorn` `Looker Studio` `HTML` `CSS`

## Running Locally

### 1. Install dependencies

```bash
pip install Flask google-cloud-bigquery gunicorn
```

### 2. Authenticate with Google Cloud

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### 3. Start the application

```bash
python app.py
```

Open `http://localhost:8080` in your browser.

## Running with Docker

```bash
docker build -t bigquery-analytics-app .
docker run -p 8080:8080 bigquery-analytics-app
```

## Deployment

The application is containerised and deployed as a serverless Cloud Run service:

```bash
gcloud run deploy bigquery-analytics-app \
  --source . \
  --region europe-west2 \
  --allow-unauthenticated
```

The Cloud Run service account requires permission to create BigQuery jobs and read the required public tables.

## Results and Business Value

- Provides repeatable product, profitability and distribution-centre analysis.
- Identifies high-profit products that may deserve greater marketing or inventory attention.
- Highlights differences in distribution-centre sales contribution.
- Tracks monthly revenue direction and growth changes.
- Centralises SQL analyses in a deployed interface for on-demand access.
- Demonstrates an end-to-end workflow spanning SQL, cloud infrastructure, web development and business intelligence.

## Limitations

- The project uses a public demonstration dataset rather than live organisational data.
- `Shipped` items are included alongside `Complete` items, so the figures represent recognised and in-progress fulfilled sales rather than completed transactions only.
- Distribution-centre performance is measured using commercial contribution, not operational measures such as delivery time, labour cost or capacity utilisation.
- The application executes predefined analyses and is not intended to be a general-purpose SQL editor.

## Skills Demonstrated

- SQL analytics and KPI development
- Cloud data warehousing with BigQuery
- Window functions and time-series analysis
- Flask web application development
- Docker containerisation
- Serverless deployment on Google Cloud Run
- Service-account authentication
- Business intelligence with Looker Studio
- Translating business questions into reproducible analytics

## Author

**Mohammad Arshad Siddique**

Data Science · Analytics · Machine Learning · Cloud
