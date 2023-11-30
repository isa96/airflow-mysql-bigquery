from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, date, timedelta
# from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.utils.dates import days_ago
import os
from airflow.providers.google.cloud.transfers.mysql_to_gcs import MySQLToGCSOperator
# from airflow.contrib.operators.mysql_to_gcs import MySqlToGoogleCloudStorageOperator
# from airflow.operators.dummy import DummyOperator

#dag arguments
default_dag = {
    "owner": "Felix Pratamasan",
    "start_date": days_ago(1),
    "email": ["felixpratama242@gmail.com"],
    "email_on_failure": True,
    "email_on_entry": True,
    "retries":1,
    "retry_delay": timedelta(hours=1)
}

#define dag
dag = DAG('extract_data',
          schedule_interval= '@daily',
          default_args= default_dag,
          description="Apache Airflow Testing DAG"
          )

BUCKET_NAME = ""
SQL_QUERY = ""
FILENAME = ""
gcp_conn_id = ""
mysql_conn_id = ""
schema = ""

upload_mysql_to_gcs = MySQLToGCSOperator(
        task_id="mysql_to_gcs", 
        mysql_conn_id=mysql_conn_id,
        sql=SQL_QUERY, 
        bucket=BUCKET_NAME, 
        gcp_conn_id  = gcp_conn_id,
        filename=FILENAME, 
        export_format="csv",
        # schema_filename=schema,
        dag=dag
    )