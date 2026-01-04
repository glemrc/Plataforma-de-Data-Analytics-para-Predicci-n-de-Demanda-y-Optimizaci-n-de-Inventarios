from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="load_sales_csv_to_postgres",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["etl", "sales", "postgres"],
) as dag:

    load_sales = BashOperator(
        task_id="load_sales_csv",
        bash_command="python /opt/airflow/scripts/load_sales_csv.py",
    )

    load_sales
