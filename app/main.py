from sre_parse import WHITESPACE
from time import sleep
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, desc, to_date, months_between, current_date, explode, split, trim, length

spark = SparkSession \
    .builder \
    .appName("project") \
    .master("local[*]") \
    .config("spark.sql.legacy.timeParserPolicy","LEGACY") \
    .getOrCreate()

    #.master("spark://spark-master:7077") \

data_file = "/app/data/full.csv"
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(data_file , format="csv")

df.printSchema()

#Question 1
cleaned_df = df.dropna()
most_commit_df = cleaned_df.groupBy("repo") \
   .count() \
   .orderBy(desc("count")) \
   .show(10)

#Question 2
best_contributor = df.where(col("repo") == "apache/spark") \
   .groupBy("Author") \
   .count() \
   .withColumnRenamed("count", "commits") \
   .orderBy(desc("commits")) \
   .show(1)
        
#Question 3
date_format_pattern = "EEE MMM dd HH:mm:ss yyyy Z"
best_contributors = df.where(col("repo") == "apache/spark") \
    .withColumn(
        "true_date", 
        to_date(col("date"), date_format_pattern)
         ) \
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
stop_words_file = "/app/data/englishST.txt"
stop_words = spark.read \
    .load(stop_words_file , format="text")
WHITESPACE = ' '

most_repeated_words = df.withColumn('word', explode(split(col('message'), WHITESPACE)))\
    .filter(length(trim(col('word'))) > 0)\
    .join(stop_words, col("word") == stop_words.value, 'left_anti')\
    .groupBy("word") \
    .count() \
    .withColumnRenamed("count", "occurrences") \
    .orderBy(desc("occurrences")) \
    .show(10)

sleep(1000)