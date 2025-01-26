# Import SparkSession from PySpark
from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("TestSparkSession") \
    .getOrCreate()

# Print Spark version to confirm it's working
print(f"Spark Version: {spark.version}")

# Create a simple DataFrame
data = [("Alice", 29), ("Bob", 35), ("Cathy", 25)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data, columns)

# Show the DataFrame
print("Sample DataFrame:")
df.show()

# Perform a simple transformation (filter rows where Age > 30)
filtered_df = df.filter(df["Age"] > 30)

# Show the filtered DataFrame
print("Filtered DataFrame (Age > 30):")
filtered_df.show()

# Converting the filtered DataFrame to Pandas
print("Converting the filtered DataFrame to Pandas.")
print(filtered_df.toPandas())

# Stop the SparkSession
spark.stop()
