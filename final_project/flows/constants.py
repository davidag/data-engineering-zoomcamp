import os


# Prefect block names
BUCKET_BLOCK_NAME = "gc-storage-data-lake"
CREDENTIALS_BLOCK_NAME = "gc-creds"

# Google Cloud constants
DATASET_NAME = "mlcet_dataset"
PROJECT_ID = os.environ["GCP_PROJECT_ID"]
