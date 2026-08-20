import pandas as pd
import mysql.connector
from pathlib import Path

# ==========================================
# DATABASE CONFIGURATION
# ==========================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Data@12345",
    database="reloop_crate_systems"
)

cursor = conn.cursor()

# ==========================================
# CSV FOLDER
# ==========================================

csv_folder = Path(r"F:\Data Analytics\Codex_Project #1\csv")

# ==========================================
# IMPORT ORDER
# ==========================================

tables = [
    "regions",
    "employees",
    "suppliers",
    "customers",
    "customer_addresses",
    "crate_models",
    "contracts",
    "deployment_orders",
    "order_items",
    "shipments",
    "service_logs",
    "invoices"
]

print("=" * 60)
print("STARTING DATA IMPORT")
print("=" * 60)

for table in tables:

    print(f"\nLoading {table}...")

    try:

        file = csv_folder / f"{table}.csv"

        df = pd.read_csv(file)

        # -----------------------------------
        # Remove empty columns
        # -----------------------------------

        df = df.loc[:, ~df.columns.isna()]
        df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed")]

        # -----------------------------------
        # Replace NaN with None
        # -----------------------------------

        df = df.astype(object)
        df = df.where(pd.notnull(df), None)

        columns = list(df.columns)

        sql = f"""
        INSERT INTO {table}
        ({','.join(columns)})
        VALUES ({','.join(['%s'] * len(columns))})
        """

        data = [tuple(row) for row in df.itertuples(index=False, name=None)]

        cursor.executemany(sql, data)

        conn.commit()

        print(f"✓ {cursor.rowcount} rows inserted.")

    except Exception as e:

        conn.rollback()

        print(f"\n❌ ERROR importing {table}")
        print(e)

        break

cursor.close()
conn.close()

print("\nFinished.")