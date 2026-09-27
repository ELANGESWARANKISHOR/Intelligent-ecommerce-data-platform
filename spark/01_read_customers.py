from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("EcommerceDataPlatform")
    .master("local[2]")
    .getOrCreate()
)

print("Spark version:", spark.version)

customers = spark.read.parquet("data/raw/customers.parquet")

print("Number of customers:", customers.count())

print("\nSchema:")
customers.printSchema()

print("\nFirst 5 customers:")
customers.show(5, truncate=False)

spark.stop()