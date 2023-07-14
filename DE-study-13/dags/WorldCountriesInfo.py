from datetime import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook

import requests
import logging


def get_Redshift_connection(autocommit=True):
    hook=PostgresHook(postgres_conn_id='redshift_dev_db')
    conn=hook.get_conn()
    conn.autocommit=autocommit
    return conn.cursor()

@task
def get_world_infomations(url):
    response = requests.get(url)
    data = response.json()
    records = []

    for row in data:
        country = row['name']['official']
        population = row['population']
        area = float(row['area'])

        records.append([country, population, area])

    return records

@task
def load(schema, table, records):
    logging.info("load started")
    cur = get_Redshift_connection()

    try:
        cur.execute("BEGIN;")
        cur.execute(f"DROP TABLE IF EXISTS {schema}.{table};")
        cur.execute(f"""
CREATE TABLE {schema}.{table} (
    country varchar(100),
    population bigint,
    area float
);""")

        # ---
        for r in records:
            sql = f"INSERT INTO {schema}.{table} (country, population, area) VALUES (%s, %s, %s);"
            parameters = (r[0], r[1], r[2])
            cur.execute(sql, parameters)

        cur.execute("COMMIT;")
    
    except Exception as error:
        print(error)
        logging.error(error)
        cur.execute("ROLLBACK;")
        raise
    logging.info("load done")

with DAG(
    dag_id='WorldCountriesInfo',
    start_date=datetime(2023, 1, 20),
    catchup=False,
    tags=['API','4th_week'],
    schedule='30 6 * * 6'   # 매주 토요일 오전 6:30
) as dag:
    url = Variable.get("world_info_json_url")
    schema = 'phvalue123'
    table = 'world_infomation'

    results=get_world_infomations(url)
    load(schema, table, results)
