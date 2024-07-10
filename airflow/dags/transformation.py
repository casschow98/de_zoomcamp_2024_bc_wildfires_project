import argparse

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

parser = argparse.ArgumentParser()
parser.add_argument("--project_id", required=True, type=str)
parser.add_argument("--bucket", required=True, type=str)
args = parser.parse_args()


BQ_TABLE = "famous-muse-426921-s5.de_zoomcamp_cchow_dataset.cchow_table"

def main():
    spark = SparkSession.builder \
             .appName('test') \
             .getOrCreate()
             
        
    spark.conf.set('temporaryGcsBucket', 'dataproc-temp-us-west1-735867942533-fwzp1ps9')


    sql_query = f"""
    SELECT LOAD_DATE, TRACK_DATE, FIRE_STAT, FIRE_SZ_HA, FIRE_YEAR, FIRE_NUM, OBJECTID, geometry
    FROM `{BQ_TABLE}`
    """

    df = spark.read \
        .format("bigquery") \
        .option("project", args.project_id) \
        .option("query", sql_query) \
        .load()


    summary_df = df.groupby([F.col("FIRE_YEAR")]).count()
    summary_df = summary_df.select((F.col("LOAD_DATE")).alias("load_date"), 
                                F.col("TRACK_DATE").alias("track_date"), 
                                F.col("FIRE_STAT").alias("fire_status"),
                                F.col("FIRE_SZ_HA").alias("fire_size_ha"),
                                F.col("FIRE_YEAR").alias("fire_year"),
                                F.col("FIRE_NUM").alias("fire_number"), 
                                F.col("OBJECT_ID").alias("object_id"),
                                F.col("geometry").alias("geometry"),
    )

    summary_df.write.format('bigquery') \
        .option('project',args.project_id) \
        .option('table', f"{args.project_id}.de_zoomcamp_cchow_dataset.fire_poly_agg") \
        .save()

        # .mode('overwrite') \


            # .option('temporaryGcsBucket', args.bucket) \

    
if __name__ == "__main__":
    main()