from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket


# Prefect constants
CREDENTIALS_BLOCK_NAME = "zoom-gcp-creds"
BUCKET_BLOCK_NAME = "zoom-gcs-week2"

# Google Cloud constants
BUCKET_GCP_NAME = "data-lake-week2_dtc-de-375612"


# Create or update credentials block in Prefect
credentials_block = GcpCredentials(
    service_account_file = "~/.secrets/gcp-zoomcamp-credentials.json"
)

credentials_block.save(CREDENTIALS_BLOCK_NAME, overwrite=True)

# Create or update Google Cloud Storage block in Prefect
bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load(CREDENTIALS_BLOCK_NAME),
    bucket=BUCKET_GCP_NAME,
)

doc_id = bucket_block.save(BUCKET_BLOCK_NAME, overwrite=True)

print(f"GcsBucket created: {doc_id}")
