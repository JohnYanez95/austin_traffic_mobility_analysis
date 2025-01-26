from functools import wraps
from datetime import datetime
from typing import Callable


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
