from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, date, timedelta
# from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.utils.dates import days_ago
import os
from airflow.providers.google.cloud.transfers.mysql_to_gcs import MySQLToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

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
dag = DAG('move_mysql_to_gbg',
          schedule_interval= '@daily',
          default_args= default_dag,
          description="Moving Data from MySQL to BigQuery"
          )

BUCKET_NAME = ""
SQL_QUERY = ""
FILENAME = ""
gcp_conn_id = ""
mysql_conn_id = ""
schema = ""
destination_dataset_table = ""

upload_mysql_to_gcs = MySQLToGCSOperator(
        task_id="mysql_to_gcs", 
        mysql_conn_id=mysql_conn_id,
        sql=SQL_QUERY, 
        bucket=BUCKET_NAME, 
        gcp_conn_id  = gcp_conn_id,
        filename=FILENAME, 
        export_format="json",
        # schema_filename=schema,
        dag=dag
    )

gcs_to_gbq = GCSToBigQueryOperator(
        task_id="gcs_to_gbq", 
        bucket=BUCKET_NAME, 
        gcp_conn_id  = gcp_conn_id,
        source_objects=[FILENAME], 
        source_format="NEWLINE_DELIMITED_JSON",
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_TRUNCATE",
        # schema_object=schema,
        destination_project_dataset_table=destination_dataset_table,
        dag=dag
    )


#Define task pipeline
upload_mysql_to_gcs>> gcs_to_gbq
