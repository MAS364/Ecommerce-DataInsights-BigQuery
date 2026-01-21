import os
from flask import Flask, render_template, request
from google.cloud import bigquery

app = Flask(__name__)

# Cloud Run: service account provides auth automatically.
# Local: set GOOGLE_APPLICATION_CREDENTIALS to a service account JSON.
PROJECT_ID = os.getenv("PROJECT_ID")  # optional
client = bigquery.Client(project=PROJECT_ID)


def load_sql(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


QUERY_1_SQL = load_sql("sql/query_1_top_profit_products.sql")
QUERY_2_SQL = load_sql("sql/query_2_top_selling_by_distribution_center.sql")


def run_query(sql: str, limit: int) -> list[dict]:
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("limit", "INT64", limit)]
    )
    rows = client.query(sql, job_config=job_config).result()
    return [dict(r) for r in rows]


@app.route("/", methods=["GET"])
def home():
    return render_template(
        "index.html",
        results=None,
        error=None,
        selected_query=None,
        limit=10,
    )


@app.route("/run", methods=["POST"])
def run():
    selected_query = request.form.get("query", "q1")

    # limit from UI (default 10; clamp 1–100)
    try:
        limit = int(request.form.get("limit", "10"))
    except ValueError:
        limit = 10
    limit = max(1, min(limit, 100))

    try:
        if selected_query == "q1":
            results = run_query(QUERY_1_SQL, limit)
            title = "Query 1 – Top Profit Products"
        elif selected_query == "q2":
            results = run_query(QUERY_2_SQL, limit)
            title = "Query 2 – Top-Selling Units by Distribution Center"
        else:
            raise ValueError("Invalid query selection.")

        return render_template(
            "index.html",
            results=results,
            error=None,
            selected_query=selected_query,
            limit=limit,
            results_title=title,
        )

    except Exception as e:
        return render_template(
            "index.html",
            results=None,
            error=str(e),
            selected_query=selected_query,
            limit=limit,
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)

