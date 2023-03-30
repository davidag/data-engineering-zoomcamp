.PHONY: setup start


setup:
	@echo "# CREATING INFRASTRUCTURE WITH TERRAFORM..."
	cd terraform && terraform init && terraform apply && cd ..

	@echo "# BUILDING AND RUNNING CONTAINERS FOR PREFECT..."
	docker compose build

	@echo "# CREATING PREFECT BLOCKS..."
	docker compose run cli python blocks/make_blocks.py

start:
	docker compose up --detach

process:
	docker compose run cli python flows/etl_db_to_gcs.py
