import datetime
from datetime import datetime, timedelta
import time
import pytz


def epoc_to_datetime(date_in):
    return datetime.fromtimestamp(float(date_in)/1000).strftime('%Y-%m-%d %H:%M:%S')


def date_sub_c(date_in, interval):
    return datetime.strptime(date_in, '%Y-%m-%d %H:%M:%S') - timedelta(days=interval)


def date_add_minutes(date_in, interval):
    return datetime.strptime(date_in, '%Y-%m-%d %H:%M:%S') - timedelta(minutes=interval)


def date_add_c(interval):
    return datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")) + timedelta(days=interval)


def datetime_to_str(date_in):
    return datetime.strptime(date_in, '%Y-%m-%d %H:%M:%S')


def format_time(time_input):
    return time_input.strftime('%Y%m%d%H%M%S')


def get_timestamp():
    ts = time.time()
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def timestamp_to_str_time():
    """
    convert timestamp to time str: %Y-%m-%d %H:%M:%S
    :return: str
    """
    ts = time.time()
    return datetime.fromtimestamp(ts).strftime('%H:%M:%S')


def date_sub_from_now(time_zone, interval):
    """
    add date with interval day from now
    :param time_zone: str
    :param interval: int
    :return:
    """
    return datetime.now(pytz.timezone(time_zone)) - timedelta(days=interval)


def date_add_from_now(time_zone, interval):
    """
    add date with interval day from now
    :param time_zone:
    :param interval:
    :return:
    """
    return datetime.now(pytz.timezone(time_zone)) + timedelta(days=interval)


def format_timestamp_to_str_time():
    """
    convert timestamp to time str: %Y-%m-%d %H:%M:%S
    :return: str
    """
    ts = time.time()
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def timestamp_to_str_time_format1():
    """
    convert timestamp to time str: %Y-%m-%d %H:%M:%S
    :return: str
    """
    ts = time.time()
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')


def compare_2date(d1, d2):
    """
    compare 2 date
    :param d1: str
    :param d2: str
    :return: boolean
    """
    d1 = datetime.strptime(d1, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.strptime(d2, '%Y-%m-%d %H:%M:%S')
    return True if d1 <= d2 else False


def compare_2date_2(d1, d2):
    return True if d1 <= d2 else False


def sub_2date(d1, d2):
    """
    sub 2 date
    :param d1: str
    :param d2: str
    :return: elapsed_time (datetime object), you can elapsed_time.total_seconds() to convert total seconds
    """
    # d1 = datetime.strptime(d1, '%Y-%m-%d %H:%M:%S')
    # d2 = datetime.strptime(d2, '%Y-%m-%d %H:%M:%S')
    elapsed_time = d1 - d2
    return elapsed_time.total_seconds()


def datetime_to_unix():
    present_date = datetime.now()
    unix_timestamp = datetime.timestamp(present_date) * 1000
    return unix_timestamp