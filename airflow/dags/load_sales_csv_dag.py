from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import psycopg2

# -------------------------
# Configuración PostgreSQL
# -------------------------
DB_CONFIG = {
    "host": "postgres",
    "dbname": "demand_forecasting",
    "user": "airflow",
    "password": "airflow",
}

# -------------------------
# Funciones de validación
# -------------------------
def check_row_count():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM sales;")
    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    if count == 0:
        raise ValueError("La tabla sales está vacía")
    print(f"Validación OK: {count} filas cargadas")


def check_duplicates():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT sale_date, store_id, product_id, COUNT(*)
        FROM sales
        GROUP BY sale_date, store_id, product_id
        HAVING COUNT(*) > 1;
    """)
    duplicates = cur.fetchall()

    cur.close()
    conn.close()

    if duplicates:
        raise ValueError(f"Duplicados encontrados: {len(duplicates)}")
    print("Validación OK: No existen duplicados")


def check_negative_sales():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM sales
        WHERE units_sold < 0;
    """)
    negatives = cur.fetchone()[0]

    cur.close()
    conn.close()

    if negatives > 0:
        raise ValueError(f"Ventas negativas encontradas: {negatives}")
    print("Validación OK: No hay ventas negativas")


def check_invalid_prices():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM sales
        WHERE price <= 0;
    """)
    invalid_prices = cur.fetchone()[0]

    cur.close()
    conn.close()

    if invalid_prices > 0:
        raise ValueError(f"Precios inválidos encontrados: {invalid_prices}")
    print("Validación OK: Todos los precios son válidos")

# -------------------------
# Definición del DAG
# -------------------------
with DAG(
    dag_id="load_and_validate_sales",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["ingestion", "data-quality", "retail"]
) as dag:

    load_sales = PythonOperator(
        task_id="load_sales_csv",
        python_callable=lambda: print("Carga realizada previamente")
    )

    row_count = PythonOperator(
        task_id="check_row_count",
        python_callable=check_row_count
    )

    duplicates = PythonOperator(
        task_id="check_duplicates",
        python_callable=check_duplicates
    )

    negative_sales = PythonOperator(
        task_id="check_negative_sales",
        python_callable=check_negative_sales
    )

    invalid_prices = PythonOperator(
        task_id="check_invalid_prices",
        python_callable=check_invalid_prices
    )

    load_sales >> row_count >> duplicates >> negative_sales >> invalid_prices
