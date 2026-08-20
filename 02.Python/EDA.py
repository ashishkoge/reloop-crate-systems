# ==========================================================
# Portfolio Project #2
# ReLoop Crate Systems
#
# File: 03_EDA.py
# Author: Ashish Koge
#
# Objective:
# Perform Exploratory Data Analysis (EDA) on the cleaned
# ReLoop Crate Systems datasets and identify business
# patterns, trends, and KPI insights.
# ==========================================================


# ==========================================================
# Import Libraries
# ==========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Import Cleaned Data
# ==========================================================

import Data_Cleaning as dc

customers = dc.customers
contracts = dc.contracts
crate_models = dc.crate_models
customer_addresses = dc.customer_addresses
deployment_orders = dc.deployment_orders
employees = dc.employees
invoices = dc.invoices
order_items = dc.order_items
regions = dc.regions
service_logs = dc.service_logs
shipments = dc.shipments
suppliers = dc.suppliers

# ==========================================================
# Dataset Dictionary
# ==========================================================

datasets = {
    "customers": dc.customers,
    "contracts": dc.contracts,
    "crate_models": dc.crate_models,
    "customer_addresses": dc.customer_addresses,
    "deployment_orders": dc.deployment_orders,
    "employees": dc.employees,
    "invoices": dc.invoices,
    "order_items": dc.order_items,
    "regions": dc.regions,
    "service_logs": dc.service_logs,
    "shipments": dc.shipments,
    "suppliers": dc.suppliers
}

# ==========================================================
# Dataset Overview
# ==========================================================

# print("=" * 70)
# print("DATASET OVERVIEW")
# print("=" * 70)

# for name, df in datasets.items():

#     print(f"{name:<25} : {df.shape}")

    # ==========================================================
# Numerical Summary
# ==========================================================

# print("=" * 70)
# print("NUMERICAL SUMMARY")
# print("=" * 70)

# for name, df in datasets.items():

#     print(f"\n{name}")
#     print("-" * 40)

#     print(df.describe())


# ==========================================================
# Categorical Summary
# ==========================================================

# print("=" * 70)
# print("CATEGORICAL SUMMARY")
# print("=" * 70)

# for name, df in datasets.items():

#     print(f"\n{name}")
#     print("-" * 40)

#     categorical_columns = df.select_dtypes(
#         include="object"
#     ).columns

#     for column in categorical_columns:

#         print(f"\n{column}")
#         print(df[column].value_counts().head(10))


# print(customers["customer_id"].is_unique)
# print(customers["customer_id"].duplicated().sum())
# print(invoices["invoice_id"].is_unique)
# print(invoices["invoice_id"].duplicated().sum())
# invoice_count_before = len(invoices)

# customer_revenue = pd.merge(
#     customers,
#     invoices,
#     on="customer_id",
#     how="inner"
# )

# invoice_count_after = len(customer_revenue)

# print("Invoices before merge :", invoice_count_before)
# print("Rows after merge      :", invoice_count_after)

# ==========================================================
# BA-01
# KPI: Top Customers by Net Revenue
#
# Business Objective:
# Identify the customers generating the highest net revenue
# for ReLoop Crate Systems.
#
# Business Logic:
# Net Revenue = Subtotal Amount - Refund Amount
#
# Tables Used:
# - invoices
# - customers
#
# Relationship:
# customers (1) ───────< invoices (many)
#
# Join Key:
# customer_id
#
# Analysis Process:
# 1. Calculate Net Revenue at invoice level.
# 2. Merge invoices with customer information.
# 3. Validate the expected one-to-many relationship.
# 4. Aggregate Net Revenue by customer.
# 5. Sort customers from highest to lowest revenue.
# ==========================================================


# ==========================================================
# Step 1: Calculate Net Revenue
# ==========================================================

invoices["Net_Revenue"] = (
    invoices["subtotal_amount"]
    - invoices["refund_amount"]
)


# ==========================================================
# Step 2: Merge Invoices with Customers
# ==========================================================

customer_revenue = pd.merge(
    customers,
    invoices,
    on="customer_id",
    how="inner",
    validate="one_to_many"
)


# ==========================================================
# Step 3: Aggregate Net Revenue by Customer
# ==========================================================

customer_revenue = (
    customer_revenue
    .groupby(
        ["customer_id", "legal_name"],
        as_index=False
    )["Net_Revenue"]
    .sum()
)


# ==========================================================
# Step 4: Rank Customers by Net Revenue
# ==========================================================

top_customers = (
    customer_revenue
    .sort_values(
        "Net_Revenue",
        ascending=False
    )
    .reset_index(drop=True)
)


# ==========================================================
# Step 5: Display Top 10 Customers
# ==========================================================

# print("=" * 70)
# print("BA-01: TOP 10 CUSTOMERS BY NET REVENUE")
# print("=" * 70)

# print(
#     top_customers.head(10)
# )


# ==========================================================
# BA-02
# KPI: Top Crate Models by Net Revenue
#
# Business Objective:
# Identify the crate models generating the highest net
# revenue and measure the number of unique orders associated
# with each crate model.
#
# Business Logic:
#
# Net Revenue =
#     subtotal_amount - refund_amount
#
# Total Orders =
#     Count of distinct order_id
#
# Ranking:
#     Crate models are ranked by Net Revenue in descending
#     order.
#
# SQL Analysis Equivalent:
#     invoices
#         ↓
#     deployment_orders
#         ↓
#     order_items
#         ↓
#     crate_models
#
# Relationships:
#     invoices.order_id
#             ↓
#     deployment_orders.order_id
#
#     deployment_orders.order_id
#             ↓
#     order_items.order_id
#
#     order_items.crate_model_id
#             ↓
#     crate_models.crate_model_id
# ==========================================================


# ==========================================================
# Step 1: Merge Invoices with Deployment Orders
# ==========================================================

deployed_invoices = pd.merge(
    invoices,
    deployment_orders,
    on="order_id",
    how="inner"
)


# ==========================================================
# Step 2: Merge with Order Items
# ==========================================================

deployed_order_item = pd.merge(
    deployed_invoices,
    order_items,
    on="order_id",
    how="inner"
)


# ==========================================================
# Step 3: Merge with Crate Models
# ==========================================================

deployed_crate_model = pd.merge(
    deployed_order_item,
    crate_models,
    on="crate_model_id",
    how="inner"
)


# ==========================================================
# Step 4: Calculate Net Revenue
#
# Net Revenue = Subtotal Amount - Refund Amount
# ==========================================================

deployed_crate_model["Net_Revenue"] = (
    deployed_crate_model["subtotal_amount"]
    - deployed_crate_model["refund_amount"]
)


# ==========================================================
# Step 5: Aggregate Revenue by Crate Model
#
# GROUP BY:
#     crate_model_id
#     model_name
#
# Aggregation:
#     SUM(Net_Revenue)
# ==========================================================

crate_model_revenue = (
    deployed_crate_model
    .groupby(
        ["crate_model_id", "model_name"],
        as_index=False
    )["Net_Revenue"]
    .sum()
)


# ==========================================================
# Step 6: Calculate Total Orders
#
# Business Definition:
# Number of unique orders associated with each crate model.
#
# SQL Equivalent:
# COUNT(DISTINCT order_id)
# ==========================================================

crate_model_orders = (
    deployed_crate_model
    .groupby(
        ["crate_model_id", "model_name"],
        as_index=False
    )["order_id"]
    .nunique()
    .rename(
        columns={"order_id": "Total_Orders"}
    )
)


# ==========================================================
# Step 7: Combine Revenue and Order Metrics
# ==========================================================

crate_model_revenue = pd.merge(
    crate_model_revenue,
    crate_model_orders,
    on=["crate_model_id", "model_name"],
    how="left",
    validate="one_to_one"
)


# ==========================================================
# Step 8: Rank Crate Models by Net Revenue
# ==========================================================

crate_model_revenue["Revenue_Rank"] = (
    crate_model_revenue["Net_Revenue"]
    .rank(
        method="dense",
        ascending=False
    )
    .astype(int)
)


# ==========================================================
# Step 9: Sort by Revenue Rank
# ==========================================================

crate_model_revenue = (
    crate_model_revenue
    .sort_values(
        ["Revenue_Rank", "Net_Revenue"],
        ascending=[True, False]
    )
    .reset_index(drop=True)
)


# ==========================================================
# Step 10: Display Top 10 Crate Models
# ==========================================================

# print("=" * 70)
# print("BA-02: TOP 10 CRATE MODELS BY NET REVENUE")
# print("=" * 70)

# print(
#     crate_model_revenue[
#         [
#             "crate_model_id",
#             "model_name",
#             "Net_Revenue",
#             "Total_Orders",
#             "Revenue_Rank"
#         ]
#     ].head(10)
# )


# ==========================================================
# BA-03
# KPI: Revenue by Customer Region
#
# Business Objective:
# Analyze net revenue generated by customers across regions
# and identify the highest-revenue customer regions.
#
# Business Logic:
#
# Net Revenue = subtotal_amount - refund_amount
#
# Total Customers = distinct customers with invoice records
#
# Revenue Rank = Dense rank based on Net Revenue
#                (highest revenue = Rank 1)
#
# Data Flow:
#
# invoices
#     ↓ customer_id
# customers
#     ↓ home_region_id
# regions
#
# ==========================================================


# ==========================================================
# Step 1: Connect Invoices with Customers
# ==========================================================
#
# Purpose:
# Bring customer information into the invoice dataset so
# that each invoice can be associated with the customer's
# home region.
#
# Join Key:
#     customer_id
#
# Join Type:
#     INNER JOIN
# ==========================================================

invoiced_customer = pd.merge(
    invoices,
    customers,
    on="customer_id",
    how="inner"
)


# ==========================================================
# Step 2: Standardize Region Key
# ==========================================================
#
# customers uses:
#     home_region_id
#
# regions uses:
#     region_id
#
# Rename home_region_id so the two DataFrames can be joined
# using the same key.
# ==========================================================

invoiced_customer = invoiced_customer.rename(
    columns={
        "home_region_id": "region_id"
    }
)


# ==========================================================
# Step 3: Connect Customers with Regions
# ==========================================================
#
# Purpose:
# Add the region name to each customer's invoice records.
#
# Join Key:
#     region_id
# ==========================================================

customer_region = pd.merge(
    invoiced_customer,
    regions,
    on="region_id",
    how="inner"
)


# ==========================================================
# Step 4: Calculate Net Revenue
# ==========================================================
#
# Net Revenue = Subtotal Amount - Refund Amount
# ==========================================================

customer_region["Net_Revenue"] = (
    customer_region["subtotal_amount"]
    - customer_region["refund_amount"]
)


# ==========================================================
# Step 5: Calculate Total Customers by Region
# ==========================================================
#
# A customer can have multiple invoices.
# Therefore, COUNT(*) would incorrectly count invoices.
#
# nunique() counts each customer only once.
#
# SQL Equivalent:
#     COUNT(DISTINCT customer_id)
# ==========================================================

region_customers = (
    customer_region
    .groupby(
        ["region_id"],
        as_index=False
    )["customer_id"]
    .nunique()
)


# ==========================================================
# Step 6: Rename Customer Count
# ==========================================================

region_customers = region_customers.rename(
    columns={
        "customer_id": "Total_Customers"
    }
)


# ==========================================================
# Step 7: Aggregate Net Revenue by Region
# ==========================================================
#
# SQL Equivalent:
#     GROUP BY region_id, region_name
#     SUM(Net_Revenue)
# ==========================================================

top_region_revenue = (
    customer_region
    .groupby(
        ["region_id", "region_name"],
        as_index=False
    )["Net_Revenue"]
    .sum()
    .sort_values(
        "Net_Revenue",
        ascending=False
    )
)


# ==========================================================
# Step 8: Combine Revenue and Customer Metrics
# ==========================================================
#
# region_customers contains:
#     region_id
#     Total_Customers
#
# top_region_revenue contains:
#     region_id
#     region_name
#     Net_Revenue
#
# region_id is the common key.
# ==========================================================

top_region_revenue = pd.merge(
    top_region_revenue,
    region_customers,
    on="region_id",
    how="inner"
)


# ==========================================================
# Step 9: Rank Regions by Net Revenue
# ==========================================================
#
# SQL Equivalent:
#
# DENSE_RANK() OVER (
#     ORDER BY Net_Revenue DESC
# )
#
# Highest revenue = Rank 1
# ==========================================================

top_region_revenue["Revenue_Rank"] = (
    top_region_revenue["Net_Revenue"]
    .rank(
        method="dense",
        ascending=False
    )
    .astype(int)
)


# ==========================================================
# Step 10: Display Top 10 Regions
# ==========================================================

# print("=" * 70)
# print("BA-03: REVENUE BY CUSTOMER REGION")
# print("=" * 70)

# print(
#     top_region_revenue.head(10)
# )


# ==========================================================
# BA-04: MONTHLY REVENUE TREND
#
# Business Objective:
# Analyze monthly net revenue trends and calculate
# Month-over-Month (MoM) revenue growth.
# ==========================================================


# ----------------------------------------------------------
# Step 1: Filter Paid Invoices
# ----------------------------------------------------------

paid_invoices = invoices[
    invoices["invoice_status"] == "Paid"
].copy()


# ----------------------------------------------------------
# Step 2: Calculate Net Revenue
# Net Revenue = Subtotal - Refund
# ----------------------------------------------------------

paid_invoices["Net_Revenue"] = (
    paid_invoices["subtotal_amount"]
    - paid_invoices["refund_amount"]
)


# ----------------------------------------------------------
# Step 3: Extract Year and Month
# ----------------------------------------------------------

paid_invoices["Year"] = (
    paid_invoices["invoice_date"].dt.year
)

paid_invoices["Month_No"] = (
    paid_invoices["invoice_date"].dt.month
)


# ----------------------------------------------------------
# Step 4: Calculate Monthly Revenue
# ----------------------------------------------------------

monthly_revenue = (
    paid_invoices
    .groupby(
        ["Year", "Month_No"],
        as_index=False
    )["Net_Revenue"]
    .sum()
    .sort_values(
        ["Year", "Month_No"]
    )
    .rename(
        columns={
            "Net_Revenue": "Monthly_Revenue"
        }
    )
)


# ----------------------------------------------------------
# Step 5: Get Previous Month Revenue
# ----------------------------------------------------------

monthly_revenue["Previous_Month_Revenue"] = (
    monthly_revenue["Monthly_Revenue"].shift(1)
)


# ----------------------------------------------------------
# Step 6: Calculate MoM Growth
# ----------------------------------------------------------

monthly_revenue["MoM_Growth_%"] = (
    (
        monthly_revenue["Monthly_Revenue"]
        - monthly_revenue["Previous_Month_Revenue"]
    )
    / monthly_revenue["Previous_Month_Revenue"]
) * 100


# ----------------------------------------------------------
# Output
# ----------------------------------------------------------

# print("=" * 70)
# print("BA-04: MONTHLY REVENUE TREND")
# print("=" * 70)

# print(monthly_revenue.head(12));

# ============================================================
# BA-05: LOYAL REPEAT CUSTOMERS
# ============================================================

# ------------------------------------------------------------
# 1. Build deployment-order/customer base
# ------------------------------------------------------------

deployment_contracts = pd.merge(
    deployment_orders,
    contracts[["contract_id", "customer_id"]].rename(
        columns={"customer_id": "contract_customer_id"}
    ),
    on="contract_id",
    how="inner"
)

# Remove the customer_id coming from deployment_orders
deployment_contracts = deployment_contracts.drop(
    columns=["customer_id"]
)

# Rename the contract-based customer ID
deployment_contracts = deployment_contracts.rename(
    columns={"contract_customer_id": "customer_id"}
)

# Attach customer name
deployment_customer = pd.merge(
    deployment_contracts,
    customers[["customer_id", "legal_name"]],
    on="customer_id",
    how="inner"
)


# ------------------------------------------------------------
# 2. Total Orders per Customer
# ------------------------------------------------------------

customer_orders = (
    deployment_customer
    .groupby("customer_id")["order_id"]
    .nunique()
    .reset_index(name="Total_Orders")
)


# ------------------------------------------------------------
# 3. Total Contracts per Customer
# ------------------------------------------------------------

customer_contracts = (
    deployment_customer
    .groupby("customer_id")["contract_id"]
    .nunique()
    .reset_index(name="Total_Contracts")
)


# ------------------------------------------------------------
# 4. Build Invoice/Customer Dataset
# ------------------------------------------------------------

customer_invoices = pd.merge(
    deployment_customer[
        ["order_id", "customer_id", "legal_name"]
    ],
    invoices[
        [
            "order_id",
            "invoice_id",
            "subtotal_amount",
            "refund_amount"
        ]
    ],
    on="order_id",
    how="left"
)


# ------------------------------------------------------------
# 5. Calculate Net Revenue
# ------------------------------------------------------------

customer_invoices["Net_Revenue"] = (
    customer_invoices["subtotal_amount"]
    - customer_invoices["refund_amount"]
)

customer_revenue = (
    customer_invoices
    .groupby("customer_id")["Net_Revenue"]
    .sum()
    .reset_index(name="Net_Revenue")
)


# ------------------------------------------------------------
# 6. Combine Customer Metrics
# ------------------------------------------------------------

customer_summary = pd.merge(
    customer_orders,
    customer_contracts,
    on="customer_id",
    how="inner"
)

customer_summary = pd.merge(
    customer_summary,
    customer_revenue,
    on="customer_id",
    how="left"
)


# ------------------------------------------------------------
# 7. Add Customer Name
# ------------------------------------------------------------

customer_summary = pd.merge(
    customer_summary,
    customers[["customer_id", "legal_name"]],
    on="customer_id",
    how="inner"
)


# ------------------------------------------------------------
# 8. Handle Customers Without Invoices
# ------------------------------------------------------------

customer_summary["Net_Revenue"] = (
    customer_summary["Net_Revenue"]
    .fillna(0)
)


# ------------------------------------------------------------
# 9. Repeat Customer Classification
# ------------------------------------------------------------

customer_summary["Repeat_Customer"] = np.where(
    customer_summary["Total_Orders"] >= 10,
    "Yes",
    "No"
)


# ------------------------------------------------------------
# 10. Loyalty Rank
# ------------------------------------------------------------

customer_summary["Loyalty_Rank"] = (
    customer_summary["Total_Orders"]
    .rank(
        method="dense",
        ascending=False
    )
    .astype(int)
)


# ------------------------------------------------------------
# 11. Final Sorting and Column Order
# ------------------------------------------------------------

customer_summary = (
    customer_summary
    .sort_values("Loyalty_Rank")
    .reset_index(drop=True)
)

customer_summary = customer_summary[
    [
        "customer_id",
        "legal_name",
        "Total_Orders",
        "Total_Contracts",
        "Net_Revenue",
        "Repeat_Customer",
        "Loyalty_Rank"
    ]
]


# ------------------------------------------------------------
# 12. Final Output
# ------------------------------------------------------------

# print(customer_summary.head(10))

# ============================================================
# BA-06: SHIPMENT DELAY ANALYSIS
# ============================================================
#
# Business Objective:
# Identify shipments delivered late by calculating the number
# of days between dispatch and actual arrival.
#
# Business Rule:
#   Transit Days > 7  -> Late
#   Transit Days <= 7 -> On Time
#
# Shipments with no actual arrival date are excluded because
# their completed transit time cannot be calculated.
# ============================================================


# ------------------------------------------------------------
# 1. Filter Completed Shipments
# ------------------------------------------------------------
# Keep only shipments that have an actual arrival date.
# This is equivalent to:
#
# WHERE actual_arrival_date IS NOT NULL
# ------------------------------------------------------------

shipment_analysis = shipments[
    shipments["actual_arrival_date"].notna()
].copy()


# ------------------------------------------------------------
# 2. Attach Origin Region
# ------------------------------------------------------------
# The shipments table contains origin_region_id.
# Join it with regions to obtain the human-readable
# origin region name.
#
# The region columns are renamed before merging to avoid
# ambiguity because the regions table will be used twice.
# ------------------------------------------------------------

origin_region = pd.merge(
    shipment_analysis,
    regions[
        ["region_name", "region_id"]
    ].rename(
        columns={
            "region_name": "Origin_Region",
            "region_id": "origin_region_id"
        }
    ),
    on="origin_region_id",
    how="inner"
)


# Rename the origin key for consistency.
origin_region = origin_region.rename(
    columns={
        "origin_region_id": "region_id"
    }
)


# ------------------------------------------------------------
# 3. Attach Destination Region
# ------------------------------------------------------------
# The shipments table also contains destination_region_id.
# Join it with regions again to obtain the destination
# region name.
# ------------------------------------------------------------

destination_region = pd.merge(
    shipments,
    regions[
        ["region_name", "region_id"]
    ].rename(
        columns={
            "region_name": "Destination_Region",
            "region_id": "destination_region_id"
        }
    ),
    on="destination_region_id",
    how="inner"
)


# Rename the destination key for consistency.
destination_region = destination_region.rename(
    columns={
        "destination_region_id": "region_id"
    }
)


# ------------------------------------------------------------
# 4. Combine Origin and Destination Information
# ------------------------------------------------------------
# Combine the two region-enriched datasets using shipment_id.
#
# Each row represents one shipment.
# ------------------------------------------------------------

shipment_details = pd.merge(
    origin_region[
        [
            "shipment_id",
            "shipment_number",
            "Origin_Region",
            "dispatch_date"
        ]
    ],
    destination_region[
        [
            "shipment_id",
            "Destination_Region",
            "actual_arrival_date"
        ]
    ],
    on="shipment_id",
    how="inner"
)


# ------------------------------------------------------------
# 5. Calculate Transit Days
# ------------------------------------------------------------
# Transit Days = Actual Arrival Date - Dispatch Date
#
# Date subtraction returns a Pandas Timedelta.
# .dt.days extracts the number of days from that Timedelta.
# ------------------------------------------------------------

shipment_details["Transit_Days"] = (
    shipment_details["actual_arrival_date"]
    - shipment_details["dispatch_date"]
).dt.days


# ------------------------------------------------------------
# 6. Classify Shipment Delivery Status
# ------------------------------------------------------------
# Business rule:
#
# Transit Days > 7  -> Late
# Otherwise         -> On Time
#
# This reproduces the SQL CASE expression.
# ------------------------------------------------------------

shipment_details["Delivery_Status"] = np.where(
    shipment_details["Transit_Days"] > 7,
    "Late",
    "On Time"
)


# ------------------------------------------------------------
# 7. Select Final KPI Columns
# ------------------------------------------------------------

shipment_details = shipment_details[
    [
        "shipment_number",
        "Origin_Region",
        "Destination_Region",
        "dispatch_date",
        "actual_arrival_date",
        "Transit_Days",
        "Delivery_Status"
    ]
]


# ------------------------------------------------------------
# 8. Display Result
# ------------------------------------------------------------

# print(shipment_details.head(5))

# ============================================================
# BA-08: CUSTOMER SEGMENTATION
# ============================================================
#
# Business Objective:
# Segment customers based on their total Net Revenue.
#
# The KPI calculates:
#   1. Customer Name
#   2. Total Orders
#   3. Net Revenue
#   4. Customer Revenue Rank
#   5. Revenue Band
#
# Revenue Band Rules:
#   Net Revenue >= 500,000 -> Platinum
#   Net Revenue >= 300,000 -> Gold
#   Net Revenue >= 100,000 -> Silver
#   Otherwise              -> Bronze
#
# Customer Rank:
#   Customers are ranked by Net Revenue in descending order.
#   DENSE ranking is used, matching the SQL logic.
#
# Grain:
#   1 row = 1 customer
# ============================================================


# ------------------------------------------------------------
# 1. Connect Deployment Orders to Contracts
# ------------------------------------------------------------
# deployment_orders contains the order and contract relationship.
#
# contracts contains the customer associated with each contract.
#
# Therefore, contract_id is used to identify which customer
# placed each deployment order.
# ------------------------------------------------------------

deployed_contracts = pd.merge(
    deployment_orders[
        ["order_id", "contract_id"]
    ],
    contracts[
        ["contract_id", "customer_id"]
    ],
    on="contract_id",
    how="inner"
)


# ------------------------------------------------------------
# 2. Attach Customer Information
# ------------------------------------------------------------
# Add the customer's legal name using customer_id.
# ------------------------------------------------------------

customer_orders = pd.merge(
    deployed_contracts[
        ["order_id", "contract_id", "customer_id"]
    ],
    customers[
        ["customer_id", "legal_name"]
    ],
    on="customer_id",
    how="inner"
)


# ------------------------------------------------------------
# 3. Attach Invoice Information
# ------------------------------------------------------------
# Join invoices using order_id.
#
# We need:
#   subtotal_amount
#   refund_amount
#
# These will be used to calculate Net Revenue.
# ------------------------------------------------------------

customer_transactions = pd.merge(
    customer_orders,
    invoices[
        [
            "invoice_id",
            "order_id",
            "subtotal_amount",
            "refund_amount"
        ]
    ],
    on="order_id",
    how="inner"
)


# ------------------------------------------------------------
# 4. Calculate Transaction-Level Net Revenue
# ------------------------------------------------------------
# Net Revenue = Subtotal Amount - Refund Amount
#
# At this point the DataFrame is still transaction/order level.
# ------------------------------------------------------------

customer_transactions["Net_Revenue"] = (
    customer_transactions["subtotal_amount"]
    - customer_transactions["refund_amount"]
)


# ------------------------------------------------------------
# 5. Create Customer-Level Summary
# ------------------------------------------------------------
# Convert the transaction-level data into customer-level data.
#
# Grain after this step:
#   1 row = 1 customer
#
# Total Orders:
#   COUNT(DISTINCT order_id)
#
# Net Revenue:
#   SUM(Net_Revenue)
# ------------------------------------------------------------

customer_summary = (
    customer_transactions
    .groupby(
        ["customer_id", "legal_name"],
        as_index=False
    )
    .agg(
        Total_Orders=("order_id", "nunique"),
        Net_Revenue=("Net_Revenue", "sum")
    )
)


# ------------------------------------------------------------
# 6. Rank Customers by Net Revenue
# ------------------------------------------------------------
# Highest revenue customer receives Rank 1.
#
# method="dense" reproduces:
#
# DENSE_RANK() OVER(ORDER BY Net_Revenue DESC)
# ------------------------------------------------------------

customer_summary["Customer_Rank"] = (
    customer_summary["Net_Revenue"]
    .rank(
        method="dense",
        ascending=False
    )
    .astype(int)
)


# ------------------------------------------------------------
# 7. Assign Revenue Band
# ------------------------------------------------------------
# Segment customers according to their total Net Revenue.
#
# Conditions are checked from the highest threshold to the
# lowest threshold.
# ------------------------------------------------------------

customer_summary["Revenue_Band"] = np.where(
    customer_summary["Net_Revenue"] >= 500000,
    "Platinum",
    np.where(
        customer_summary["Net_Revenue"] >= 300000,
        "Gold",
        np.where(
            customer_summary["Net_Revenue"] >= 100000,
            "Silver",
            "Bronze"
        )
    )
)


# ------------------------------------------------------------
# 8. Sort Customers by Revenue Rank
# ------------------------------------------------------------

customer_summary = (
    customer_summary
    .sort_values(
        "Customer_Rank",
        ascending=True
    )
    .reset_index(drop=True)
)


# ------------------------------------------------------------
# 9. Arrange Final Output Columns
# ------------------------------------------------------------

customer_summary = customer_summary[
    [
        "customer_id",
        "legal_name",
        "Total_Orders",
        "Net_Revenue",
        "Customer_Rank",
        "Revenue_Band"
    ]
]


# ------------------------------------------------------------
# 10. Display Result
# ------------------------------------------------------------

print(customer_summary.head(10))


# ============================================================
# Ticket ID: BA-09
# KPI: Average Rental Days by Crate Model
# ============================================================
#
# Business Objective:
# Identify which crate models stay longest with customers.
#
# Final Output:
#   - Model_Name
#   - Average_Rental_Days
#   - Total_Orders
#   - Rental_Rank
#
# Business Logic:
#
#   Average_Rental_Days:
#       Average of daily_rental_days for each crate model.
#
#   Total_Orders:
#       Number of distinct orders using the crate model.
#
#   Rental_Rank:
#       Dense rank based on Average_Rental_Days in descending
#       order. The model with the highest average rental days
#       receives Rank 1.
#
# Final Grain:
#   1 row = 1 crate model
# ============================================================


# ------------------------------------------------------------
# 1. Join Order Items with Crate Models
# ------------------------------------------------------------
#
# order_items contains:
#   - order_id
#   - crate_model_id
#   - daily_rental_days
#
# crate_models contains:
#   - crate_model_id
#   - model_name
#
# crate_model_id is used to connect the two tables.
#
# After this merge, each order item has the corresponding
# crate model name.
# ------------------------------------------------------------

crate_order = pd.merge(
    order_items[
        [
            "order_item_id",
            "order_id",
            "crate_model_id",
            "daily_rental_days"
        ]
    ],
    crate_models[
        [
            "crate_model_id",
            "model_name"
        ]
    ],
    on="crate_model_id",
    how="inner"
)


# ------------------------------------------------------------
# 2. Calculate Average Rental Days and Total Orders
# ------------------------------------------------------------
#
# SQL equivalent:
#
#   GROUP BY
#       cm.crate_model_id,
#       cm.model_name
#
#   AVG(oi.daily_rental_days)
#   COUNT(DISTINCT oi.order_id)
#
# We group by both crate_model_id and model_name because both
# columns identify the crate model in the SQL query.
#
# After this step:
#
#   1 row = 1 crate model
# ------------------------------------------------------------

average_rental_days = (
    crate_order
    .groupby(
        [
            "crate_model_id",
            "model_name"
        ],
        as_index=False
    )
    .agg(
        Total_Orders=("order_id", "nunique"),
        Average_Rental_Days=("daily_rental_days", "mean")
    )
)


# ------------------------------------------------------------
# 3. Round Average Rental Days
# ------------------------------------------------------------
#
# SQL equivalent:
#
#   ROUND(AVG(oi.daily_rental_days), 2)
#
# Pandas .mean() can return many decimal places, so we round
# the result to 2 decimal places to match the SQL output.
# ------------------------------------------------------------

average_rental_days["Average_Rental_Days"] = (
    average_rental_days["Average_Rental_Days"]
    .round(2)
)


# ------------------------------------------------------------
# 4. Rank Crate Models
# ------------------------------------------------------------
#
# SQL equivalent:
#
#   DENSE_RANK() OVER(
#       ORDER BY Average_Rental_Days DESC
#   )
#
# Highest average rental duration receives Rank 1.
#
# method="dense" ensures that tied values receive the same rank
# without creating gaps in the ranking sequence.
# ------------------------------------------------------------

average_rental_days["Rental_Rank"] = (
    average_rental_days["Average_Rental_Days"]
    .rank(
        method="dense",
        ascending=False
    )
    .astype(int)
)


# ------------------------------------------------------------
# 5. Sort by Rental Rank
# ------------------------------------------------------------
#
# The business objective is to identify the crate models that
# stay longest with customers.
#
# Therefore, Rank 1 should appear first.
# ------------------------------------------------------------

average_rental_days = (
    average_rental_days
    .sort_values("Rental_Rank")
    .reset_index(drop=True)
)


# ------------------------------------------------------------
# 6. Select Final Output Columns
# ------------------------------------------------------------
#
# crate_model_id was useful during the calculation but is not
# required in the final business output.
# ------------------------------------------------------------

average_rental_days = average_rental_days[
    [
        "model_name",
        "Average_Rental_Days",
        "Total_Orders",
        "Rental_Rank"
    ]
]


# ------------------------------------------------------------
# 7. Display Final Result
# ------------------------------------------------------------

# print(average_rental_days.head(10))

# ==========================================================
# Ticket ID: BA-11
# KPI: Revenue by Contract Tier
#
# Business Objective:
# Identify which contract tiers generate the highest revenue
# to support sales strategy and contract planning.
#
# SQL Equivalent:
#   - Net Revenue
#   - Total Contracts
#   - Total Customers
#   - Average Contract Revenue
#   - Tier Rank
#   - Revenue Contribution %
#
# Final Grain:
#   1 row = 1 Contract Tier
# ==========================================================


# ----------------------------------------------------------
# STEP 1: Combine Contracts with Invoices
#
# contracts contains:
#   contract_id
#   contract_tier
#
# invoices contains:
#   contract_id
#   customer_id
#   subtotal_amount
#   refund_amount
#
# contract_id is used because each invoice belongs to a
# contract, and the contract determines its contract tier.
# ----------------------------------------------------------

contract_details = pd.merge(
    contracts[
        [
            "contract_id",
            "contract_tier"
        ]
    ],

    invoices[
        [
            "contract_id",
            "customer_id",
            "subtotal_amount",
            "refund_amount"
        ]
    ],

    on="contract_id",
    how="inner"
)


# ----------------------------------------------------------
# STEP 2: Calculate Net Revenue
#
# Net Revenue = Subtotal Amount - Refund Amount
#
# This calculation is performed at the invoice level
# before aggregating revenue by contract tier.
# ----------------------------------------------------------

contract_details["Net_Revenue"] = (
    contract_details["subtotal_amount"]
    - contract_details["refund_amount"]
)


# ----------------------------------------------------------
# STEP 3: Aggregate Data by Contract Tier
#
# Final grain after this step:
#   1 row = 1 Contract Tier
#
# Total_Contracts:
#   Number of unique contracts in each tier.
#
# Total_Customers:
#   Number of unique customers associated with each tier.
#
# Net_Revenue:
#   Total net revenue generated by each tier.
# ----------------------------------------------------------

contract_details = (
    contract_details
    .groupby(
        "contract_tier",
        as_index=False
    )
    .agg(
        Total_Contracts=(
            "contract_id",
            "nunique"
        ),

        Total_Customers=(
            "customer_id",
            "nunique"
        ),

        Net_Revenue=(
            "Net_Revenue",
            "sum"
        )
    )
)


# ----------------------------------------------------------
# STEP 4: Calculate Average Contract Revenue
#
# Business Definition:
#
# Average Contract Revenue =
#       Net Revenue / Total Contracts
#
# Important:
# This is NOT the average invoice revenue.
# It represents the average revenue generated per
# contract within each contract tier.
# ----------------------------------------------------------

contract_details["Average_Contract_Revenue"] = (
    contract_details["Net_Revenue"]
    / contract_details["Total_Contracts"]
).round(2)


# ----------------------------------------------------------
# STEP 5: Rank Contract Tiers by Net Revenue
#
# Equivalent SQL:
#
# DENSE_RANK() OVER (
#     ORDER BY Net_Revenue DESC
# )
#
# The tier with the highest revenue receives Rank 1.
# ----------------------------------------------------------

contract_details["Tier_Rank"] = (
    contract_details["Net_Revenue"]
    .rank(
        method="dense",
        ascending=False
    )
    .astype(int)
)


# ----------------------------------------------------------
# STEP 6: Calculate Total Revenue Across All Tiers
#
# This represents the denominator used for calculating
# each contract tier's contribution to total company revenue.
#
# Equivalent concept in SQL:
#
# SUM(Net_Revenue) OVER()
# ----------------------------------------------------------

total_revenue = contract_details["Net_Revenue"].sum()


# ----------------------------------------------------------
# STEP 7: Calculate Revenue Contribution Percentage
#
# Revenue Contribution % =
#
#       Tier Net Revenue
#       ---------------- × 100
#       Total Net Revenue
#
# This tells us what percentage of total revenue is
# generated by each contract tier.
# ----------------------------------------------------------

contract_details["Revenue_Contribution_Pct"] = (
    contract_details["Net_Revenue"]
    / total_revenue
    * 100
).round(2)


# ----------------------------------------------------------
# STEP 8: Sort Contract Tiers by Revenue Rank
#
# Highest-revenue contract tier appears first.
# ----------------------------------------------------------

contract_details = (
    contract_details
    .sort_values(
        "Tier_Rank",
        ascending=True
    )
)


# ----------------------------------------------------------
# STEP 9: Select Final KPI Columns
#
# Keep only the business-facing columns required for
# the final analysis.
# ----------------------------------------------------------

contract_details = contract_details[
    [
        "contract_tier",
        "Net_Revenue",
        "Total_Contracts",
        "Total_Customers",
        "Average_Contract_Revenue",
        "Tier_Rank",
        "Revenue_Contribution_Pct"
    ]
]


# ----------------------------------------------------------
# STEP 10: Display Final Result
# ----------------------------------------------------------

# print(contract_details.head(10))

supplier_details = pd.merge(
    suppliers[["supplier_id","supplier_name", "quality_rating"]],
    shipments[["shipment_id", "carrier_supplier_id", "freight_cost"]].rename(
        columns={"carrier_supplier_id": "supplier_id"}
    ),
    on="supplier_id",
    how="inner"    
)

supplier_details["quality_rating"] = supplier_details["quality_rating"].fillna(0)

supplier_details = (
    supplier_details
    .groupby(["supplier_id", "supplier_name"],as_index=False)
    .agg(
        Total_Shipments=("shipment_id", "nunique"),
        Average_Freight_Cost=("freight_cost", "mean"),
        Quality_Rating=("quality_rating", "first")
    )
)
supplier_details["Average_Freight_Cost"] = (
    supplier_details["Average_Freight_Cost"].round(2)
)

ranking_keys = (
    supplier_details[
        ["Quality_Rating", "Average_Freight_Cost"]
    ]
    .drop_duplicates()
)

ranking_keys = ranking_keys.sort_values(
    ["Quality_Rating", "Average_Freight_Cost"],
    ascending=[False, True]
)

ranking_keys["Supplier_Rank"] = range(
    1,
    len(ranking_keys) + 1
)

supplier_details = pd.merge(
    supplier_details,
    ranking_keys,
    on=["Quality_Rating", "Average_Freight_Cost"],
    how="left"
)


supplier_details = (
    supplier_details
    .sort_values(
    ["Quality_Rating", "Average_Freight_Cost"],
    ascending=[False, True]
)
)

# print(
#     supplier_details[
#         [
#             "supplier_id",
#             "supplier_name",
#             "Quality_Rating",
#             "Total_Shipments",
#             "Average_Freight_Cost",
#             "Supplier_Rank"
#         ]
#     ].head(20)
# )

# ==========================================================
# Ticket ID: BA-13
# KPI: Deployment Trend Analysis
#
# Business Objective:
# Analyze monthly deployment trends to identify business
# growth and operational demand using Month-over-Month (MoM)
# deployment growth.
#
# SQL Concepts Translated:
# - YEAR() / MONTH() / MONTHNAME()
# - GROUP BY
# - COUNT()
# - LAG()
# - MoM Growth Calculation
# - ROUND()
# - ORDER BY
# ==========================================================


# ----------------------------------------------------------
# STEP 1: Create a KPI-specific copy
# ----------------------------------------------------------
# We create a copy so that the original deployment_orders
# DataFrame remains unchanged.
#
# This is a good practice when building multiple KPIs from
# the same source DataFrame.

deployment_trend = deployment_orders.copy()


# ----------------------------------------------------------
# STEP 2: Select the columns required for this KPI
# ----------------------------------------------------------
# We only need:
#
# order_date  -> Used to determine Year and Month
# order_id    -> Used to count deployments

deployment_summary = (
    deployment_trend[
        [
            "order_date",
            "order_id"
        ]
    ]
    .copy()
)


# ----------------------------------------------------------
# STEP 3: Extract Year, Month Number and Month Name
# ----------------------------------------------------------
# SQL equivalent:
#
# YEAR(order_date)
# MONTH(order_date)
# MONTHNAME(order_date)
#
# Month_No is important because it allows us to maintain
# chronological month order.

deployment_summary["Year"] = (
    deployment_summary["order_date"].dt.year
)

deployment_summary["Month_No"] = (
    deployment_summary["order_date"].dt.month
)

deployment_summary["Month_Name"] = (
    deployment_summary["order_date"].dt.month_name()
)


# ----------------------------------------------------------
# STEP 4: Calculate Monthly Deployments
# ----------------------------------------------------------
# SQL equivalent:
#
# COUNT(order_id)
# GROUP BY Year, Month_No, Month_Name
#
# count() is used rather than nunique() because the SQL query
# uses COUNT(order_id), NOT COUNT(DISTINCT order_id).

deployment_summary = (
    deployment_summary
    .groupby(
        [
            "Year",
            "Month_No",
            "Month_Name"
        ],
        as_index=False
    )
    .agg(
        Total_Deployments=(
            "order_id",
            "count"
        )
    )
)


# ----------------------------------------------------------
# STEP 5: Sort Chronologically
# ----------------------------------------------------------
# We must sort by:
#
# Year     -> ascending
# Month_No -> ascending
#
# This is especially important because the next step uses
# shift(), which depends on the order of the rows.
#
# Without this sorting, "previous row" may not represent
# "previous month".

deployment_summary = (
    deployment_summary
    .sort_values(
        [
            "Year",
            "Month_No"
        ],
        ascending=[
            True,
            True
        ]
    )
    .reset_index(drop=True)
)


# ----------------------------------------------------------
# STEP 6: Calculate Previous Month's Deployments
# ----------------------------------------------------------
# SQL equivalent:
#
# LAG(Total_Deployments)
# OVER(ORDER BY Year, Month_No)
#
# Pandas equivalent:
#
# shift(1)
#
# shift(1) moves the value from the previous row into the
# current row.
#
# Therefore:
#
# January  -> NaN
# February -> January's deployments
# March    -> February's deployments
# etc.

deployment_summary["Previous_Month_Deployment"] = (
    deployment_summary["Total_Deployments"]
    .shift(1)
)


# ----------------------------------------------------------
# STEP 7: Calculate Month-over-Month Growth
# ----------------------------------------------------------
# Formula:
#
#       Current Month - Previous Month
#       -------------------------------- × 100
#              Previous Month
#
# SQL equivalent:
#
# (
#   (Total_Deployments - Previous_Month_Deployment)
#   / Previous_Month_Deployment
# ) * 100
#
# The first month will have NaN because there is no previous
# month available for comparison.

deployment_summary["Growth_%"] = (
    (
        deployment_summary["Total_Deployments"]
        - deployment_summary["Previous_Month_Deployment"]
    )
    / deployment_summary["Previous_Month_Deployment"]
) * 100


# ----------------------------------------------------------
# STEP 8: Round MoM Growth
# ----------------------------------------------------------
# SQL uses ROUND(..., 2), so we round the growth percentage
# to two decimal places.

deployment_summary["Growth_%"] = (
    deployment_summary["Growth_%"].round(2)
)


# ----------------------------------------------------------
# STEP 9: Select Final KPI Columns
# ----------------------------------------------------------
# Keep only the columns required in the final output.

deployment_summary = deployment_summary[
    [
        "Year",
        "Month_No",
        "Month_Name",
        "Total_Deployments",
        "Previous_Month_Deployment",
        "Growth_%"
    ]
]


# ----------------------------------------------------------
# STEP 10: Display Final Result
# # ----------------------------------------------------------

# print(deployment_summary.head(20)) 