from pyspark.sql import SparkSession


"""
Create a Spark session with optimized configurations to reduce CPU stress and manage heat:
    * master == local[6]:
        - Use all 6 cores out of my 8 total cores.
    * config:
        - spark.executor.memory == 32g:
            Assign 32 GB of RAM for Spark executors (ample memory remains).
        - spark.driver.memory == 16g:
            Assign 16 GB of RAM for the Spark driver (no change in allocation).
        - spark.executor.cores == 4:
            Use 4 cores per executor (reduced from 8 to lower CPU load/heat).
        - spark.task.cpus == 1:
            Each task uses 1 core.
        - spark.sql.adaptive.enabled == false:
            Disable Adaptive Query Execution for consistent performance
            and avoid CPU heat spikes.
        - spark.sql.shuffle.partitions == 12:
            Set shuffle partitions to 2-3x the # of available cores.
        - spark.sql.execution.arrow.enabled == true:
            Enable Arrow for toPandas() optimization, reducing CPU overhead
            during DataFrame conversion.
"""


def create_SparkSession():
    spark = (
        SparkSession.builder.appName("OptimizedSparkSession")
        .master("local[6]")
        .config("spark.executor.memory", "16g")
        .config("spark.driver.memory", "32g")
        .config("spark.sql.adaptive.enabled", "false")
        .config("spark.sql.shuffle.partitions", "216")
        .config("spark.sql.execution.arrow.pyspark.enabled", "false")
        .getOrCreate()
    )
    return spark
