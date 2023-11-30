# Airflow-MySQL-To-BigQuery

## How to use

1. Install requirements libraries using this command ```pip install -r requirements.txt```
2. In Airflow you need to add connection for ```gcp_conn_id``` and ```mysql_conn_id```. 
3. in [etl.py](etl.py), filled ```BUCKET_NAME```, ```SQL_QUERY```, ```FILENAME```, ```gcp_conn_id```, ```mysql_conn_id```, ```schema```, ```destination_dataset_table```
4. Then you can just run the airflow and the dags

Then finally, you have moved your data from MySQL into BigQuery.


