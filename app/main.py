from time import sleep
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    ceil,
    lit,
    col,
    desc,
    to_date,
    months_between,
    current_date,
    explode,
    trim,
    length,
)
from pyspark.ml.feature import StopWordsRemover, Tokenizer

# Initialisation de la SparkSession
spark = (
    SparkSession.builder
    .appName("project")
    .master("spark://spark-master:7077")
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY")
    .getOrCreate()
)

# .master("local[*]") \

# Lecture du fichier
data_file = "app/data/full.csv"
df = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .csv(data_file)
)

cleaned_df = df.dropna()

# Question 1
most_commit_df = (
    cleaned_df.groupBy("repo").count().orderBy("count", ascending=False).show(10)
)

# Question 2
best_contributor = (
    cleaned_df.where(col("repo") == "apache/spark")
    .groupBy("Author")
    .count()
    .withColumnRenamed("count", "commits")
    .orderBy(desc("commits"))
    .show(1)
)

# Question 3
date_format_pattern = "EEE MMM dd HH:mm:ss yyyy Z"
best_contributors = (
    cleaned_df.where(col("repo") == "apache/spark")
    .withColumn("true_date", to_date(col("date"), date_format_pattern))
    .filter(ceil(months_between(current_date(), col("true_date")) / lit(12)) <= 4)
    .groupBy("Author")
    .count()
    .withColumnRenamed("count", "commits")
    .orderBy(desc("commits"))
    .show()
)

# Question 4
tokenizer = Tokenizer(inputCol="message", outputCol="word")
tokenized = tokenizer.transform(cleaned_df).select("word")

remover = StopWordsRemover(inputCol="word", outputCol="filtered")
most_used_words = (
    remover.transform(tokenized)
    .select(explode(col("filtered")).alias("single_words"))
    .filter(length(trim(col("single_words"))) > 0)
    .groupBy("single_words")
    .count()
    .withColumnRenamed("count", "occurences")
    .orderBy(desc("occurences"))
    .show(10)
)

sleep(1000)
