terraform {
  required_version = ">= 1.0"
  backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project
  region = var.region
  // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name          = "${local.data_lake_bucket}_${var.project}" # Concatenating DL bucket & Project name for unique naming
  location      = var.region
  labels        = {}

  # Optional, but recommended settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}

# Data Warehouse
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset
  project    = var.project
  location   = var.region
}

resource "google_bigquery_table" "nodes_table" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "nodes"
  schema = <<EOF
[
  {
    "name": "nid",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "uid",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "type",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "created",
    "type": "TIMESTAMP",
    "mode": "NULLABLE"
  },
  {
    "name": "year",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "month",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "title",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "stems",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "view_counter",
    "type": "INTEGER",
    "mode": "NULLABLE"
  }
]
EOF
  time_partitioning {
    type = "YEAR"
    field = "created"
  }
}

resource "google_bigquery_table" "comments_table" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "comments"
  schema = <<EOF
[
  {
    "name": "cid",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "nid",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "uid",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "type",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "created",
    "type": "TIMESTAMP",
    "mode": "NULLABLE"
  },
  {
    "name": "year",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "month",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "stems",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF
  time_partitioning {
    type = "YEAR"
    field = "created"
  }
}

resource "google_bigquery_table" "users_table" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "users"
  schema = <<EOF
[
  {
    "name": "uid",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "name",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "created",
    "type": "TIMESTAMP",
    "mode": "NULLABLE"
  },
  {
    "name": "year",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "month",
    "type": "INTEGER",
    "mode": "NULLABLE"
  }
]
EOF
}