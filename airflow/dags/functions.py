import os
from airflow.exceptions import AirflowException
from google.cloud import storage
import wget
import zipfile
import pyogrio
import geopandas as gpd
import shutil


# Function to download wildfire data from BC Data Catalogue
def download_wildfire_data(home_dir, fire_poly_name):
    
    fire_poly_url = 'https://pub.data.gov.bc.ca/datasets/cdfc2d7b-c046-4bf0-90ac-4897232619e1/prot_current_fire_polys.zip'
    zipfile = f"{fire_poly_name}.zip"
    path = os.path.join(home_dir,zipfile)
    if os.path.exists(path):
        os.remove(path)
    wget.download(fire_poly_url, out=path)

# Function to upload files to GCS
def upload_to_gcs(home_dir, bucket_name, rel_path):
    # Initialize a storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)
    basename = os.path.basename(rel_path)
    source_path = os.path.join(home_dir, rel_path)

    # Create a blob
    blob = bucket.blob(basename)

    # Upload the file
    print(f"Uploading to storage bucket as {blob} from {source_path}...")
    try:
        blob.upload_from_filename(source_path)
        print(f"Successfully uploaded file from {source_path} to {blob}")
    except Exception as e:
        print(f"Error uploading file {source_path} to {blob}: {str(e)}")
        raise AirflowException("Task failed due to an exception")

# Function to extract the zipfiles and convert to geojson
def convert_to_geojson(home_dir, file_name):
    # Unzip the local shapefile
    zipfile_name = f"{file_name}.zip"
    local_zip_path = os.path.join(home_dir, zipfile_name)
    extracted_folder = os.path.join(home_dir,'tmp')
    os.makedirs('tmp',exist_ok=True)

    with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_folder)
    
    for file in os.listdir(extracted_folder):
        if file.endswith(".shp"):
            shapefile=file
    
    shapefile_path = os.path.join(extracted_folder,shapefile)
    print(f"Transforming shapefile {shapefile} from {shapefile_path}")
    gdf = gpd.read_file(shapefile_path)
    gdf = gdf.to_crs(epsg="4326")
    df_size = gdf.size
    print(f"Size of dataframe from shapefile is: {df_size}")
    # Convert to a geojson
    try:
        gdf.to_file(f"{extracted_folder}/{file_name}.geojson",driver='GeoJSON')
        print(f"Downloaded {file_name}.geojson to {extracted_folder} successfully")
    except Exception as e:
        print(f"Error exporting file {file_name}.geojson: {str(e)}")


# Function to delete files or directories
def delete_contents(home_dir, *name):
    
    path = os.path.join(home_dir,name)
    for n in name:
        if os.path.isfile(path):
            os.remove(path)
            print(f"Successfully removed file {path}!")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Successfully removed directory and contents of {path}!")
