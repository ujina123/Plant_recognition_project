# JngMkk
from pythonfiles.slackbot import Slack
import pendulum
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

sb = Slack('#pipeline')
kst = pendulum.timezone('Asia/Seoul')

default_args = {
    "owner" : "admin",
    "depends_on_past" : False,
    "wait_for_downstream" : False,
    "retries" : 1,
    "retry_delay" : timedelta(minutes=15),
    "on_failure_callback" : sb.fail,
    "on_success_callbak" : sb.success,
}

dag = DAG(
    dag_id='Airflow',
    default_args=default_args,
    schedule_interval="0 * * * *",
    start_date=datetime(2022, 5, 10, tzinfo=kst),
    end_date=datetime(2022, 5, 15, tzinfo=kst),
    catchup=False
)

#=================================================
#                      Go                        #
#=================================================

getWeather = BashOperator(
    task_id="getWeather",
    bash_command="/home/ubuntu/go/src/github.com/JngMkk/foreWeather",
)

#=================================================
#                      HDFS                      #
#=================================================

checkHDFS = BashOperator(
    task_id='checkHDFS',
    bash_command="""
                    if [ -z $(jps | grep "ResourceManager") ] || [ -z $(jps | grep NodeManager) ]
                    then echo "Not Running"; start-yarn.sh
                    else echo "Running"
                    fi

                    if [ -z $(jps | grep "NameNode") ] || [ -z $(jps | grep "DataNode") ]
                    then echo "Not Running"; start-dfs.sh
                    else echo "Running"
                    fi
                """
)

putHDFS = BashOperator(
    task_id="putHDFS",
    bash_command="hdfs dfs -put -f /home/ubuntu/finalproject/dags/data/weather.csv /home/data/"
)

#=================================================
#                      Spark                     #
#=================================================

weatherSpark = SparkSubmitOperator(
    task_id="weatherSpark",
    application="/home/ubuntu/finalproject/dags/spark/weather_2.12-0.1.0-SNAPSHOT.jar",
    conn_id="spark_default",
    dag=dag
)