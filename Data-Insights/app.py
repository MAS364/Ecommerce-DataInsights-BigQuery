"""Cloud-native e-commerce analytics dashboard.

Runs three predefined GoogleSQL analyses against the public
bigquery-public-data.thelook_ecommerce dataset and renders the results in a
responsive Flask interface.
"""

import os

from flask import Flask, render_template_string, request
from google.cloud import bigquery


app = Flask(__name__)
client = bigquery.Client()


HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>BigQuery E-commerce Analytics</title>
    <style>
        :root {
            color-scheme: dark;
            --background: #0b1020;
            --surface: #141b2d;
            --surface-light: #1d263b;
            --text: #f4f7fb;
            --muted: #aab4c8;
            --accent: #d4aa5c;
            --success: #39d98a;
            --danger: #ff6b6b;
            --border: #34405a;
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            background: var(--background);
            color: var(--text);
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }
        main {
            width: min(1180px, calc(100% - 2rem));
            margin: 0 auto;
            padding: 3rem 0 4rem;
        }
        h1 { margin-bottom: .5rem; font-size: clamp(2rem, 5vw, 3.5rem); }
        .intro { color: var(--muted); margin-bottom: 2rem; }
        .panel {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.25rem;
            margin-bottom: 1.5rem;
        }
        form { display: grid; grid-template-columns: 1fr auto; gap: .75rem; }
        select, button {
            min-height: 48px;
            border-radius: 10px;
            border: 1px solid var(--border);
            font: inherit;
        }
        select { width: 100%; padding: 0 .9rem; background: var(--surface-light); color: var(--text); }
        button {
            padding: 0 1.4rem;
            background: var(--accent);
            color: #17120a;
            border-color: var(--accent);
            font-weight: 700;
            cursor: pointer;
        }
        button:hover { filter: brightness(1.08); }
        .status { color: var(--success); font-weight: 700; }
        .error {
            color: var(--danger);
            background: rgba(255, 107, 107, .08);
            border: 1px solid rgba(255, 107, 107, .4);
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1.5rem;
        }
        .table-wrap { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; min-width: 720px; }
        th, td { padding: .8rem; text-align: left; border-bottom: 1px solid var(--border); }
        th { color: var(--accent); background: var(--surface-light); }
        tbody tr:hover { background: rgba(255, 255, 255, .025); }
        .empty { color: var(--muted); text-align: center; padding: 2rem; }
        @media (max-width: 640px) {
            main { padding-top: 1.5rem; }
            form { grid-template-columns: 1fr; }
            button { width: 100%; }
        }
    </style>
</head>
<body>
<main>
    <h1>BigQuery E-commerce Analytics</h1>
    <p class="intro">
        On-demand business intelligence using Flask, Google Cloud Run and
        <code>bigquery-public-data.thelook_ecommerce</code>.
    </p>

    <section class="panel">
        <form method="post">
            <select name="query" aria-label="Choose an analysis" required>
                {% for query_id, label in query_labels.items() %}
                    <option value="{{ query_id }}" {% if selected_query == query_id %}selected{% endif %}>
                        {{ label }}
                    </option>
                {% endfor %}
            </select>
            <button type="submit">Run analysis</button>
        </form>
    </section>

    {% if error %}
        <div class="error">{{ error }}</div>
    {% endif %}

    {% if columns %}
        <section class="panel">
            <p class="status">Analysis completed · {{ rows|length }} rows returned</p>
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            {% for column in columns %}<th>{{ column }}</th>{% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in rows %}
                            <tr>{% for value in row %}<td>{{ value }}</td>{% endfor %}</tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </section>
    {% elif not error %}
        <section class="panel empty">Choose an analysis and select “Run analysis”.</section>
    {% endif %}
</main>
</body>
</html>
"""


QUERY_1 = """
-- Top 10 most profitable products
SELECT
    oi.product_id,
    p.name AS product_name,
    p.brand,
    p.category,
    COUNT(*) AS total_units_sold,
    ROUND(SUM(oi.sale_price), 2) AS total_revenue,
    ROUND(SUM(oi.sale_price - p.cost), 2) AS total_profit,
    ROUND(
        100 * SAFE_DIVIDE(
            SUM(oi.sale_price - p.cost),
            SUM(oi.sale_price)
        ),
        2
    ) AS profit_margin_percentage
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
    ON oi.product_id = p.id
WHERE oi.returned_at IS NULL
  AND oi.status IN ('Complete', 'Shipped')
GROUP BY
    oi.product_id,
    p.name,
    p.brand,
    p.category
ORDER BY total_profit DESC
LIMIT 10
"""


QUERY_2 = """
-- Distribution centre performance
SELECT
    dc.id AS distribution_center_id,
    dc.name AS distribution_center_name,
    COUNT(*) AS total_units_sold,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(SUM(oi.sale_price), 2) AS total_revenue,
    ROUND(SUM(oi.sale_price - p.cost), 2) AS total_profit,
    ROUND(
        100 * SAFE_DIVIDE(
            SUM(oi.sale_price - p.cost),
            SUM(oi.sale_price)
        ),
        2
    ) AS profit_margin_percentage
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
    ON oi.product_id = p.id
JOIN `bigquery-public-data.thelook_ecommerce.distribution_centers` AS dc
    ON p.distribution_center_id = dc.id
WHERE oi.returned_at IS NULL
  AND oi.status IN ('Complete', 'Shipped')
GROUP BY
    dc.id,
    dc.name
ORDER BY total_units_sold DESC
"""


QUERY_3 = """
-- Monthly revenue and month-over-month growth
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC(DATE(o.created_at), MONTH) AS order_month,
        SUM(oi.sale_price) AS total_monthly_revenue
    FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
    JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
        ON oi.order_id = o.order_id
    WHERE oi.returned_at IS NULL
      AND oi.status IN ('Complete', 'Shipped')
      AND o.created_at IS NOT NULL
    GROUP BY order_month
),
revenue_with_previous_month AS (
    SELECT
        order_month,
        total_monthly_revenue,
        LAG(total_monthly_revenue) OVER (
            ORDER BY order_month
        ) AS previous_month_revenue
    FROM monthly_revenue
)
SELECT
    FORMAT_DATE('%Y-%m', order_month) AS order_month,
    ROUND(total_monthly_revenue, 2) AS total_monthly_revenue,
    ROUND(previous_month_revenue, 2) AS previous_month_revenue,
    ROUND(
        100 * SAFE_DIVIDE(
            total_monthly_revenue - previous_month_revenue,
            previous_month_revenue
        ),
        2
    ) AS mom_growth_percentage
FROM revenue_with_previous_month
ORDER BY order_month
"""


QUERIES = {
    "1": QUERY_1,
    "2": QUERY_2,
    "3": QUERY_3,
}

QUERY_LABELS = {
    "1": "Top 10 most profitable products",
    "2": "Distribution centre performance",
    "3": "Monthly revenue and month-over-month growth",
}


@app.route("/", methods=["GET", "POST"])
def home():
    """Render the query selector and execute a selected predefined analysis."""

    columns = []
    rows = []
    error = None
    selected_query = request.form.get("query", "1")

    if request.method == "POST":
        query = QUERIES.get(selected_query)
        if query is None:
            error = "Invalid query selection."
        else:
            try:
                query_job = client.query(query, location="US")
                result = query_job.result(timeout=120)
                columns = [field.name for field in result.schema]
                rows = [list(row.values()) for row in result]
            except Exception as exc:
                app.logger.exception("BigQuery analysis failed")
                error = f"Unable to run the selected analysis: {exc}"

    return render_template_string(
        HTML_TEMPLATE,
        columns=columns,
        rows=rows,
        error=error,
        selected_query=selected_query,
        query_labels=QUERY_LABELS,
    )


@app.get("/health")
def health():
    """Cloud Run health endpoint."""

    return {"status": "healthy", "queries_available": len(QUERIES)}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=False)
