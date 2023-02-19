from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket


# Prefect constants
CREDENTIALS_BLOCK_NAME = "zoom-gcp-creds"  # Assumes this one already exists from last week
BUCKET_BLOCK_NAME = "zoom-gcs-bucket"

# Google Cloud constants
BUCKET_GCP_NAME = "data-warehouse_dtc-de-375612"

# Create or update Google Cloud Storage block in Prefect
bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load(CREDENTIALS_BLOCK_NAME),
    bucket=BUCKET_GCP_NAME,
)

doc_id = bucket_block.save(BUCKET_BLOCK_NAME, overwrite=True)

print(f"GcsBucket created: {doc_id}")
