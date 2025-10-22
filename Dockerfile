FROM apache/airflow:2.8.3-python3.11

# Instala gosu, Java (necessário para PySpark) e curl
USER root
RUN apt-get update && \
    apt-get install -y gosu curl gcc python3-dev libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

COPY ./requirements.txt /opt/airflow/dags/

RUN pip install --no-cache-dir -r /opt/airflow/dags/requirements.txt

COPY ./dags/etl /opt/airflow/etl
