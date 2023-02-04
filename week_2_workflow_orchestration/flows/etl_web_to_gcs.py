import argparse
from pathlib import Path

import pandas as pd
from prefect import flow, task, get_run_logger
from prefect_gcp.cloud_storage import GcsBucket


BUCKET_BLOCK_NAME = "zoom-gcs-week2"


@task(retries=3, log_prints=True)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url, parse_dates=[1, 2])
    print(f"Loaded csv with {df.shape[0]} rows and {df.shape[1]} columns")
    return df


@task()
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Nothing yet."""
    return df


@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"data/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path


@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load(BUCKET_BLOCK_NAME)
    gcs_block.upload_from_path(from_path=path, to_path=path)


@flow()
def etl_web_to_gcs(color: str, year: int, month: int) -> None:
    """The main ETL function"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load Taxi data into Google Cloud Storage')

    parser.add_argument('--color', type=str, required=True, help='Taxi color data')
    parser.add_argument('--year', type=int, required=True, help='Data year')
    parser.add_argument('--month', type=int, required=True, help='Data month')
    args = parser.parse_args()

    etl_web_to_gcs(args.color, args.year, args.month)
