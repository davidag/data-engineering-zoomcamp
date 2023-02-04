# Homework solutions

## Setup infrastructure

**Local**

- Activate your local Python virtual environment and install dependencies:

```python
pip install -r requirements.txt
```

**Google Cloud**

- Create resources using Terraform:

```bash
$ export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
$ cd terraform
$ terraform init
$ terraform apply
```

**Prefect**

- Create Prefect blocks

```bash
$ python blocks/make_gcp_blocks.py
```

- Run Orion UI

```bash
$ prefect orion start
```
- Run agent on default queue:

```bash
$ prefect agent start -q default
```

## Question 1: Loading January 2020 data

- Run flow:
```bash
$ python -m flows.etl_web_to_gcs --color green --year 2020 --month 1
...
13:39:47.833 | INFO    | Task run 'fetch-b4598a4a-0' - Loaded csv with 447770 rows and 20 columns
...
```
## Question 2: Scheduling with Cron

- Create deployment using Python:
```bash
$ python -m deployments.make_web_to_ecs_deployment
Created deployment scheduled for: [2023-03-01T05:00:00+00:00, 2023-04-01T05:00:00+00:00, 2023-05-01T05:00:00+00:00, ...]
```
## Question 3: Loading data to BigQuery

- Load data from web to gcs:
```bash
$ python -m flows.etl_web_to_gcs --color yellow --year 2019 --month 2
$ python -m flows.etl_web_to_gcs --color yellow --year 2019 --month 3
```

- Create deployment using Python:
```bash
$ python -m deployments.make_ecs_to_bq_deployment
Registered with API: 9cda8bc7-67f0-484d-ac53-e4a22f8f0a19
```

- Run deployment:
```bash
$ prefect deployment run --id 9cda8bc7-67f0-484d-ac53-e4a22f8f0a19
Creating flow run for deployment 'etl-gcs-to-bq/green-2019-02..03'...
Created flow run 'micro-raccoon'.
└── UUID: 259a0dfc-0712-41dd-ae65-54985ff0f601
└── Parameters: {'color': 'yellow', 'year': 2019, 'months': [2, 3]}
└── Scheduled start time: 2023-02-04 16:58:16 CET (now)
└── URL: <no dashboard available>
```
