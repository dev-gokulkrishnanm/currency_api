from __future__ import annotations
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.append('/home/caretaker/Desktop/api')
from pipeline import run_etl

default_args = {
    'owner' : 'airflow',
    'retries' : 1,
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retry_delay' : timedelta(minutes=5),
}

with DAG(
    dag_id='currency_pipeline_dag',
    default_args=default_args,
    description='Fetch currency rate',
    schedule='@hourly',
    start_date=datetime.now(),
    catchup=False,
    tags=['currency','api','etl'],
) as dag:
    
    etl_task=PythonOperator(
        task_id='run_etl',
        python_callable=run_etl
    )

run_etl