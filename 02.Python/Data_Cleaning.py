# ==========================================================
# Portfolio Project #2
# ReLoop Crate Systems
#
# File: 02_Data_Cleaning.py
# Author: Ashish Koge
#
# Objective:
# Perform data quality assessment, validate data types,
# investigate missing values, and prepare the dataset
# for business analysis.
# ==========================================================

# ==========================================================
# Import Data
import os
import pandas as pd
import Data_Loading as dl
# ==========================================================


customers = dl.customers
contracts = dl.contracts
crate_models = dl.crate_models
customer_addresses = dl.customer_addresses
deployment_orders = dl.deployment_orders
employees = dl.employees
invoices = dl.invoices
order_items = dl.order_items
regions = dl.regions
service_logs = dl.service_logs
shipments = dl.shipments
suppliers = dl.suppliers

# ==========================================================
# Dataset Dictionary
# ==========================================================

datasets = {
    "customers": customers,
    "contracts": contracts,
    "crate_Models": crate_models,
    "customer_addresses": customer_addresses,
    "deployment_orders": deployment_orders,
    "employees": employees,
    "invoices": invoices,
    "order_items": order_items,
    "regions": regions,
    "service_logs": service_logs,
    "shipments": shipments,
    "suppliers": suppliers
}

# ==========================================================
# Date Columns
# ==========================================================

date_columns = {
    "customers"         : ["registered_on"],
    "contracts"         : ["start_date"],
    "customer_addresses": ["validated_on"],
    "deployment_orders" : ["order_date","requested_delivery_date_raw"],
    "invoices"          : ["invoice_date","due_date","paid_date"],
    "service_logs"      : ["service_date"],
    "shipments"         : ["dispatch_date","scheduled_arrival_date","actual_arrival_date"]
               }

# ==========================================================
# Date Conversion
# ==========================================================

for dataset_name, columns in date_columns.items():

    # Get the actual DataFrame from the datasets dictionary
    df = datasets[dataset_name]

    # Convert every date column in that DataFrame
    for column in columns:

        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

# ==========================================================
# Categorical Standardization
# ==========================================================

contracts["contract_tier"] = (
    contracts["contract_tier"]
    .str.strip()
    .str.upper()
)



if __name__ == "__main__":

    # ==========================================================
    # Data Quality Report
    # ==========================================================
    # Shape Validation
    # ==========================================================
    print("=" * 70)
    print("DATASET SHAPE SUMMARY")
    print("=" * 70)

    for name, df in datasets.items():
        print(f"{name:<22} : {df.shape}")

    # ==========================================================
    # Data Type Validation (info)
    # ==========================================================

    print("=" * 70)
    print("DATA TYPE SUMMARY")
    print("=" * 70)

    for name, df in datasets.items():
       print(f"\n{name}")
       print("-" * 40)
       df.info()
 
    # ==========================================================
    # Date Conversion Verification
    # ==========================================================

    print("=" * 70)
    print("DATE CONVERSION SUMMARY")
    print("=" * 70)

    for dataset_name, columns in date_columns.items():
       df = datasets[dataset_name]
       print(f"\n{dataset_name}")
       for column in columns:
         print(f"✓ {column:<25} : {df[column].dtype}")

    #==========================================================
    # Missing Value Investigation
 
    # Pandas Concept:
    # DataFrame.isnull().sum()
    #
    # SQL Equivalent:
    # COUNT(*) WHERE column IS NULL 
    #
    # Purpose:
    # Identify missing values in each DataFrame before deciding
    # whether cleaning is required.
    # ==========================================================

    print("=" * 70)
    print("MISSING VALUE SUMMARY")
    print("=" * 70)

    for name, df in datasets.items():

       missing = df.isnull().sum()

       missing = missing[missing > 0]

       print(f"\n{name}")
       print("-" * 40)

       if missing.empty:
          print("✓ No Missing Values")

       else:
          print(missing)


    # ==========================================================
    # Duplicate Check
    #
    # Pandas Concept:
    # DataFrame.duplicated().sum()
    #
    # SQL Equivalent:
    # GROUP BY all columns HAVING COUNT(*) > 1
    #
    # Purpose:
    # Identify duplicate records that may affect KPI accuracy.
    # ==========================================================

    print("=" * 70) 
    print("DUPLICATE SUMMARY")
    print("=" * 70)

    for name, df in datasets.items():

       duplicate_count = df.duplicated().sum()

       print(f"{name:<25} : {duplicate_count}")


    # ==========================================================
    # Business Cleaning Decisions
    # ==========================================================
    #print("=" * 70)
    print("BUSINESS CLEANING DECISIONS")
    print("=" * 70)

    print("""
     1. Date Columns
        Converted all business date columns to datetime.
        Excluded 'end_date_raw' because it contains mixed
        date formats and represents raw imported data rather
        than a standardized business field.
 
     2. Missing Values
      - Missing values were investigated.
      - Business-optional fields (email, phone, tax ID,
        cancellation reason, inspection notes, etc.) were
        retained because they do not affect the planned KPIs.

     3. Duplicate Records
      - No duplicate rows were found in any dataset.

     4. Data Quality Status
      - Dataset is considered suitable for exploratory data
        analysis (EDA) and KPI development.
     """)
       

