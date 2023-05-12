# SETUP

## Install dependencies
- Install depency from requirements.txt
- create a directory called data inside the app directory and put in the data files
  - stopwords (englishST.txt): https://www.kaggle.com/datasets/rtatman/stopword-lists-for-19-languages?select=englishST.txt
  - data (full.csv): https://www.kaggle.com/datasets/dhruvildave/github-commit-messages-dataset

## Run the app
- Launch docker container : `docker-compose up -d`
- Connect to the master container : `docker exec -it spark-master bash`
- Launch the cluster : `/spark/bin/spark-submit /app/main.py`