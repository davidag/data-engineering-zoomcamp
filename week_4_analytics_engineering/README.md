# Week 4: Analytics Engineering

## Prerequisites

1. Use week 3 Prefect flow to upload all ny taxi data to a GCS bucket:
```bash
$ python -m flows.etl_web_to_gcs --color fhv --year 2019
$ python -m flows.etl_web_to_gcs --color yellow --year 2019
$ python -m flows.etl_web_to_gcs --color yellow --year 2020
$ python -m flows.etl_web_to_gcs --color green --year 2019
$ python -m flows.etl_web_to_gcs --color green --year 2020
```
2. Create external tables in BigQuery for the three types of taxi data:
```sql
CREATE OR REPLACE EXTERNAL TABLE `nyc_dataset.fhv_tripdata_ext`
OPTIONS (
  format = 'CSV',
  uris = ['gs://data-warehouse_dtc-de-375612/fhv_tripdata_2019-*.csv.gz']
);

CREATE OR REPLACE EXTERNAL TABLE `trips_data_all.yellow_tripdata_ext`
OPTIONS (
  format = 'CSV',
  uris = ['gs://data-warehouse_dtc-de-375612/yellow_tripdata*.csv.gz']
);

CREATE OR REPLACE EXTERNAL TABLE `trips_data_all.green_tripdata_ext`
OPTIONS (
  format = 'CSV',
  uris = ['gs://data-warehouse_dtc-de-375612/green_tripdata*.csv.gz']
);
```
3. Create tables in BigQuery from the external tables (no partitioning or clustering):
```sql
CREATE OR REPLACE TABLE nyc_dataset.fhv_tripdata_2019 AS
SELECT * FROM nyc_dataset.fhv_tripdata_2019_ext;

CREATE OR REPLACE TABLE trips_data_all.yellow_tripdata AS
SELECT * FROM trips_data_all.yellow_tripdata_ext;

CREATE OR REPLACE TABLE trips_data_all.green_tripdata AS
SELECT * FROM trips_data_all.green_tripdata_ext;
```
## Homework

```sql
-- Question 1
SELECT count(*) FROM `dtc-de-375612.dbt_dataset.fact_trips` where extract(year from pickup_datetime) in (2019, 2020);

-- Question 3
SELECT count(*) FROM `dtc-de-375612.dbt_dataset.stg_fhv_tripdata` where extract(year from pickup_datetime) = 2019;

-- Question 4
SELECT count(*) FROM `dtc-de-375612.dbt_dataset.fact_fhv_trips` where extract(year from pickup_datetime) = 2019;
```
