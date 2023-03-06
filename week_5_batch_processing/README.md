# Week 5: Batch Processing

## Prerequistes

- How many trips were started on June 15th?

```
df.filter(F.to_date(df.pickup_datetime) == '2021-06-15').count()
```

- How long is the longest trip in the dataset?

```
df \
    .withColumn('trip_duration', (df.dropoff_datetime - df.pickup_datetime).cast("integer") / 60.0 / 60.0) \
    .agg(F.max('trip_duration')) \
    .show()
```

- What is the most frequent pickup location zone?

```
df_zones = spark.read.csv("taxi_zone_lookup.csv", "LocationID INT, Borough STRING, Zone STRING, ServiceZone STRING")
df_zones.registerTempTable("zones")

df.registerTempTable("trips_data")

df_result = spark.sql("""
	select td.PULocationID, first(z.Zone), count(*)
	from trips_data td join zones z
	on td.PULocationID = z.LocationID
	group by td.PULocationID
	order by 3 desc
	""").show()
```
