# SETUP

## Install dependencies
- create a directory called data inside the app directory and put in the data file
  - data (full.csv): https://www.kaggle.com/datasets/dhruvildave/github-commit-messages-dataset

## Run the app
- Launch docker container : `docker-compose up -d`
- Connect to the master container : `docker exec -it spark-master bash`
- Launch the cluster : `sh /app/run.sh`

## Monitoring
- You can monitor what the jobs on this url : [localhost:4040](http://localhost:4040/)
- On your terminal where you launched the cluster you can check prints of the data processing.
