.PHONY: setup start


setup:
	@echo "# CREATING INFRASTRUCTURE WITH TERRAFORM..."
	cd terraform && terraform init && terraform apply -var project=${GCP_PROJECT_ID} && cd ..

	@echo "# BUILDING CONTAINERS..."
	docker compose build


start:
	@echo "# CREATING AND STARTING CONTAINERS..."
	docker compose up --detach

	@echo "# CREATING PREFECT BLOCKS..."
	docker compose run cli python -m blocks.make_blocks

stop:
	@echo "# DESTROYING CONTAINERS AND NETWORKS..."
	docker compose down

process:
	docker compose run cli python -m flows.etl_db_to_gcs

transfer:
	docker compose run cli python -m flows.etl_gcs_to_bq

transform:
	docker compose run dbt run
