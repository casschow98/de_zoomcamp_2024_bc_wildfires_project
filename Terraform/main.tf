terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.35.0"
    }
  }
}

provider "google" {
  credentials = file(var.gcp_credentials)
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "bucket-1" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = true
  storage_class = var.bucket_storage_class

  public_access_prevention = "enforced"


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "dataset-1" {
  dataset_id = var.bq_dataset_name
  location = var.region

  delete_contents_on_destroy = true
}


# resource "google_bigquery_table" "table-1" {
#   project = var.project_id
#   dataset_id = var.bq_dataset_name
#   table_id   = var.bq_table_1
#   schema = <<EOF
# [
#   {
#     "name": "type",
#     "type": "STRING",
#     "mode": "NULLABLE",
#     "description": ""
#   },
#   {
#     "name": "properties",
#     "type": "RECORD",
#     "mode": "REPEATED",
#     "fields": [
#       {
#         "name": "OBJECTID",
#         "type": "INTEGER",
#         "mode": "NULLABLE",
#         "description": ""
#       },
#       {
#         "name": "FIRE_YEAR",
#         "type": "INTEGER",
#         "mode": "NULLABLE",
#         "description": ""
#       },
#       {
#         "name": "FIRE_NUM",
#         "type": "STRING",
#         "mode": "NULLABLE",
#         "description": ""
#       },
#       {
#         "name": "VERSN_NUM",
#         "type": "INTEGER",
#         "mode": "NULLABLE",
#         "description": ""
#       },
#       {
#         "name": "FIRE_SZ_HA",
#         "type": "FLOAT",
#         "mode": "NULLABLE",
#         "description": ""
#       },
#       {
#         "name": "SOURCE",
#         "type": "STRING",
#         "mode": "NULLABLE",
#         "description": ""
#       },
#       {
#         "name": "TRACK_DATE",
#         "type": "TIMESTAMP",
#         "mode": "NULLABLE",
#         "description": ""
#       },
#       {
#         "name": "LOAD_DATE",
#         "type": "TIMESTAMP",
#         "mode": "NULLABLE",
#         "description": ""
#       },
#       {
#         "name": "FIRE_STAT",
#         "type": "STRING",
#         "mode": "NULLABLE",
#         "description": ""
#       },
#       {
#         "name": "FIRE_LINK",
#         "type": "STRING",
#         "mode": "NULLABLE",
#         "description": ""
#       },
#       {
#         "name": "FEATURE_CD",
#         "type": "STRING",
#         "mode": "NULLABLE",
#         "description": ""
#       }
#     ],
#     "description": "Properties of the fire incident"
#   },
#   {
#     "name": "geometry",
#     "type": "RECORD",
#     "mode": "NULLABLE",
#     "fields": [
#       {
#         "name": "type",
#         "type": "STRING",
#         "mode": "NULLABLE",
#         "description": ""
#       },
#       {
#         "name": "coordinates",
#         "type": "GEOGRAPHY",
#         "mode": "REQUIRED",
#         "description": ""
#       }
#     ],
#     "description": "Geographic coordinates"
#   }
# ]

# EOF
# }


# resource "google_bigquery_table" "table-2" {
#   project = var.project_id
#   dataset_id = var.bq_dataset_name
#   table_id   = var.bq_table_2
# }