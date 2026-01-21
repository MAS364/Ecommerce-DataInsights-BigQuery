from flask import Flask, render_template_string, request
from google.cloud import bigquery
import os

app = Flask(__name__)
client = bigquery.Client()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BigQuery on Cloud Run</title>
    <style>
        table { border-collapse: collapse; width: 90%; margin-top: 20px;}
        th, td { border: 1px solid #ddd; padding: 8px;}
        th { background-color: #f2f2f2; }
        button { margin-right: 10px; padding: 10px 20px; }
    </style>
</head>
<body>
    <h1>BigQuery Cloud Run Demo</h1>
    <form method="post">
        <button type="submit" name="query" value="1">Query 1</button>
        <button type="submit" name="query" value="2">Query 2</button>
    </form>
    {% if columns and rows %}
        <table>
            <thead>
                <tr>{% for col in columns %}<th>{{ col }}</th>{% endfor %}</tr>
            </thead>
            <tbody>
                {% for row in rows %}
                <tr>
                    {% for cell in row %}
                    <td>{{ cell }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% elif error %}
        <p style="color:red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

# Your SQL queries
QUERY_1 = """
SELECT 
  OI.product_id,
  P.name,
  P.brand,
  P.category,
  COUNT(OI.order_id) AS total_units_sold,
  ROUND(SUM(OI.sale_price),2) AS total_revenue,
  ROUND(SUM(OI.sale_price - P.cost),2) AS total_profit
FROM 
  `bigquery-public-data.thelook_ecommerce.order_items` AS OI
JOIN
  `bigquery-public-data.thelook_ecommerce.orders` AS O
  ON OI.order_id = O.order_id
JOIN
  `bigquery-public-data.thelook_ecommerce.products` AS P
  ON OI.product_id = P.id
WHERE
  OI.returned_at IS NULL 
  AND OI.status IN ('Complete','Shipped')
GROUP BY 
  OI.product_id,
  P.name,
  P.brand,
  P.category
ORDER BY 
  total_profit DESC
LIMIT 10
"""

QUERY_2 = """
SELECT 
   II.product_distribution_center_id,
   P.brand,
   P.department,
   P.name,
  COUNT(OI.order_id) AS total_units_sold
FROM 
  `bigquery-public-data.thelook_ecommerce.order_items` AS OI
JOIN 
  `bigquery-public-data.thelook_ecommerce.inventory_items` AS II
  ON OI.product_id = II.product_id
JOIN 
  `bigquery-public-data.thelook_ecommerce.products` AS P 
  ON OI.product_id = P.id
WHERE
  OI.returned_at IS NULL
  AND OI.status IN ('Complete', 'Shipped')
GROUP BY
   II.product_distribution_center_id,
   P.brand,
   P.department,
   P.name
ORDER BY
  total_units_sold DESC
LIMIT 10
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    columns = []
    rows = []
    error = None

    if request.method == 'POST':
        query_num = request.form.get('query')
        try:
            if query_num == '1':
                query = QUERY_1
            elif query_num == '2':
                query = QUERY_2
            else:
                error = "Invalid query selection."
                return render_template_string(HTML_TEMPLATE, columns=None, rows=None, error=error)

            query_job = client.query(query)
            result = query_job.result()

            columns = result.schema
            columns = [field.name for field in columns]
            rows = [list(row.values()) for row in result]

        except Exception as e:
            error = f"Error running query: {e}"

    return render_template_string(HTML_TEMPLATE, columns=columns, rows=rows, error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
