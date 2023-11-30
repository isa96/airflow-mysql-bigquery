from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, date, timedelta
# from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.utils.dates import days_ago
import os
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
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
dag = DAG('load_data',
          schedule_interval= '@daily',
          default_args= default_dag,
          description="Apache Airflow Testing DAG"
          )

BUCKET_NAME = ""
FILENAME = ""
gcp_conn_id = ""
schema = ""
destination_dataset_table = ""

gcs_to_gbq = GCSToBigQueryOperator(
        task_id="gcs_to_gbq", 
        bucket=BUCKET_NAME, 
        gcp_conn_id  = gcp_conn_id,
        source_objects=[FILENAME], 
        source_format="csv",
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_TRUNCATE",
        # schema_object=schema,
        destination_project_dataset_table=destination_dataset_table,
        dag=dag
    )
