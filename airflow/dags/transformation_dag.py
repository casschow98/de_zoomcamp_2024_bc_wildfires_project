from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.dataproc import (DataprocSubmitJobOperator)
from google.cloud import storage
import zipfile
from airflow.operators.bash import BashOperator
import os
import pendulum
import datetime


# Fetch the path to the .jar file from the environment variable
home_path = os.environ.get("AIRFLOW_HOME","/opt/airflow/")
project_name = os.environ.get("GCP_PROJECT_NAME")
project_id = os.environ.get("GCP_PROJECT_ID")
bucket_name = os.environ.get("GCP_STORAGE_BUCKET")
region="us-west1"
zone="us-west1-c"
cluster_name="example-cluster"
extracted_folder = f"tmp/shapefiles"
pyspark_file = "transformation.py"
pyspark_file_path = os.path.join(home_path,"dags",pyspark_file)
spark_bq_jar_file = "spark-bigquery-latest_2.12.jar"
spark_bq_jar_path = os.path.join(home_path,"dags",spark_bq_jar_file)

def upload_to_gcs(bucket_name, local_file):
    # Initialize a storage client
    storage_client = storage.Client()
    # Get the bucket
    bucket = storage_client.bucket(bucket_name)
    object_name = os.path.basename(local_file)
    # Create blob
    blob = bucket.blob(object_name)
    # Upload the file
    blob.upload_from_filename(local_file)


# CLUSTER_GENERATOR_CONFIG = ClusterGenerator(
#     project_id=project_id,
#     zone=zone,
#     master_machine_type="n1-standard-4",
#     master_disk_size=32,
#     num_masters=1,
#     num_workers=0,
#     storage_bucket=bucket_name,
# ).make()

pyspark_job = {
    "reference": {"project_id": project_id},
    "placement": {"cluster_name": cluster_name},
    "pyspark_job": {
        "main_python_file_uri": f"gs://{bucket_name}/{pyspark_file}",
        "jar_file_uris": [f"gs://{bucket_name}/{spark_bq_jar_file}"],
        "args": [
        f"--project_id={project_id}",
        f"--bucket={bucket_name}",
        ],
    },
}

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "start_date": pendulum.datetime(2024, 1, 1, tz="America/Vancouver"),
    "end_date": pendulum.datetime(2025, 2, 1, tz="America/Vancouver"),
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=1)
}

dag = DAG(
    'test_transformation',
    default_args=default_args,
    description='Create summary table of recreation lines data',
    schedule='@daily',
    catchup=False
)

upload_script_task = PythonOperator(
    task_id='upload_script_task',
    python_callable=upload_to_gcs,
    op_kwargs={
        "bucket_name": bucket_name,
        "local_file": pyspark_file_path
    },
    dag=dag
)

upload_spark_bq_jar_task = PythonOperator(
    task_id='upload_spark_bq_jar_task',
    python_callable=upload_to_gcs,
    op_kwargs={
        "bucket_name": bucket_name,
        "local_file": spark_bq_jar_path
    },
    dag=dag
)

# create_cluster_task = DataprocCreateClusterOperator(
#     task_id="create_cluster",
#     project_id=project_id,
#     cluster_config=CLUSTER_GENERATOR_CONFIG,
#     region=region,
#     cluster_name=cluster_name,
#     dag=dag
# )

pyspark_task = DataprocSubmitJobOperator(
    task_id="pyspark_task", job=pyspark_job, region=region, project_id=project_id
)

# geojsonl_task = BashOperator(
#     task_id="geojsonl_task",
#     bash_command="cd /opt/airflow/dbt && dbt run"
#     geojson2ndjson {in.geojson} > {out.geojsonl}
# ,
# )

# delete_cluster_task = DataprocDeleteClusterOperator(
#     task_id="delete_cluster",
#     project_id=project_id,
#     cluster_name=cluster_name,
#     region=region,
# )



upload_script_task >> upload_spark_bq_jar_task >> pyspark_task