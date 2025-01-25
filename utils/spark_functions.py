from functools import wraps
from datetime import datetime
from pyspark.sql import SparkSession
from typing import Callable

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


def inject_logging(function: Callable):
    @wraps(function)
    def wrap(*args, **kwargs):
        # Determine if the function is a method (i.e., first argument is 'self')
        if args and hasattr(args[0], "__dict__"):
            instance = args[0]
            logging = kwargs.pop("logging", getattr(instance, "logging", True))
        else:
            logging = kwargs.pop("logging", True)

        # Check if this is a nested call
        if getattr(wrap, "_is_nested", False):
            return function(*args, **kwargs)

        # Indicate that nested calls are happening
        wrap._is_nested = True

        # Record the start time
        start_datetime = datetime.now()

        try:
            result = function(*args, **kwargs)
            failed_run = False
        except Exception as e:
            failed_run = True
            result = None
            error_message = str(e)

        # Record the end time
        end_datetime = datetime.now()

        # Calculate run time
        run_time = end_datetime - start_datetime
        hours, remainder = divmod(run_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Format start and end times
        start_string = start_datetime.strftime("%m/%d/%Y, %H:%M:%S")
        end_string = end_datetime.strftime("%m/%d/%Y, %H:%M:%S")

        # Format Keyword Arguments if logging is enabled
        key_string = ""
        if logging and kwargs:
            max_key_len = max(len(k) for k in kwargs.keys())
            key_format = "                 - {:" + str(max_key_len) + "} : {}\n"
            key_string = "".join([key_format.format(k, v) for k, v in kwargs.items()])

        # Construct log message
        if logging:
            log_message = (
                f"Function       : {function.__name__}\n"
                f"Input(s)       :\n{key_string or '                 - No keyword arguments'}\n"
                f"Run Time       : {hours:02} hour(s) : {minutes:02} minute(s) : {seconds:02} second(s)\n"
                f"Start Time     : {start_string}; End Time: {end_string}\n"
                f"Run Successful : {not failed_run}\n"
            )
            print(log_message)

        # Reset nested flag
        wrap._is_nested = False

        if failed_run:
            raise RuntimeError(
                f"Function '{function.__name__}' failed with error: {error_message}"
            )

        return result

    return wrap
