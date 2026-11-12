
import os
import re
import sqlite3
import pandas as pd

from datasets import load_dataset

# Output directory
OUTPUT_DIR = "bangladesh_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Dataset information
datasets_info = [
    {
        "repo": "Mahadih534/Institutional-Information-of-Bangladesh",
        "csv": "institutions.csv",
        "db": "institutions.db",
        "table": "institutions"
    },
    {
        "repo": "Mahadih534/all-bangladeshi-hospitals",
        "csv": "hospitals.csv",
        "db": "hospitals.db",
        "table": "hospitals"
    },
    {
        "repo": "Mahadih534/Bangladeshi-Restaurant-Data",
        "csv": "restaurants.csv",
        "db": "restaurants.db",
        "table": "restaurants"
    }
]


# Clean column names
def clean_column_name(column):
    column = str(column).strip().lower()
    column = re.sub(r'[^a-zA-Z0-9]+', '_', column)
    return column.strip('_')


# Convert dataframe types
def convert_data_types(df):

    for col in df.columns:

        # Keep identifier columns as TEXT
        if any(key in col for key in
               ["id", "code", "eiin", "phone", "mobile", "zip"]):
            df[col] = df[col].astype("string")
            continue

        numeric = pd.to_numeric(df[col], errors="coerce")

        total = df[col].notna().sum()

        if total > 0 and numeric.notna().sum() / total >= 0.95:

            if (numeric.dropna() % 1 == 0).all():
                df[col] = numeric.astype("Int64")
            else:
                df[col] = numeric.astype("float64")

    return df


# Create SQLite database
def create_database(df, db_path, table_name):

    connection = sqlite3.connect(db_path)

    df.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False
    )

    # Create index for name column if available
    if "name" in df.columns:
        connection.execute(
            f'CREATE INDEX IF NOT EXISTS idx_{table_name}_name '
            f'ON "{table_name}" ("name")'
        )

    connection.commit()
    connection.close()


# Main processing
def main():

    for item in datasets_info:

        print("\n" + "=" * 60)
        print("Downloading:", item["repo"])

        # Download dataset
        dataset = load_dataset(item["repo"])

        # Load train split
        df = dataset["train"].to_pandas()

        print("Original rows:", len(df))

        # Clean columns
        df.columns = [
            clean_column_name(col)
            for col in df.columns
        ]

        # Convert data types
        df = convert_data_types(df)

        # Save CSV
        csv_path = os.path.join(
            OUTPUT_DIR,
            item["csv"]
        )

        df.to_csv(
            csv_path,
            index=False,
            encoding="utf-8-sig"
        )

        print("CSV saved:", csv_path)

        # Create SQLite database
        db_path = os.path.join(
            OUTPUT_DIR,
            item["db"]
        )

        create_database(
            df,
            db_path,
            item["table"]
        )

        print("SQLite DB saved:", db_path)

        # Verify database
        with sqlite3.connect(db_path) as conn:

            count = conn.execute(
                f'SELECT COUNT(*) FROM "{item["table"]}"'
            ).fetchone()[0]

            columns = conn.execute(
                f'PRAGMA table_info("{item["table"]}")'
            ).fetchall()

        print("Total records:", count)
        print("Database columns:")

        for column in columns:
            print(f"{column[1]} -> {column[2]}")

    print("\nAll datasets processed successfully!")


if __name__ == "__main__":
    main()
