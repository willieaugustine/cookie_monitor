from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("CookieMonitor") \
    .getOrCreate()

# Make robot ears listen to the walkie-talkie
orders = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "cookie_orders") \
    .load()
