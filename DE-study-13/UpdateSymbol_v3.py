from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
from pandas import Timestamp

import yfinance as yf
import pandas as pd
import logging


def get_Redshift_connection(autocommit=True):
    hook = PostgresHook(postgres_conn_id='redshift_dev_db')
    conn = hook.get_conn()
    conn.autocommit = autocommit
    return conn.cursor()


@task
def get_historical_prices(symbol):
    ticket = yf.Ticker(symbol)
    data = ticket.history()
    records = []

    for index, row in data.iterrows():
        date = index.strftime('%Y-%m-%d %H:%M:%S')
        records.append([date, row["Open"], row["High"], row["Low"], row["Close"], row["Volume"]])

    return records


def _create_table(cur, schema, table, drop_first):
    if drop_first:
        cur.execute(f"DROP TABLE IF EXISTS {schema}.{table};")
    cur.execute(f"""
CREATE TABLE IF NOT EXISTS {schema}.{table} (
    date date,
    "open" float,
    high float,
    low float,
    close float,
    volume bigint,
    created_date timestamp default GETDATE()
);""")


@task
def load(schema, table, records):
    logging.info("load started")
    cur = get_Redshift_connection()

    create_t_sql = f"CREATE TEMP TABLE t AS SELECT * FROM {schema}.{table};"

    # -----create table, dump
    try:
        cur.execute("BEGIN;")
        # 원본 테이블이 없으면 생성 - 테이블이 처음 한번 만들어질 때 필요한 코드
        _create_table(cur, schema, table, False)
        # 임시 테이블로 원본 테이블을 복사
        cur.execute(create_t_sql)
        cur.execute("COMMIT;")
    except Exception as error:
        print(error)
        cur.execute("ROLLBACK;") 
        raise

    # -----insert to temp
    try: 
        # 임시 테이블에 데이터 입력
        for r in records:
            t_insert_sql = f"INSERT INTO t VALUES ('{r[0]}', {r[1]}, {r[2]}, {r[3]}, {r[4]}, {r[5]});"
            cur.execute(t_insert_sql)
        cur.execute("COMMIT;") 
    except Exception as error:
        print(error)
        cur.execute("ROLLBACK;") 
        raise

    # -----기존 테이블 대체
    alter_sql = f"""DELETE FROM {schema}.{table};
    INSERT INTO {schema}.{table}
    SELECT date, "open", high, low, close, volume 
    FROM ( SELECT *, ROW_NUMBER() OVER (PARTITION BY date ORDER BY created_date DESC) seq FROM t )
    WHERE seq = 1;;
    """
    try:
        cur.execute(alter_sql)
        cur.execute("COMMIT;")
    except Exception as e:
        print(error)
        cur.execute("ROLLBACK;")
        raise


with DAG(
    dag_id = 'UpdateSymbol_v3',
    start_date = datetime(2023,5,30),
    catchup=False,
    tags=['API','5th_week'],
    schedule = '0 10 * * *'
) as dag:

    results = get_historical_prices("AAPL")
    load("phvalue123", "stock_info_v3", results)
