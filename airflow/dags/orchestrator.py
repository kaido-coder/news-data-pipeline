import sys
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
from docker.types import Mount

sys.path.append('/opt/airflow/api-request')

def safe_main_callable():
    from insert_records import main
    return main()

default_args = {
    'description': 'A DAG to orchestrate data',
    'start_date': datetime(2026, 4, 1)
}

dag = DAG(
    dag_id="news-api-orchestrator",
    default_args = default_args,
    schedule = timedelta(minutes = 1),
    catchup = False
)

with dag:
    task1 = PythonOperator(
        task_id='ingest_data_task',
        python_callable=safe_main_callable
    )

    task2 = DockerOperator(
        task_id = 'dbt_transform_task',
        image = 'ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command = 'run',
        working_dir = '/usr/app',
        mounts = [
            Mount(source='/home/sardor/fintech/fintech-data-pipeline/dbt/my_project', target='/usr/app', type='bind'),
            Mount(source='/home/sardor/fintech/fintech-data-pipeline/dbt/profiles.yml', target='/root/.dbt/profiles.yml', type='bind')
        ],
        network_mode = 'fintech-data-pipeline_my-network', 
        docker_url = 'unix://var/run/docker.sock', 
        auto_remove = 'success',
        user = 'root' 
    )

    task1 >> task2



