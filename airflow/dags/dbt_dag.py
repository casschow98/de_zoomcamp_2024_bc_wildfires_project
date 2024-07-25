import os
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
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

dag=DAG(
    dag_id="dbt_dag",
    default_args=default_args,
    schedule='@daily',
    catchup=False,
)

# wait_for_rec_data = ExternalTaskSensor(
#     task_id='wait_for_rec_data',
#     external_dag_id='rec_data_dag',
#     external_task_id='delete_contents_task',  # Task ID to check in the parent DAG
#     mode='poke',
#     timeout=600,
#     poke_interval=30,
#     allowed_states=['success'],
#     dag=dag,
# )

# wait_for_fire_data = ExternalTaskSensor(
#     task_id='wait_for_fire_data',
#     external_dag_id='fire_data_dag',
#     external_task_id='load_fire_bq_task',  # Task ID to check in the parent DAG
#     mode='poke',
#     timeout=600,
#     poke_interval=30,
#     allowed_states=['success'],
#     dag=dag,
# )

dbt_task = BashOperator(
    task_id="dbt_task",
    bash_command=f"cd /opt/airflow/dbt/ && dbt deps && dbt debug --config-dir && dbt run",
    dag=dag
)



# wait_for_fire_data >>
dbt_task