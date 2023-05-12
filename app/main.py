from time import sleep
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, col, desc, to_date, months_between, current_date



# Initialisation de la SparkSession
spark = SparkSession \
    .builder \
    .appName("project") \
    .master("local[*]") \
    .config("spark.sql.legacy.timeParserPolicy","LEGACY") \
    .getOrCreate()
    

  #.master("spark://spark-master:7077") \

 # Lecture du fichier
data_file = "/app/data/full.csv"

df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(data_file , format="csv")

df.printSchema()

cleaned_df = df.dropna()

#Question 1
most_commit_df = cleaned_df.groupBy("repo") \
   .count() \
   .orderBy("count", ascending=False) \
   .show(10)

#Question 2
best_contributor = cleaned_df.where(col("repo") == "apache/spark") \
   .groupBy("Author") \
   .count() \
   .withColumnRenamed("count", "commits") \
   .orderBy(desc("commits")) \
   .show(1)
        
#Question 3
date_format_pattern = "EEE MMM dd HH:mm:ss yyyy Z"
best_contributors = df.where(col("repo") == "apache/spark") \
    .withColumn("true_date", to_date(col("date"), date_format_pattern)) \
    .filter(
        months_between(
            current_date(),
            col("true_date"))
            <= 48) \
    .groupBy("Author") \
    .count() \
    .withColumnRenamed("count", "commits") \
    .orderBy(desc("commits")) \
    .show()

# Question 4
# J'AI AJOUTER DU CODE MERDE
        
  









sleep(1000)