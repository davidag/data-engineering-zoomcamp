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

1. *(run only if no parquet files exist, requires access to MySQL database)* Extract raw data from a MySQL database and create parquet files with anonymized data.
2. Create parquet files and upload them to data lake.

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
	- Service account key locally installed in: `~/secrets/gcp-zoomcamp-credentials.json`
- Terraform installed

### Setup

- Run `make setup` leaving *empty* all MySQL-related configuration.

- Run `make start` to launch the Prefect Server available at `http://127.0.0.1:4200`

- Run `make process` to upload dataset parquet files to data lake (i.e. GCS).

## Glossary

Node
: A node in Drupal CMS is any piece of individual content, like a forum post or a blog entry.

Comment
: A comment associated with a node.

## Next steps

- Create a Prefect deployment and run from cloud in order to update the source data daily

## References

- [Prefect 2 with Docker Compose](https://github.com/rpeden/prefect-docker-compose)
- [SQL queries in Pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-sql)
- [New York Times frontpage articles dataset (inspiration)](https://components.one/datasets/above-the-fold)
