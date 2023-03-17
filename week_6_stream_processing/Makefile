.PHONY: setup download producers

setup:
	pip install -r requirements.txt
	docker compose up -d

download:
	wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-01.csv.gz -O - | \
		gzip -d > data/fhv_tripdata_2019-01.csv
	wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz -O - | \
		gzip -d > data/green_tripdata_2019-01.csv
	wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv -O data/taxi_zone_lookup.csv

producers:
	python producer.py -f data/green_tripdata_2019-01.csv
	python producer.py -f data/fhv_tripdata_2019-01.csv
	python producer.py -f data/taxi_zone_lookup.csv
