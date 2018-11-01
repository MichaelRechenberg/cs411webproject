# Create a decorator that will return a string of the error and 
#   HTTP 500 for use while debugging

import functools
import mysql.connector


def report_db_error(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except mysql.connector.Error as err:
            return str(err), 500

    return wrapper


