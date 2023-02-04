import argparse
from typing import List
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

# Prefect constants
BUCKET_BLOCK_NAME = "zoom-gcs-week2"
CREDENTIALS_BLOCK_NAME = "zoom-gcp-creds"

# Google Cloud constants
DATASET_NAME = "trips_data_week2"
TABLE_NAME = "ny_trips"
PROJECT_ID = "dtc-de-375612"


@task()
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}_tripdata_{year}-{month:02}.parquet"

    # load bucket block from Prefect
    gcs_block = GcsBucket.load(BUCKET_BLOCK_NAME)

    # use default working directory as local_path, temp folder when run in a deployment
    gcs_block.get_directory(from_path=gcs_path)

    local_path = Path(gcs_path)
    if not local_path.exists():
        raise FileNotFoundError(f"File not found in bucket: {local_path}")

    return local_path


@task()
def transform(path: Path) -> pd.DataFrame:
    """Load DataFrame without any transformation"""
    return pd.read_parquet(path)


@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""
    gcp_credentials_block = GcpCredentials.load(CREDENTIALS_BLOCK_NAME)
    df.to_gbq(
        destination_table=f"{DATASET_NAME}.{TABLE_NAME}",
        project_id=PROJECT_ID,
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="replace",
    )


@flow(log_prints=True)
def etl_gcs_to_bq(color: str, year: int, months: List[int]):
    """Main ETL flow to load data into Big Query"""
    total_rows = 0

    for month in months:
        print(f"Processing month {month:02}...")

        path = extract_from_gcs(color, year, month)
        df = transform(path)
        write_bq(df)

        total_rows += df.shape[0]

    print(f"Total rows processed: {total_rows}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load Taxi data into Google Cloud Storage')

    parser.add_argument('--color', type=str, required=True, help='Taxi color data')
    parser.add_argument('--year', type=int, required=True, help='Data year')
    parser.add_argument('--months', type=str, required=True, help='Comma-separated list of months')
    args = parser.parse_args()

    etl_gcs_to_bq(args.color, args.year, [int(m) for m in args.months.split(",")])
