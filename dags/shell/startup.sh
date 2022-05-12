#!/bin/bash

nohup /home/ubuntu/.local/bin/airflow webserver > /tmp/airflow_webserver.log 2>&1 &

nohup /home/ubuntu/.local/bin/airflow scheduler > /tmp/airflow_scheduler.log 2>&1 &

if [ -z $(jps | grep Elasticsearch) ]
then
    /home/ubuntu/elasticsearch-7.16.2/bin/elasticsearch -d
else
    "Running"
