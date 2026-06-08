# 📊 BigQuery Analytics Web App (Cloud-Native BI System)

## 📌 Problem
Enable fast, data-driven decision-making by building a cloud-based analytics system that queries large-scale e-commerce data and presents actionable business insights through a web interface.

---

## 📊 Data
- Public dataset: `bigquery-public-data.thelook_ecommerce`  
- Tables: orders, products, order_items, distribution_centers  
- Large-scale transactional e-commerce data  

Key business entities:
- Products  
- Revenue & profit transactions  
- Distribution centre performance  

---

## ⚙️ Approach

### Architecture
Flask Web App → Google Cloud Run → BigQuery → HTML Dashboard

- Flask handles UI and query execution  
- BigQuery runs analytical SQL queries at scale  
- Cloud Run provides serverless deployment  
- Results rendered in structured web dashboard  

---

### Analytics Layer
Built SQL-based business intelligence queries:
- Revenue and profit analysis  
- Product performance ranking  
- Distribution centre efficiency analysis  
- Aggregations using SUM, COUNT, JOIN operations  
- Filtered and sorted outputs for business relevance  

---

### Query Design
- Join-based analytical modelling across multiple tables  
- Profit calculation using sale price vs cost  
- Aggregated KPIs for business performance tracking  
- Parameterized LIMIT controls for performance optimization  

---

## 🚀 Deployment
- Deployed on Google Cloud Run  
- Containerized using Docker  
- Uses Cloud Run service account for authentication  
- Fully serverless execution with BigQuery integration  

Live App:
https://task-b-cloud-run-1023861211173.europe-west2.run.app/

Dashboard:
https://datastudio.google.com/u/0/reporting/a094a2c8-bbcc-49d8-91a1-51b846bd13d0/page/tkwdF


---

## 📈 Result
- Real-time execution of SQL analytics on large-scale dataset  
- Successfully generated product and logistics insights  
- Reduced manual analysis time through automated querying system  
- Delivered interactive business intelligence dashboard


<img width="617" height="488" alt="Screenshot 2026-06-08 at 01 31 24" src="https://github.com/user-attachments/assets/29857da4-385d-4488-9438-ddead4141256" />
<img width="549" height="776" alt="Screenshot 2026-06-08 at 01 31 38" src="https://github.com/user-attachments/assets/5a6b691d-68fc-4857-930e-e40861214cba" />








---

## 💡 Impact / Insight
- Identifies high-profit products for pricing and marketing decisions  
- Highlights distribution centre performance differences  
- Demonstrates scalable cloud-native BI architecture  
- Shows ability to combine SQL analytics + cloud deployment + web apps  
- Replicates real-world data analyst / BI engineer workflows  

---

## 🧠 Skills Demonstrated
- SQL analytics (JOINs, aggregations, KPI design)  
- Google BigQuery (cloud data warehouse)  
- Flask web development  
- Cloud Run deployment (serverless architecture)  
- Docker containerisation  
- Business intelligence & data storytelling  
