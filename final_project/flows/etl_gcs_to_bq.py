from io import BytesIO
from pathlib import Path

import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

from . import constants as c


@task(log_prints=True)
def extract_from_gcs() -> dict[str, BytesIO]:
    """Download data from GCS"""
    # load bucket block from Prefect
    gcs_block = GcsBucket.load(c.BUCKET_BLOCK_NAME)

    # Download all existing blobs from data/ folder
    blobs = gcs_block.list_blobs("data")

    buffers = {}
    for blob in blobs:
        print(f"Loading file '{blob.name}' from Cloud Storage...")
        buf = BytesIO()
        gcs_block.download_object_to_file_object(blob.name, buf)

        filename = Path(blob.name).stem
        buffers[filename] = buf
    return buffers


@task()
def transform(buffers: dict[str, BytesIO]) -> dict[str, pd.DataFrame]:
    """Load DataFrame without any transformation"""
    dataframes = {}
    for name, buf in buffers.items():
        dataframes[name] = pd.read_parquet(buf)
    return dataframes


@task(log_prints=True)
def write_bq(table_name: str, df: pd.DataFrame):
    """Write DataFrames to BiqQuery"""
    gcp_credentials_block = GcpCredentials.load(c.CREDENTIALS_BLOCK_NAME)

    destination_table = f"{c.DATASET_NAME}.{table_name}"
    print(f"Uploading table '{destination_table}' to BigQuery...")

    df.to_gbq(
        destination_table=destination_table,
        project_id=c.PROJECT_ID,
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="replace",
    )


@flow(log_prints=True)
def etl_gcs_to_bq():
    """Main ETL flow to load data into BigQuery"""
    buffers = extract_from_gcs()

    dataframes = transform(buffers)

    for name, df in dataframes.items():
        write_bq(name, df)


if __name__ == "__main__":
    etl_gcs_to_bq()
