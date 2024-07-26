"""
Module for handling default date values in KN Trading Django web application.

This module provides a function to retrieve default date values for start, end,
and specific dates to be used in various views of the web application.

Functions:
    - default_dates(request): Returns a dictionary containing default date values.

Dependencies:
    - datetime: Module for working with dates and times.
"""
from datetime import datetime, timedelta

# pylint: disable=unused-argument.
def default_dates(request):
    """
    Returns a dictionary containing default date values for start, end, and specific date.

    The default start date is set to seven days before the current date.
    The default end date is set to the current date.
    The default specific date is set to an empty string.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary containing default date values with keys:
            - 'default_start_date' (str): The default start date in 'YYYY-MM-DD' format.
            - 'default_end_date' (str): The default end date in 'YYYY-MM-DD' format.
            - 'default_specific_date' (str): An empty string for the specific date.
    """
    return {
        'default_start_date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
        'default_end_date': datetime.now().strftime('%Y-%m-%d'),
        'default_specific_date': '',
    }
