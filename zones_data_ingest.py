from time import time
from sqlalchemy import create_engine
import pandas as pd
import argparse
import os


def data_load(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    file_name = os.path.basename(url)

    # download the csv
    # os system function can run command line arguments from Python
    os.system(f"wget {url}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # create the connection to the database engine to see if everything is working properly
    # engine.connect()

    t_start = time()

    zones = pd.read_csv(file_name)
    zones.to_sql(name=table_name, con=engine, if_exists='replace')

    t_end = time()

    print('Zones table is loaded in %.3f second(s)' % (t_end - t_start))

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

    # create the connection to the database engine to see if everything is working properly
    # engine.connect()

    data_load(args)


# URL="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"

# python zones_data_ingest.py \
#   --user=admin \
#   --password=admin \
#   --host=localhost \
#   --port=5432 \
#   --db=ny_taxi \
#   --table_name=zones \
#   --url="${URL}"