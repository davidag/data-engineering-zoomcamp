import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(f'postgresql://root:root@localhost:5432/ny_taxi')

df = pd.read_csv("./data/taxi_zone_lookup.csv")

df.to_sql(name="zones", con=engine, if_exists='replace')
