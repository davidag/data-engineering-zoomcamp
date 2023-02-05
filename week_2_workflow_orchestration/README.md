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
## Question 4: GitHub Storage Block

- Load data from web to gcs:
```bash
$ python -m flows.etl_web_to_gcs --color green --year 2020 --month 11
```

- Create GitHub storage block using Python:

```bash
$ python blocks/make_github_block.py
```

- Create deployment using the GitHub block:
	- **Important**: This must be run in the root of the GitHub repo!

```bash
$ prefect deployment build ./week_2_workflow_orchestration/flows/etl_gcs_to_bq.py:etl_gcs_to_bq --name "github-deployment" --tag week-2 --storage-block github/de-zoomcamp-personal-repo

$ prefect deployment apply etl_gcs_to_bq-deployment.yaml
Successfully loaded 'github-deployment'
Deployment 'etl-gcs-to-bq/github-deployment' successfully created with id
'd7a4438c-8b31-41bd-b855-fa4763a78bf7'.
```

- Run deployment parameterized for Green data for November 2020:

```bash
$ prefect deployment run --params '{"color": "green", "year": 2020, "months": [11]}' etl-gcs-to-bq/github-deployment
```
