import os
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from prefect_sqlalchemy import SqlAlchemyConnector, ConnectionComponents, SyncDriver


project_id = os.environ["GCP_PROJECT_ID"]

print(f"Using project id: {project_id}")

# Prefect constants
CREDENTIALS_BLOCK_NAME = "gc-creds"
BUCKET_BLOCK_NAME = "gc-storage-data-lake"
MYSQL_BLOCK_NAME = "mysql-db"

# Google Cloud constants
BUCKET_GCP_NAME = f"data-lake_{project_id}"

# Create or update credentials block
credentials_block = GcpCredentials(
    service_account_file = "~/.secrets/gcp-zoomcamp-credentials.json"
)

doc_id = credentials_block.save(CREDENTIALS_BLOCK_NAME, overwrite=True)

print(f"GcsCredentials created: {doc_id}")

# Create or update Google Cloud Storage block
bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load(CREDENTIALS_BLOCK_NAME),
    bucket=BUCKET_GCP_NAME,
)

doc_id = bucket_block.save(BUCKET_BLOCK_NAME, overwrite=True)

print(f"GcsBucket created: {doc_id}")

# Create or update MySQL database block
dbhost = input("Enter MySQL hostname: ")
dbport = input("Enter MySQL port: ")
dbusername = input("Enter MySQL username: ")
dbpassword = input("Enter MySQL password: ")
dbname = input("Enter MySQL database name: ")

if not all([dbhost, dbport, dbusername, dbpassword, dbname]):
    print("Skipped creation of SqlAlchemyConnector block")
    exit()

connector = SqlAlchemyConnector(
    connection_info=ConnectionComponents(
        driver=SyncDriver.MYSQL_MYSQLDB,
        username=dbusername,
        password=dbpassword,
        host=dbhost,
        port=int(dbport),
        database=dbname,
    )
)

doc_id = connector.save(MYSQL_BLOCK_NAME, overwrite=True)

print(f"SqlAlchemyConnector for MySQL created: {doc_id}")
