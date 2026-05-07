#!/bin/bash

set -e # The script stops immediately at the first failure. Every line after it is only reached if everything before succeeded.
LOGFILE="$HOME/Documents/devops/project-python/deploy.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

trap 'echo "[$(date "+%Y-%m-%d %H:%M:%S")] deployment failed at line $LINENO" >> "$LOGFILE"' ERR

# check if containers are running and log the result.
echo "[$TIMESTAMP]  Starting deployment...." >> $LOGFILE
git pull origin multi-container-setup
docker compose build --no-cache
docker compose down

docker compose up -d
echo "Waiting for MongoDB to be healthy..."
until [ "$(docker inspect --format='{{.State.Health.Status}}' project-python-mongodb-1)" == "healthy" ]; do
    sleep 2
done
echo "[$(date '+%Y-%m-%d %H:%M:%S')] MongoDB status: HEALTHY" >> $LOGFILE
echo "[$(date '+%Y-%m-%d %H:%M:%S')] devcheck status: STARTED" >> $LOGFILE
echo "[$(date '+%Y-%m-%d %H:%M:%S')] nginx status: STARTED" >> $LOGFILE

echo "--- Deployment complete --- " >> $LOGFILE
