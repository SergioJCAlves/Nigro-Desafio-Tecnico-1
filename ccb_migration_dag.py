from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from migration_script import migrate_data 

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 11),
    'email': ['sergio.maxpayne@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ccb_migration',
    default_args=default_args,
    description='Migração de dados CCB',
    schedule_interval=timedelta(days=1),
    catchup=False
)

migrate_task = PythonOperator(
    task_id='migrate_ccb_data',
    python_callable=migrate_data,
    dag=dag,
)