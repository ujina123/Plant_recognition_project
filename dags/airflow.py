# JngMkk
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

#=================================================
#                      Python                    #
#=================================================

#=================================================
#                      Bash                      #
#=================================================

checkHDFS = BashOperator(
    task_id='checkHDFS',
    bash_command='echo "hello"',
    dag=dag
)
