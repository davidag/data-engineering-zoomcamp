# Week 6: Stream Processing

## Setup

- Install Python libraries and start Kafka broker and ksqlDB server
```
make setup
```
- Download data from fhv and green datasets for 2019-01
```
make download
```

## Run producers

- Run producers for the green and fhv datasets sequentially that will create one topic per dataset
```
make producers
```

## Create streams using ksqlDB

- Start ksqldb-cli to execute sql statements in the terminal

```
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088
```

- Create stream with trip zone information:

```sql
CREATE STREAM taxiZoneLU (
  locationid INT KEY,
  borough STRING,
  zone STRING,
  service_zone STRING
  )
  WITH (KAFKA_TOPIC='taxi_zone_lookup', FORMAT='DELIMITED', partitions=1);
```

- Create stream for the green dataset

```sql
CREATE STREAM greenTripdata (
  key STRING KEY,
  pu_datetime STRING,
  do_datetime STRING,
  flag STRING,
  rateid INT,
  pulocationid INT,
  dolocationid INT,
  passenger_count INT,
  distance DOUBLE,
  fare_amount DOUBLE,
  extra DOUBLE,
  mta_tax DOUBLE,
  tip_amount DOUBLE,
  tolls_amount DOUBLE,
  ehail_fee DOUBLE,
  improv_surcharge DOUBLE,
  total_amount DOUBLE,
  payment_type INT,
  trip_type INT,
  congest_surcharge DOUBLE
  )
  WITH (KAFKA_TOPIC='green_tripdata_2019-01', FORMAT='DELIMITED', partitions=1);
```

- Create stream for the fhv dataset

```sql
CREATE STREAM fhvTripdata (
  key STRING KEY,
  pu_datetime STRING,
  do_datetime STRING,
  pulocationid INT,
  dolocationid INT,
  sr_flag STRING,
  affiliated_base_num STRING
  )
  WITH (KAFKA_TOPIC='fhv_tripdata_2019-01', FORMAT='DELIMITED', partitions=1);
```

- Create a new stream that will contain entries from both original streams

```sql
CREATE STREAM allTripdata (
  key STRING KEY,
  pu_datetime STRING,
  do_datetime STRING,
  pulocationid INT,
  dolocationid INT
  )
  WITH (KAFKA_TOPIC='all_tripdata_2019-01', FORMAT='DELIMITED', partitions=1);
```

- Make sure we're reading from the beginning of the streams

```sql
SET 'auto.offset.reset' = 'earliest';
```

- Insert all data from the green and fhv streams into the new all tripdata

```sql
INSERT INTO allTripdata SELECT key, pu_datetime, do_datetime, pulocationid, dolocationid FROM greenTripdata;
INSERT INTO allTripdata SELECT key, pu_datetime, do_datetime, pulocationid, dolocationid FROM fhvTripdata;
```

- Create a persistent query over the allTripdata stream

```sql
CREATE TABLE topTripdata AS
	SELECT a.pulocationid, t.zone, count(*)
	FROM allTripdata a JOIN taxiZoneLU t WITHIN 1 DAY ON a.pulocationid = t.locationid
	WHERE pulocationid IS NOT null
	GROUP BY a.pulocationid, t.zone
	EMIT CHANGES;
```

- Show top pickup location ids for all tripdata from 2019-01

```bash
docker exec -it ksqldb-cli ksql --output JSON --execute "select * from toptripdata" -- http://ksqldb-server:8088 | jq -n '[inputs | .columns | { zone: .[1], count: .[2] }] | sort_by(.count)' | tail

  },
  {
    "zone": "East Village",
    "count": 276933
  },
  {
    "zone": "NV",
    "count": 779457
  }
]
```

## Useful commands

- Delete topic
```
docker exec broker /bin/kafka-topics --delete --topic green_tripdata_2019-01 --bootstrap-server broker:9092
```
- Delete stream with ksql
```sql
DROP STREAM name;
```

## References

- https://docs.ksqldb.io/en/latest/reference/serialization/#delimited
- https://developer.confluent.io/tutorials/merge-many-streams-into-one-stream/ksql.html

