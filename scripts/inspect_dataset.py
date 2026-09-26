import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")

for file in DATA_DIR.glob("*.parquet"):
    print("\n" + "=" * 60)
    print(f"FILE: {file.name}")
    print("=" * 60)

    df = pd.read_parquet(file)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}: {df[column].dtype}")

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))