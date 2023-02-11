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

- Run flow to download fhv 2019 data:
```bash
$ python -m flows.etl_web_to_gcs --color fhv --year 2019
```

