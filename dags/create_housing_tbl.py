from asyncio import tasks
from datetime import datetime, timedelta
from warnings import catch_warnings
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import pandas as pd 
import sqlalchemy


dag = DAG(
    'create_housing_tbl',
    start_date=datetime(2022, 2, 24),
    schedule_interval=timedelta(days=1),
    default_args={'mysql_conn_id' : 'musql_connect'},
    tags=['mysql'],
    catchup=False
)

uri = 'mysql+pymysql://root:example@host.docker.internal/classicmodels'
engine = sqlalchemy.create_engine(uri)


def create_table(engine, **kwargs):
    print('Creating housing table')
    engine.execute("""
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
            """)

# def preprocessing(input_file, **kwargs):
#     housing_df = pd.read_csv('/opt/bitnami/airflow/dags/house-prices.csv')
#     housing_df.columns = [col.lower() for col in housing_df.columns]
#     print(housing_df.columns)

# '/opt/bitnami/airflow/dags/house-prices.csv'
def load_table(uri, input_file, table_name,  **kwargs):
    housing_df = pd.read_csv(input_file)
    housing_df.columns = [col.lower() for col in housing_df.columns]   
    housing_df.to_sql(name=table_name,
                con=uri,
                if_exists='append',
                 index=False)


create_housing_table = PythonOperator(
                            task_id='create_housing_table',
                            provide_context=True,
                            python_callable=create_table,
                            op_kwargs={'engine': engine},
                            dag=dag)

load_housing_table = PythonOperator(
                            task_id='load_housing_table',
                            provide_context=True,
                            python_callable=load_table,
                            op_kwargs={'uri': uri,
                                        'input_file' : '/opt/bitnami/airflow/dags/house-prices.csv',
                                        'table_name' : 'house_price'
                                        },
                            dag=dag)


create_housing_table >> load_housing_table