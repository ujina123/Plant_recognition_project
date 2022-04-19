import requests
from mod.slackbot import Slack
import pendulum
import pandas as pd
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.branch import BaseBranchOperator


sb = Slack('#pipeline')
kst = pendulum.timezone('Asia/Seoul')

default_args = {
    "owner" : "admin",
    "depends_on_past" : False,
    "wait_for_downstream" : False,
    "retries" : 1,
    "retry_delay" : timedelta(minutes=10),
    "on_failure_callback" : sb.fail,
    "on_success_callbak" : sb.success,
}

dag = DAG(
    dag_id='Airflow',
    default_args=default_args,
    schedule_interval="0 * * * *",
    start_date=datetime(2022, 4, 17, tzinfo=kst),
    end_date=datetime(2022, 5, 14, tzinfo=kst),
    catchup=False
)

def path():
    t_now = datetime.now()
    t_6 = t_now.replace(hour=6, minute=0, second=0, microsecond=0)
    t_7 = t_now.replace(hour=7, minute=0, second=0, microsecond=0)
    t_18 = t_now.replace(hour=18, minute=0, second=0, microsecond=0)
    t_19 = t_now.replace(hour=19, minute=0, second=0, microsecond=0)
    if t_6 <= t_now < t_7 or t_18 <= t_now < t_19:
        task_id = 'path1'
    else:
        task_id = 'path2'
    return task_id

paths = ['path1', 'path2']

#=================================================
#                      Python                    #
#=================================================

check = BranchPythonOperator(
    task_id='check_path',
    python_callable=path,
    dag=dag
)

#=================================================
#                      Bash                      #
#=================================================

checkHDFS = BashOperator(
    task_id='checkHDFS',
    bash_command='echo "hello"',
    dag=dag
)

next_job = DummyOperator(
    task_id='next_job',
    trigger_rule='all_success',
    dag=dag,
)

for p in paths:
    dummy = DummyOperator(
        task_id=p,
        dag=dag
    )
    if p == 'path1':
        checkHDFS >> check >> dummy >> [weather, uv] >> next_job
    else:
        checkHDFS >> check >> dummy >> weather >> next_job
