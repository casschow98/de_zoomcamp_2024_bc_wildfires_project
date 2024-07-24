from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import pendulum
import datetime
import os
from functions import upload_to_gcs, convert_to_geojson, delete_contents

# Define your bucket and home path environment variables
home_path = os.environ.get("AIRFLOW_HOME","/opt/airflow/")
BUCKET = os.environ.get("GCP_STORAGE_BUCKET")
DATASET = "de_zoomcamp_cchow_dataset"
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

# Define the file name stem
rec_lines_file = "recreation_lines"

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
    'rec_data_dag',
    default_args=default_args,
    description='Uploading recreation data to Google Cloud Storage and BigQuery',
    schedule='@daily',
    catchup=False
)

# Define the tasks

upload_zip_task_rec = PythonOperator(
    task_id='upload_zip_task_rec',
    python_callable=upload_to_gcs,
    op_kwargs={
        "home_dir": home_path,
        "bucket_name": BUCKET,
        "rel_path": f"{rec_lines_file}.zip"
    },
    dag=dag
)

convert_to_geojson_task_rec = PythonOperator(
    task_id='convert_to_geojson_task_rec',
    python_callable=convert_to_geojson,
    op_kwargs={
        "home_dir": home_path,
        "file_name": rec_lines_file
    },
    dag=dag
)

geojsonl_task_rec = BashOperator(
    task_id='geojsonl_task_rec',
    bash_command="geojson2ndjson {{ params.in_geojson }} > {{ params.out_geojsonl }}",
    params = {
        "in_geojson" : f"{home_path}/tmp/{rec_lines_file}.geojson",
        "out_geojsonl" : f"{home_path}/tmp/{rec_lines_file}_nl.geojsonl"
    },
    dag=dag
)

upload_geojsonl_task_rec = PythonOperator(
    task_id='upload_geojsonl_task_rec',
    python_callable=upload_to_gcs,
    op_kwargs={
        "home_dir": home_path,
        "bucket_name": BUCKET,
        "rel_path": f"tmp/{rec_lines_file}_nl.geojsonl"
    },
    dag=dag
)

load_rec_bq_task = BashOperator(
    task_id='load_rec_bq_task',
    bash_command="bq load  --replace --source_format=NEWLINE_DELIMITED_JSON --clustering_fields=geometry --json_extension=GEOJSON --autodetect {{ params.dataset }}.{{ params.file_stem}}_raw gs://{{ params.bucket }}/{{ params.file_stem }}_nl.geojsonl",
    params = {
        "dataset" : DATASET,
        "file_stem" : rec_lines_file,
        "bucket" : BUCKET
    },
    dag=dag
)

delete_contents_task = PythonOperator(
    task_id='delete_contents_task',
    python_callable=delete_contents,
    op_kwargs={
        "home_dir": home_path,
        "names": ['tmp']
    },
    provide_context=True,
    dag=dag
)


# Set the dependencies between the tasks
upload_zip_task_rec >> convert_to_geojson_task_rec >> geojsonl_task_rec >> upload_geojsonl_task_rec >> load_rec_bq_task >> delete_contents_task