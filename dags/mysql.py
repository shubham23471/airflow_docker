"""
Example use of MySql related operators.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.hooks.mysql_hook import MySqlHook



dag = DAG(
    'example_mysql_create_table',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 2, 24),
    default_args={'mysql_conn_id': 'mysql_connect'},
    tags=['mysql'],
    catchup=False
)


"function to create to create "

create_table_mysql_task = MySqlOperator(
    task_id='create_table_mysql', sql=r"""create table tutorials_tbl(
   tutorial_id INT NOT NULL AUTO_INCREMENT,
   tutorial_title VARCHAR(100) NOT NULL,
   tutorial_author VARCHAR(40) NOT NULL,
   submission_date DATE,
   PRIMARY KEY ( tutorial_id )
            );""", 
            dag=dag
)

create_table_mysql_task 

"creating mysql table from external sql file"

# mysql_task = MySqlOperator(
#     task_id='create_table_mysql_external_file',
#     sql='/scripts/drop_table.sql',
#     dag=dag,
# )

# # [END howto_operator_mysql_external_file]

# drop_table_mysql_task >> mysql_task
