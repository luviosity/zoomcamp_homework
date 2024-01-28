from time import time
from sqlalchemy import create_engine, inspect
import pandas as pd
import argparse
import os


def data_transform(df):
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

def data_load(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url


    # download the csv
    # os system function can run command line arguments from Python
    os.system(f"wget {url}")

    file_name = os.path.basename(url)

    if file_name.endswith('.gz'):
        os.system(f"gunzip {file_name}")
        file_name = file_name[:-3]

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # create the connection to the database engine to see if everything is working properly
    # engine.connect()

    inspector = inspect(engine)

    csv_chunks = pd.read_csv(file_name, chunksize=100000)

    table_exists = True if inspector.has_table(table_name) else False

    for chunk in csv_chunks:
        # pass the engine variable to get_schema function
        # Pandas will execute the schema SQL statement using the engine connection we have defined
        # pd.io.sql.get_schema(df, name="yellow_taxi_data", con=engine)
        t_start = time()

        data_transform(chunk)

        if not table_exists:
            chunk.to_sql(table_name, engine, if_exists='replace')
            table_exists = True
        else:
            chunk.to_sql(table_name, engine, if_exists='append')

        t_end = time()

        print('Inserted another chunk... took %.3f second(s)' % (t_end - t_start))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    parser.add_argument('--user', help="user name for postgres")
    parser.add_argument('--password', help="password for postgres")
    parser.add_argument('--host', help="host for postgres")
    parser.add_argument('--port', help="port for postgres")
    parser.add_argument('--db', help="database name for postgres")
    parser.add_argument('--table_name', help="name of the table where we will write the results to")
    parser.add_argument('--url', help="url of the CSV")

    args = parser.parse_args()

    data_load(args)


# URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"

# python trip_data_ingest.py \
#   --user=admin \
#   --password=admin \
#   --host=localhost \
#   --port=5432 \
#   --db=ny_taxi \
#   --table_name=yellow_taxi_trips \
#   --url="${URL}"