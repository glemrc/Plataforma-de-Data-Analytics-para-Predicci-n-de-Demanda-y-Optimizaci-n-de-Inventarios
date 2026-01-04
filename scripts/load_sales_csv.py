import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

DATA_ROOT = "/opt/airflow/data/raw"

DB_CONFIG = {
    "host": "postgres",
    "dbname": "demand_forecasting",
    "user": "airflow",
    "password": "airflow",
    "port": 5432
}


def load_csv_to_postgres():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    records_loaded = 0

    for store_folder in os.listdir(DATA_ROOT):
        store_path = os.path.join(DATA_ROOT, store_folder)

        if not os.path.isdir(store_path):
            continue

        for file in os.listdir(store_path):
            if not file.endswith(".csv"):
                continue

            file_path = os.path.join(store_path, file)
            print(f"Cargando archivo: {file_path}")

            df = pd.read_csv(file_path)

            expected_columns = {
                "date",
                "product_id",
                "store_id",
                "units_sold",
                "price",
                "promotion_flag"
            }

            if not expected_columns.issubset(df.columns):
                raise ValueError(f"Columnas inválidas en {file}")

            records = list(
                df[[
                    "date",
                    "product_id",
                    "store_id",
                    "units_sold",
                    "price",
                    "promotion_flag"
                ]].itertuples(index=False, name=None)
            )

            query = """
                INSERT INTO sales (
                    sale_date,
                    product_id,
                    store_id,
                    units_sold,
                    price,
                    promotion_flag
                )
                VALUES %s
                ON CONFLICT DO NOTHING;
            """

            execute_values(cursor, query, records)
            records_loaded += len(records)

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Carga finalizada. Filas procesadas: {records_loaded}")


if __name__ == "__main__":
    load_csv_to_postgres()
