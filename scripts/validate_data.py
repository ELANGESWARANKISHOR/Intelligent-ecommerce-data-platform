import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")


def check_duplicates(file_name, column):
    df = pd.read_parquet(DATA_DIR / file_name)

    duplicates = df[column].duplicated().sum()

    print(f"{file_name}")
    print(f"  Total rows: {len(df):,}")
    print(f"  Duplicate {column}: {duplicates:,}")
    print()


def check_foreign_key(file_name, column, reference_file, reference_column):
    df = pd.read_parquet(DATA_DIR / file_name)
    reference_df = pd.read_parquet(DATA_DIR / reference_file)

    invalid = (~df[column].isin(reference_df[reference_column])).sum()

    print(f"{file_name} -> {reference_file}")
    print(f"  Invalid {column}: {invalid:,}")
    print()


print("=" * 60)
print("PRIMARY KEY VALIDATION")
print("=" * 60)

check_duplicates("customers.parquet", "customer_id")
check_duplicates("sessions.parquet", "session_id")
check_duplicates("orders.parquet", "order_id")
check_duplicates("order_items.parquet", "order_item_id")
check_duplicates("products.parquet", "product_id")
check_duplicates("returns.parquet", "return_id")
check_duplicates("support_tickets.parquet", "ticket_id")


print("=" * 60)
print("FOREIGN KEY VALIDATION")
print("=" * 60)

check_foreign_key(
    "sessions.parquet",
    "customer_id",
    "customers.parquet",
    "customer_id"
)

check_foreign_key(
    "orders.parquet",
    "customer_id",
    "customers.parquet",
    "customer_id"
)

check_foreign_key(
    "orders.parquet",
    "session_id",
    "sessions.parquet",
    "session_id"
)

check_foreign_key(
    "order_items.parquet",
    "order_id",
    "orders.parquet",
    "order_id"
)

check_foreign_key(
    "order_items.parquet",
    "product_id",
    "products.parquet",
    "product_id"
)

check_foreign_key(
    "returns.parquet",
    "order_id",
    "orders.parquet",
    "order_id"
)

check_foreign_key(
    "returns.parquet",
    "order_item_id",
    "order_items.parquet",
    "order_item_id"
)

check_foreign_key(
    "returns.parquet",
    "product_id",
    "products.parquet",
    "product_id"
)

check_foreign_key(
    "support_tickets.parquet",
    "customer_id",
    "customers.parquet",
    "customer_id"
)

check_foreign_key(
    "support_tickets.parquet",
    "order_id",
    "orders.parquet",
    "order_id"
)


print("=" * 60)
print("NUMERIC VALIDATION")
print("=" * 60)

orders = pd.read_parquet(DATA_DIR / "orders.parquet")

print("Orders with zero/negative total:")
print((orders["order_total"] <= 0).sum())

order_items = pd.read_parquet(DATA_DIR / "order_items.parquet")

print("\nOrder items with zero/negative quantity:")
print((order_items["quantity"] <= 0).sum())

print("\nOrder items with zero/negative price:")
print((order_items["unit_price"] <= 0).sum())

print("\nOrder items where line_total != quantity * unit_price:")

calculated_total = order_items["quantity"] * order_items["unit_price"]

mismatch = (
    (order_items["line_total"] - calculated_total).abs() > 0.01
).sum()

print(mismatch)

print("\n" + "=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)