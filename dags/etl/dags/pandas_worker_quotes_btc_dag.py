"""Módulo de execução de dags no Airflow para extração da cotação de BTC."""

import os
from datetime import datetime

from airflow import DAG  # type:ignore
from airflow.operators.bash import BashOperator  # type:ignore

BASE_DIR = os.path.dirname(__file__)

with DAG(
    dag_id="pandas_worker_quotes_btc_dag",
    start_date=datetime(2025, 10, 19),
    schedule="*/15 * * * *",
    catchup=False,
    tags=["quotes_btc"],
) as dag:

    run_worker = BashOperator(
        task_id="run_worker",
        bash_command=(
            f"export PYTHONPATH={BASE_DIR}/../src && "
            "python -m worker.quotes_btc.etl_quotes_btc_daily_event"
        ),
    )
