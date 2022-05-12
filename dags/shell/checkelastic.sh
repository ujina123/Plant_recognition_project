#!bin/bash

if [ -z $(jps | grep Elasticsearch) ]
then
    echo "Not Running"; $HOME/elasticsearch-7.16.2/bin/elasticsearch -d
else
    echo "Running"
fi
