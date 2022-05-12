#!/bin/bash

if [ -z $(jps | grep ResourceManager) ] || [ -z $(jps | grep NodeManager) ]
then
    echo "Not Running"; start-yarn.sh
else
    echo "Running"
fi

if [ -z $(jps | grep NameNode) ] || [ -z $(jps | grep DataNode) ]
then
    echo "Not Running"; start-dfs.sh
else
    echo "Running"
fi
