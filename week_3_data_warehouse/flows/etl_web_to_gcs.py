import argparse
from pathlib import Path

import requests

from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


BUCKET_BLOCK_NAME = "zoom-gcs-bucket"


@task()
def write_gcs_from_url(dataset_url: str, dataset_file: str) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load(BUCKET_BLOCK_NAME)
    r = requests.get(dataset_url, stream=True)
    gcs_block.upload_from_file_object(r.raw, dataset_file)


@flow()
def etl_web_to_gcs(color: str, year: int, months: list[int]) -> None:
    """The main ETL function"""
    for month in months:
        print(f"Processing month {month:02}...")
        dataset_file = f"{color}_tripdata_{year}-{month:02}.csv.gz"
        dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}"
        write_gcs_from_url(dataset_url, dataset_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load Taxi data into Google Cloud Storage')

    parser.add_argument('--color', type=str, required=True, help='Taxi color data')
    parser.add_argument('--year', type=int, required=True, help='Data year')
    parser.add_argument('--months', type=str, required=False, help='Comma-separated list of months. All months if ommitted.')
    args = parser.parse_args()

    if args.months:
        months = [int(m) for m in args.months.split(",")]
    else:
        months = [i for i in range(1, 12 + 1)]

    etl_web_to_gcs(args.color, args.year, months)
