from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
import pendulum
import datetime
import os
from functions import download_wildfire_data, upload_to_gcs, convert_to_geojson, delete_contents


# Define your bucket and home path environment variables
home_path = os.environ.get("AIRFLOW_HOME","/opt/airflow/")
BUCKET = os.environ.get("GCP_STORAGE_BUCKET")
DATASET = "de_zoomcamp_cchow_dataset"
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

# Define the file name stem
fire_poly_file = "wildfire_polygons"

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "start_date": pendulum.datetime(2024, 1, 1, tz="America/Vancouver"),
    "end_date": pendulum.datetime(2025, 2, 1, tz="America/Vancouver"),
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=0.5)
}

# Define the DAG
dag = DAG(
    'fire_data_dag',
    default_args=default_args,
    description='Uploading wildfire data to Google Cloud Storage and BigQuery',
    schedule='@daily',
    catchup=False
)

# Define the tasks
download_task_fire = PythonOperator(
    task_id='download_task_fire',
    python_callable=download_wildfire_data,
    op_kwargs={
        "home_dir": home_path,
        "fire_poly_name": fire_poly_file
    },
    dag=dag
)

upload_zip_task_fire = PythonOperator(
    task_id='upload_zip_task_fire',
    python_callable=upload_to_gcs,
    op_kwargs={
        "home_dir": home_path,
        "bucket_name": BUCKET,
        "rel_path": f"{fire_poly_file}.zip"
    },
    dag=dag
)

convert_to_geojson_task_fire = PythonOperator(
    task_id='convert_to_geojson_task_fire',
    python_callable=convert_to_geojson,
    op_kwargs={
        "home_dir": home_path,
        "file_name": fire_poly_file
    },
    dag=dag
)

geojsonl_task_fire = BashOperator(
    task_id='geojsonl_task_fire',
    bash_command="geojson2ndjson {{ params.in_geojson }} > {{ params.out_geojsonl }}",
    params = {
        "in_geojson" : f"{home_path}/tmp/{fire_poly_file}.geojson",
        "out_geojsonl" : f"{home_path}/tmp/{fire_poly_file}_nl.geojsonl"
    },
    dag=dag
)

upload_geojsonl_task_fire = PythonOperator(
    task_id='upload_geojsonl_task_fire',
    python_callable=upload_to_gcs,
    op_kwargs={
        "home_dir": home_path,
        "bucket_name": BUCKET,
        "rel_path": f"tmp/{fire_poly_file}_nl.geojsonl"
    },
    dag=dag
)

delete_contents_task = PythonOperator(
    task_id='delete_contents_task',
    python_callable=delete_contents,
    op_kwargs={
        "home_dir": home_path,
        "names": ['tmp',f"{fire_poly_file}.zip"]
    },
    provide_context=True,
    dag=dag
)

load_fire_bq_task = BashOperator(
    task_id='load_fire_bq_task',
    bash_command="bq load  --replace --source_format=NEWLINE_DELIMITED_JSON --clustering_fields=geometry --json_extension=GEOJSON --autodetect {{ params.dataset }}.{{ params.file_stem}}_raw gs://{{ params.bucket }}/{{ params.file_stem }}_nl.geojsonl",
    params = {
        "dataset" : DATASET,
        "file_stem" : fire_poly_file,
        "bucket" : BUCKET
    },
    dag=dag
)

wait_for_rec_data = ExternalTaskSensor(
    task_id='wait_for_rec_data',
    external_dag_id='rec_data_dag',
    external_task_id='delete_contents_task',  # Task ID to check in the parent DAG
    mode='poke',
    timeout=600,
    poke_interval=30,
    allowed_states=['success'],
    dag=dag,
)


# Set the dependencies between the tasks
wait_for_rec_data >> download_task_fire >> upload_zip_task_fire >> convert_to_geojson_task_fire >> geojsonl_task_fire >> upload_geojsonl_task_fire >> load_fire_bq_task >> delete_contents_task