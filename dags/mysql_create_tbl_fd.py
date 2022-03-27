"""
create mysql table from csv
MySqlHook : not working rn only ingest one columns leaving other blank
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.hooks.mysql_hook import MySqlHook
import pandas as pd 



dag = DAG(
    'mysql_create_tbl_fd',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 2, 24),
    default_args={'mysql_conn_id': 'mysql_connect'},
    tags=['mysql'],
    catchup=False
)


def bulk_load(table_name, local_filepath, **kwargs):
    print("Connecting to MYSQL")
    print('mysql_connect')
    conn = MySqlHook(mysql_conn_id='mysql_connect')
    print('Starting bulk load')
    conn.bulk_load(table_name,local_filepath)
    # return table_name
    
def preprocess_data(local_filepath, **kwargs):
    house_price_df = pd.read_csv(local_filepath)
    house_price_df.columns = [col.lower() for col in house_price_df.columns]
    house_price_df.to_csv('/opt/bitnami/airflow/dags/house_price2.csv', index=False)
    print('CSV written after preprocessing')


""" 
    Add to connection from UI in Json form 
    { "local_infile": true}

"""

create_housing_tbl = MySqlOperator(task_id='create_housing_table',
                                    sql=r"""
                                        create table if not exists classicmodels.house_price(
                                                home int(5), 
                                                price int(20), 
                                                sqft int(2), 
                                                bedrooms int(2), 
                                                bathrooms int(2),
                                                offers int(2), 
                                                brick char(10),
                                                neighborhood char(10)
                                                );
                                        """,
                                        dag=dag)

preprocess_csv = PythonOperator(task_id='preprocess_csv',
                                provide_context=True,
                                python_callable=preprocess_data,
                                op_kwargs={'local_filepath':'/opt/bitnami/airflow/dags/house-prices.csv'},
                                dag=dag)

load_housing_tbl = PythonOperator(
                        task_id='load_housing_tbl',
                        provide_context=True,
                        python_callable=bulk_load,
                        op_kwargs={'table_name':'house_price', 'local_filepath':'/opt/bitnami/airflow/dags/house_price2.csv'},
                        dag=dag)


create_housing_tbl >> preprocess_csv >> load_housing_tbl