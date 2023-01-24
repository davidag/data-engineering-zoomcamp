## Homework

- start containers
```
    docker compose up -d
```
- ingest green taxi data
```
    URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"
    docker run --network=pg-network taxi_ingest:v001 \
      --user=root \
      --password=root \
      --host=pgdatabase \
      --port=5432 \
      --db=ny_taxi \
      --table_name=green_taxi_trips \
      --url=${URL}
```
- connect to postgres from host
```
    pgcli -h localhost -p 5432 -u root ny_taxi
```
- query count records on given day
```
    select count(*)
      from green_taxi_trips
      where lpep_pickup_datetime >= '2019-01-15 00:00'
        and lpep_dropoff_datetime < '2019-01-16 00:00';
```
- query day with the largest trip using pickup time for calculations
```
    select date_trunc('day', lpep_pickup_datetime) as day,
           max(trip_distance) as max_distance
      from green_taxi_trips
      group by day
      order by max_distance desc;
```
- query number of trips with 2 or 3 passengers on 2019-01-01
```
    select passenger_count passengers,
           count(*) num_trips
      from green_taxi_trips
     where date_trunc('day', lpep_pickup_datetime) = '2019-01-01 00:00'
     group by passenger_count
     order by passenger_count;
```
- query drop up zone with largest tip for passengers picked up in the Astoria Zone
```
    select dropoff."Zone" do_zone,
           max(t.tip_amount) max_tip
    from green_taxi_trips t
            join zones pickup
              on t."PULocationID" = pickup."LocationID"
            join zones dropoff
              on t."DOLocationID" = dropoff."LocationID"
    where pickup."Zone" = 'Astoria'
    group by do_zone
    order by max_tip desc
    limit 10;

    -- Some dropoff Boroughs are Unknown and Zone is null for them.
    select dropoff.*
    from green_taxi_trips t
            join zones pickup
              on t."PULocationID" = pickup."LocationID"
            join zones dropoff
              on t."DOLocationID" = dropoff."LocationID"
    where pickup."Zone" = 'Astoria' and dropoff."Zone" is null;
```
