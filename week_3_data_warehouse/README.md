# Homework solution

## Setup

- Create bucket and big query dataset using Terraform:
```bash
$ cd terraform
$ terraform init
$ terraform apply
```

- Create Prefect block representing the Storage Bucket:
```bash
$ python blocks/make_gcp_blocks.py
```

- Run flow to upload fhv 2019 data to the GCS bucket without using local storage:
```bash
$ python -m flows.etl_web_to_gcs --color fhv --year 2019
```
- Create external table using all 2019 data:
```sql
CREATE OR REPLACE EXTERNAL TABLE `nyc_dataset.fhv_tripdata_2019_external`
OPTIONS (
  format = 'CSV',
  uris = ['gs://data-warehouse-week3_dtc-de-375612/fhv_tripdata_2019-*.csv.gz']
);
```
- Create table using all 2019 data:
```sql
CREATE OR REPLACE TABLE nyc_dataset.fhv_tripdata_2019 AS
SELECT * FROM nyc_dataset.fhv_tripdata_2019_external;
```
## Question 1
```sql
-- Count vehicle trip records for FHV data in 2019
SELECT count(*) AS trip_records FROM nyc_dataset.fhv_tripdata_2019;
```

## Question 2
```sql
-- Count distinct number of affiliated_base_number in external table (0 MB estimated processing)
SELECT distinct(Affiliated_base_number) FROM nyc_dataset.fhv_tripdata_2019_external;

-- Count distinct number of affiliated_base_number in materialized table (317.94 MB estimated processing)
SELECT distinct(Affiliated_base_number) FROM nyc_dataset.fhv_tripdata_2019;
```

## Question 3
```sql
-- Count records that have both a blank (null) PUlocationID and DOlocationID
SELECT count(*) AS unknown_locations_count FROM nyc_dataset.fhv_tripdata_2019 WHERE PULocationID IS NULL and DOLocationID IS NULL;
```

## Question 4

What is the best strategy to optimize the table if query always filter by `pickup_datetime` and order by `affiliated_base_number`?

We can partition by `pickup_datetime` and cluster by `affiliated_base_number`. This allows pruning of partitions that do not match the date interval and having the data clustered by affiliated base names inside each partition.

## Question 5
```sql
-- Create partitioned and clustered table
CREATE OR REPLACE TABLE nyc_dataset.fhv_tripdata_2019_ps
PARTITION BY DATE(pickup_datetime)
CLUSTER BY Affiliated_base_number AS
SELECT * FROM nyc_dataset.fhv_tripdata_2019;

-- Query to retrieve the distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive)
-- ref: https://cloud.google.com/bigquery/docs/reference/standard-sql/operators#comparison_operators

-- Estimated: 647.87 MB
SELECT DISTINCT(Affiliated_base_number) FROM nyc_dataset.fhv_tripdata_2019 WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';

-- Estimated: 23.05 MB
SELECT DISTINCT(Affiliated_base_number) FROM nyc_dataset.fhv_tripdata_2019_ps WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';
```
## Question 6

[External tables using external data sources keep data in the corresponding source](https://cloud.google.com/bigquery/docs/external-data-sources)

> External tables are similar to standard BigQuery tables, in that these tables store their metadata and schema in BigQuery storage. However, their data resides in an external source.

## Question 7

Typically, clustering does not offer significant performance gains on tables less than 1 GB.

