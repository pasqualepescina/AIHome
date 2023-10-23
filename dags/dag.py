from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from Tecnocasa.tecnocasa_main import scrape_tecnocasa_url

default_args = {
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG('AIHOME', default_args=default_args, schedule_interval=None)

start = DummyOperator(task_id='start', dag=dag)

Tecnocasa_scrapper = PythonOperator(
    task_id='Scrapper_tecnocasa',
    python_callable=scrape_tecnocasa_url,
    dag=dag,
)

start >> Tecnocasa_scrapper
if __name__ == "__main__":
    dag.cli()
