# ReLoop Crate Systems

End-to-end B2B analytics project using SQL, Python and Power BI.

## Project Overview

ReLoop Crate Systems is a fictional B2B circular-logistics company that rents reusable insulated crates and temperature-controlled carriers to business customers.

The company manages customer contracts, crate deployments, shipments, returns, inspection, repair and redeployment.

The purpose of this project was to analyze the company's revenue, customers and operations and present the findings in a Power BI dashboard for management.

## Business Questions

The analysis focuses on a few main questions:

- How is revenue changing over time?
- Which customers generate the most revenue?
- How is revenue distributed across customer segments?
- Which contract tiers contribute the most revenue?
- How are shipments performing?
- How many shipments are late or have not arrived?
- Which suppliers have higher delivery problems?
- How does delivery performance differ across regions?

Profit/loss was not included because the dataset did not contain enough complete cost information to calculate it reliably.

## Dataset

The dataset contains 12 relational tables covering the company's commercial and operational activities.

The main tables used in the analysis are:

| Table | Used for |
|---|---|
| `customers` | Customer analysis |
| `contracts` | Contracts and contract tiers |
| `deployment_orders` | Deployment analysis |
| `invoices` | Revenue analysis |
| `shipments` | Shipment analysis |
| `order_items` | Order and crate details |
| `crate_models` | Crate model analysis |
| `regions` | Regional analysis |

Other supporting tables include suppliers, service_logs, employees and customer_addresses.

The data was provided as CSV files.

## Tools Used

- MySQL
- MySQL Workbench
- SQL
- Python
- Pandas
- NumPy
- Matplotlib
- Power BI
- DAX
- VS Code
- Git
- GitHub

## Project Workflow

The project was built in the following order:

```text
Raw CSV files
     ↓
Python data loading
     ↓
Data cleaning and validation
     ↓
MySQL
     ↓
SQL business analysis
     ↓
Python EDA and charts
     ↓
Power BI dashboard
```

### Data Loading

The CSV files were first loaded into Python using Pandas.

The SQL insert file generated for the dataset contained a large number of INSERT statements and caused practical problems in MySQL Workbench. Because of this, a separate Python loader was used to insert the CSV data into MySQL.

### Data Cleaning and Validation

The data was checked for:

- Duplicate records
- Missing values
- Data types
- Date fields
- Table relationships
- Successful data loading

One issue found during cleaning was inconsistent capitalization in the `contract_tier` column, such as `Strategic` and `STRATEGIC`. The values were standardized before analysis.

## SQL Analysis

The SQL analysis was focused on business questions rather than general SQL practice.

Some of the main analyses were:

- Top Customers by Revenue
- Revenue by Crate Model
- Revenue by Customer Region
- Repeat / Loyal Customers
- Shipment Delay Analysis
- Customer Segmentation
- Average Rental Days
- Revenue by Contract Tier

SQL techniques used included:

- JOINs
- GROUP BY and aggregations
- CTEs
- Window functions
- RANK()
- DENSE_RANK()
- PARTITION BY
- OVER()
- Date-based analysis

The SQL folder contains the final business queries used for this project.

## Python Analysis

The Python work was separated into four files.

### Data_Loading.py

Loads the raw CSV files into Pandas DataFrames and supports the MySQL loading process.

### Data_Cleaning.py

Handles data quality checks, data types, missing values, duplicates and categorical standardization.

### EDA.py

Uses the cleaned data to calculate KPIs and investigate business patterns.

### Visualization.py

Uses the results from `EDA.py` to create Matplotlib charts.

Keeping the files separate helped avoid mixing data preparation, analysis and visualization logic.

## Power BI Dashboard

The Power BI report has three pages.

### Page 1 — Executive Overview

This page gives a high-level view of the company.

It contains:

- Net Revenue
- Total Customers
- Total Contracts
- Total Deployments
- Monthly Net Revenue Trend
- Net Revenue by Contract Tier

The purpose of this page is to give management a quick view of overall performance.

### Page 2 — Customer & Revenue Analysis

This page focuses on customers and revenue.

It contains:

- Active Customers
- Average Customer Revenue
- Top Customer Revenue
- Top Revenue Band
- Top Customers by Revenue
- Customers by Revenue Band
- Net Revenue by Customer Revenue Band
- Contract Tier slicer
- Revenue Band slicer

The purpose is to understand customer performance and identify the customer segments contributing to revenue.

### Page 3 — Operations & Shipment Performance

This page focuses on logistics and shipment performance.

It contains:

- Total Deployments
- Total Shipments
- Late Shipments
- Not Arrived Shipments
- Delivery Delay Rate
- Average Transit Days
- Monthly Shipment Trend
- Monthly Deployment Trend
- Top 10 Suppliers by Late Shipments
- Shipment Performance by Delivery Status
- Top 10 Suppliers by Delivery Delay Rate
- Delivery Delay Rate by Region
- Year slicer
- Delivery Status slicer

The three pages were separated because each one answers a different type of business question: overall performance, customer/revenue performance and operations.

## Revenue Segmentation

Customers were grouped into four revenue bands based on their net revenue:

| Band | Revenue |
|---|---:|
| Bronze | < 100K |
| Silver | 100K to < 300K |
| Gold | 300K to < 500K |
| Platinum | >= 500K |

## Key Findings

The analysis showed that:

- Most customers fall into the Bronze revenue band, while the higher revenue bands contain fewer customers.
- Strategic contracts contribute the largest share of net revenue in the final Power BI view.
- Late and Not Arrived shipments are important areas to investigate from an operational perspective.
- Supplier analysis highlights suppliers with comparatively higher late-shipment counts or delivery-delay rates.
- Regional delivery-delay rates are relatively close in the displayed analysis, so large regional differences should not be assumed without further investigation.

## Data Quality Issues

A few data-quality issues were handled during the project.

The main example was inconsistent capitalization in `contract_tier`. `Strategic` and `STRATEGIC` were initially treated as different values. The values were standardized so that the same four contract tiers were used consistently across the analysis.

The project also included checks for duplicate records, missing values, date types and relationships between tables.

## Challenges

One of the main technical problems occurred while loading the database. The generated SQL file contained many INSERT statements and was difficult to work with in MySQL Workbench. A Python-based loader was therefore used to insert the CSV data into MySQL.

Another challenge was Power BI filter context. The Contract Tier filter and customer segmentation analysis were based on different parts of the model. `TREATAS` was used in the affected calculation to pass the selected customer IDs into the customer-level calculation.

## Project Structure

```text
ReLoop_Crate_Systems/
│
├── SQL/
│   └── Business_Queries.sql
│
├── Python/
│   ├── Data_Loading.py
│   ├── Data_Cleaning.py
│   ├── EDA.py
│   └── Visualization.py
│
├── PowerBI/
│   └── ReLoop_Crate_Systems_Analytics.pbix
│
├── csv/
│   ├── customers.csv
│   ├── contracts.csv
│   ├── deployment_orders.csv
│   ├── invoices.csv
│   ├── shipments.csv
│   └── ...
│
└── README.md
```

## Conclusion

This project follows a complete Data Analyst workflow from raw CSV data to a final Power BI report.

I used SQL for relational business analysis, Python for cleaning and exploratory analysis, and Power BI for the final interactive dashboard.

The main areas covered were revenue, customers, contracts, shipments, suppliers and regional operations.

## Future Improvements

Some possible improvements for the project are:

- Add more automated data-quality checks.
- Improve the customer segmentation model.
- Add predictive analysis for shipment delays.
- Add more operational KPIs.
- Further improve the Power BI model and dashboard.

## Author

Ashish Koge

Aspiring Data Analyst

Skills: SQL, Python, Power BI, Excel

## Disclaimer

ReLoop Crate Systems is a fictional company and the dataset is synthetic. This project was created for portfolio and learning purposes.