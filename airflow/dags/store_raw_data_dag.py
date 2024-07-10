from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum
import datetime
from google.cloud import storage
import os
import wget

# Define your bucket and home path environment variables
BUCKET = os.environ.get("GCP_STORAGE_BUCKET")
home_path = os.environ.get("AIRFLOW_HOME","/opt/airflow/")

# Define the file names
fire_poly_file = "fire_poly.zip"
rec_lines_file = "rec_lines.zip"

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "start_date": pendulum.datetime(2024, 1, 1, tz="America/Vancouver"),
    "end_date": pendulum.datetime(2025, 2, 1, tz="America/Vancouver"),
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=1)
}

# Define the function to download wildfire data
def download_wildfire_data(home_dir, fire_poly_name):
    
    fire_poly_url = 'https://pub.data.gov.bc.ca/datasets/cdfc2d7b-c046-4bf0-90ac-4897232619e1/prot_current_fire_polys.zip'
    path = os.path.join(home_dir,fire_poly_name)
    if os.path.exists(path):
        os.remove(path) # if exist, remove it directly
    wget.download(fire_poly_url, out=path) # download it to the specific path.

# Define the function to upload files to GCS
def upload_to_gcs(home_dir, bucket_name, file_name):
    # Initialize a storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)
    destination_folder = "shapefiles"
    destination_path = os.path.join(destination_folder, file_name)
    source_path = os.path.join(home_dir, file_name)

    # Create a blob
    blob = bucket.blob(destination_path)

    # Upload the file
    blob.upload_from_filename(source_path)


# Define the DAG
dag = DAG(
    'ingestion_dag',
    default_args=default_args,
    description='Uploading raw shapefiles to GCP Storage Bucket',
    schedule='@daily',
    catchup=False
)

# Define the tasks
download_data_task = PythonOperator(
    task_id='download_data_task',
    python_callable=download_wildfire_data,
    op_kwargs={
        "home_dir": home_path,
        # "fire_points_name": fire_points_file,
        "fire_poly_name": fire_poly_file
    },
    dag=dag
)

upload_fire_poly_task = PythonOperator(
    task_id='upload_fire_poly_task',
    python_callable=upload_to_gcs,
    op_kwargs={
        "home_dir": home_path,
        "bucket_name": BUCKET,
        "file_name": fire_poly_file
    },
    dag=dag
)

upload_rec_data_task = PythonOperator(
    task_id='upload_rec_data_task',
    python_callable=upload_to_gcs,
    op_kwargs={
        "home_dir": home_path,
        "bucket_name": BUCKET,
        "file_name": rec_lines_file
    },
    dag=dag
)


# Set the dependencies between the tasks
download_data_task >> upload_fire_poly_task >> upload_rec_data_task
