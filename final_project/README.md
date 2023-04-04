# Dataeng Zoomcamp 2023 - Final Project

:rotating_light: *This my Data Engineering Zoomcast 2023 project, meaning that some decisions were made based on the [review criteria provided](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/9d9a3f0/week_7_project/README.md#peer-review-criteria).* :rotating_light:

## Problem description

One of my lifetime goals is helping people quit smoking. For that purpose, I created a non-profit forum and journaling website in 2001. It's still online and can be browsed here (in Spanish): https://miluchacontraeltabaco.com It contains thousands of messages with tips, experiences and motivational words.

Content is divided in two types: journal entries and forum posts. Both types can have associated comments. We want to show analytics related to this content, e.g. word counts, common words, number of comments, forum category, date & time, etc.

## Dataset

The website runs on [Drupal CMS](https://www.drupal.org/) using a MySQL database which is in the order of the hundreds of megabytes. The data is split into multiple tables and includes content, configuration and metadata, including [personally identifiable information (PII)](https://en.wikipedia.org/wiki/PII).

Because raw data cannot be made public for privacy reasons, a dataset containing only anonymous information is provided in the `data/` folder. This data set is composed of multiple parquet files which are generated with a [Prefect flow](./flows/etl_db_to_gcs.py).

Content is provided in the form of [stems](https://www.nltk.org/howto/stem.html) generated using [NLTK](https://www.nltk.org/index.html), after [tokenizing](https://www.nltk.org/api/nltk.tokenize.html#nltk.tokenize.word_tokenize) the original user-generated texts.

## Technologies

- Docker, for running applications
- Google Cloud Storage (GCS), as data lake
- Google Cloud BigQuery (GCBQ), as data warehouse
- Terraform, for IaC
- Prefect, for workflow orchestration

## Data pipeline

1. Process: `etl_db_to_gcs.py`
	- Extract raw data from a MySQL database, clean and preprocess the data, and save as parquet files.
	- Upload parquet files to **data lake** in Google Cloud Storage.
2. Transfer: `etl_gcs_to_bq.py`
	- Download parquet files from **data lake** and load them in memory as a Pandas DataFrame.
	- Create tables in **data warehouse** in Google Cloud BigQuery.

## Clustering and Partitioning

*Note: our data is smaller than 1GB so probably these techniques won't improve our queries, but it's implemented in order to meet the project evaluation criteria.*

**Partitioning**

- It might be beneficial to partition by year because I'm going to filter by year.
- Because the tables have a `created` timestamp column, we create a [time-unit partition](https://cloud.google.com/bigquery/docs/partitioned-tables#date_timestamp_partitioned_tables) on it.
- The tables `nodes` and `comments` have a yearly partitioned column defined in `terraform/main.tf`

**Clustering**

- Partitioning granularity and number of partitions is enough for our case, so we don't need clustering.

## Folder structure

- `blocks/`: Prefect blocks. Enable the storage of configuration and provide an interface for interacting with external systems. Used in `make setup` to create the initial configuration.
- `data/`: Dataset files in parquet format.
- `docker/`: Dockerfile used to run Prefect flows.
- `flows/`: Python files defining Prefect flows.
- `terraform/`: Terraform files defining Google Cloud resources.

## Instructions

### Prerequisites

- Google Cloud
	- Empty project created
	- Service account with Storage and BigQuery permissions created
	- Service account key locally installed in: `~/.secrets/gcp-zoomcamp-credentials.json`
- Terraform installed
- Export the following shell variables using your specific configuration:

```
$ export GCP_PROJECT_ID="<your google cloud project id>"
```

### Pipeline execution

1. Run `make setup` to create the Google Cloud infrastructure and build the Docker containers.

2. Run `make start` to run the Docker containers and create the Prefect blocks leaving *empty* all MySQL-related configuration.

3. Run `make process` to upload the dataset parquet files to the data lake (i.e. Cloud Storage).

4. Run `make transfer` to upload the dataset data to BigQuery with a one-to-one mapping of files and tables.

## Glossary

Node
: A node in Drupal CMS is any piece of individual content, like a forum post or a blog entry.

Comment
: A comment associated with a node.

## FAQ

- Error when making Prefect blocks: `httpx.ConnectError: All connection attempts failed`?
	- Try `make stop && make start`, and check if you can run the code inside a bash shell: `docker compose run cli /bin/bash` (`python blocks/make_blocks.py`).

## Next steps

- Create a Prefect deployment and run from cloud in order to update the source data daily.

## References

**Datasets**

- [New York Times frontpage articles dataset (inspiration)](https://components.one/datasets/above-the-fold)

**Google Cloud**

- [Python Client for BigQuery](https://github.com/googleapis/python-bigquery)
- [Partitioned tables on BigQuery](https://cloud.google.com/bigquery/docs/partitioned-tables)

**Prefect and Pandas**

- [Prefect GCP Docs](https://prefecthq.github.io/prefect-gcp/cloud_storage/)
- [Prefect 2 with Docker Compose](https://github.com/rpeden/prefect-docker-compose)
- [SQL queries in Pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-sql)

