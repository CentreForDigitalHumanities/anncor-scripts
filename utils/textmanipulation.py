"""
    This file should contain custom functions that are used to manipulate strings
"""
from datetime import date
import time


def prepend_zeros(length, string):
    """
    Prepend zeros to the string until the desired length is reached
    :param length: the length that the string should have
    :param string: the string that we should appends 0's to
    :return: A string with zeros appended
    """
    return "{}{}".format("0" * (length - len(string)), string)


dates = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12
}


def datestring_to_timestamp(date_string):
    """
    Converts the string containing a date to a timestamp: the string is of the following format
    day-month-year, where day and year are a number and month is a three letter acronym
    :param date_string:
    :return: a timestamp
    """
    ar = date_string.split("-")
    d = date(int(ar[2]), dates[ar[1]], int(ar[0]))
    return time.mktime(d.timetuple())
