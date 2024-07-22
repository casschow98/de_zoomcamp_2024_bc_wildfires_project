from datetime import datetime
import os
from airflow.models import DAG
from airflow.operators.bash import BashOperator
import pendulum
import datetime


default_args = {
    "owner": "airflow",
    "start_date": pendulum.datetime(2024, 1, 1, tz="America/Vancouver"),
    "end_date": pendulum.datetime(2025, 2, 1, tz="America/Vancouver"),
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=0.5)
}

with DAG(
    dag_id="test_dbt_dag",
    default_args=default_args,
    start_date=datetime(2021, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    dbt_task = BashOperator(
        task_id="dbt_task",
        bash_command=f"cd /opt/airflow/dbt/ && dbt deps && dbt debug --config-dir && dbt run"
    )

dbt_task