from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime

import requests
import logging

def get_Redshift_connection(autocommit=True):
    hook = PostgresHook(postgres_conn_id='redshift_dev_db')
    conn = hook.get_conn()
    conn.autocommit = autocommit
    return conn.cursor()

@task
def extract(**country):
    request = requests.get('https://restcountries.com/v3/all')
    countries = request.json()
    data = []
    for country in countries:
        name = country['name']['common']
        pop = country['population']
        area = country['area']
        data.append([name, pop, area])
    return data

@task
def load(schema, table, records):
    logging.info("load started")
    cur = get_Redshift_connection()
    try:
        cur.execute("BEGIN;")
        cur.execute(f"DROP TABLE IF EXISTS {schema}.{table};")
        cur.execute(f"""
CREATE TABLE {schema}.{table} (
    name varchar(256) primary key,
    population int,
    area float
);
""")
        # DELETE FROM을 먼저 수행 -> FULL REFRESH을 하는 형태
        for r in records:
            sql = f"INSERT INTO {schema}.{table} VALUES ('{r[0]}', {r[1]}, {r[2]});"
            print(sql)
            cur.execute(sql)
        cur.execute("COMMIT;")   # cur.execute("END;")
    except Exception as error:
        print(error)
        cur.execute("ROLLBACK;")
        raise

    logging.info("load done")

with DAG(
    dag_id = 'CountryInfo',
    start_date = datetime(2023,5,30),
    catchup = False,
    tags = ['API'],
    schedule = '30 6 * * 6'  # 매주 토요일 6시 30분에 실행
) as dag:
    results = extract()
    load("plays0708", "CountryInfo", results)