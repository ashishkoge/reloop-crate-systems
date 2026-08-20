# ==========================================================
# Portfolio Project #2
# ReLoop Crate Systems
#
# File: 01_Data_Loading.py
# Author: Ashish Koge
#
# Objective:
# Load all CSV files into Pandas DataFrames using
# relative file paths.
# ==========================================================

# ==========================================================
# Import Libraries
# ==========================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Project Directory
# ==========================================================
# Current Script Directory
CURRENT_DIR = os.path.dirname(__file__)

# # Project Root Directory
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

# CSV Folder
DATA_DIR = os.path.join(PROJECT_DIR, "csv")

# ==========================================================
# Load Dataset
# ==========================================================

customers = pd.read_csv(os.path.join(DATA_DIR,"customers.csv"))
contracts = pd.read_csv(os.path.join(DATA_DIR,"contracts.csv"))
crate_models = pd.read_csv(os.path.join(DATA_DIR,"crate_models.csv"))
customer_addresses = pd.read_csv(os.path.join(DATA_DIR,"customer_addresses.csv"))
deployment_orders = pd.read_csv(os.path.join(DATA_DIR,"deployment_orders.csv"))
employees = pd.read_csv(os.path.join(DATA_DIR,"employees.csv"))
invoices = pd.read_csv(os.path.join(DATA_DIR,"invoices.csv"))
order_items = pd.read_csv(os.path.join(DATA_DIR,"order_items.csv"))
regions = pd.read_csv(os.path.join(DATA_DIR,"regions.csv"))
service_logs = pd.read_csv(os.path.join(DATA_DIR,"service_logs.csv"))
shipments = pd.read_csv(os.path.join(DATA_DIR,"shipments.csv"))
suppliers = pd.read_csv(os.path.join(DATA_DIR,"suppliers.csv"))

# ==========================================================

# Verification
# ==========================================================

# if __name__ == "__main__":
#     print(f"Customers            : {customers.shape}")
#     print(f"Contracts            : {contracts.shape}")
#     print(f"Crate Models         : {crate_models.shape}")
#     print(f"Customer Addresses   : {customer_addresses.shape}")
#     print(f"Deployment Orders    : {deployment_orders.shape}")
#     print(f"Employees            : {employees.shape}")
#     print(f"Invoices             : {invoices.shape}")
#     print(f"Order Items          : {order_items.shape}")
#     print(f"Regions              : {regions.shape}")
#     print(f"Service Logs         : {service_logs.shape}")
#     print(f"Shipments            : {shipments.shape}")
#     print(f"Suppliers            : {suppliers.shape}")

#     print("\n✅ All CSV files loaded successfully.")


# missing = customers.isnull().sum()

# print("Original Series")
# print(missing)

# print("\nBoolean Mask")
# print(missing > 0)

# print("\nFiltered Series")
# print(missing[missing > 0])

