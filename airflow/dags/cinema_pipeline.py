from airflow import DAG
from datetime import datetime, timedelta
import os
import shlex
import sys

try:
    from airflow.providers.standard.operators.bash import BashOperator
    from airflow.providers.standard.operators.python import PythonOperator
except ImportError:
    from airflow.operators.bash import BashOperator
    from airflow.operators.python import PythonOperator

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts')))

from data_generator import load_data_to_dwh

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# airflow/dags/ -> корінь репозиторію -> cinema_dbt
DBT_PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'cinema_dbt'))
DBT_PROFILES_DIR = DBT_PROJECT_DIR

with DAG(
    'cinema_elt_pipeline',
    default_args=default_args,
    description='Конвеєр завантаження та трансформації даних онлайн-кінотеатру',
    schedule='@daily',
    catchup=False
) as dag:

    extract_load_task = PythonOperator(
        task_id='extract_and_load_raw_data',
        python_callable=load_data_to_dwh
    )

    dbt_run_task = BashOperator(
        task_id='dbt_run_transformations',
        bash_command=f'dbt run --project-dir {shlex.quote(DBT_PROJECT_DIR)} --profiles-dir {shlex.quote(DBT_PROFILES_DIR)}'
    )

    dbt_test_task = BashOperator(
        task_id='dbt_test_models',
        bash_command=f'dbt test --project-dir {shlex.quote(DBT_PROJECT_DIR)} --profiles-dir {shlex.quote(DBT_PROFILES_DIR)}'
    )

    extract_load_task >> dbt_run_task >> dbt_test_task
