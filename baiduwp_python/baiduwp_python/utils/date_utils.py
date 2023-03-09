import time
from datetime import datetime


def get_datetime_now_str():
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")


def get_date_time_str(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt and isinstance(dt, datetime) else None


def get_date_now_str(fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.strftime(datetime.now(), fmt)


def get_datetime_from_str(time_str):
    try:
        return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return None


def get_datetime_start_end_str(dt_str):
    # "2022-04-20 18:18:26" => ("2022-04-20 00:00:00","2022-04-20 23:59:59")
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S") if isinstance(dt_str, str) else dt_str
        return dt.strftime("%Y-%m-%d 00:00:00"), dt.strftime("%Y-%m-%d 23:59:59")
    except Exception as e:
        pass


def get_datetime_num():
    return datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")


def time_to_stamp(time_data):
    if isinstance(time_data, str):
        struct_time = time.strptime(time_data, "%Y-%m-%d %H:%M:%S")
    elif isinstance(time_data, datetime):
        struct_time = time_data.timetuple()
    else:
        return
    return int(time.mktime(struct_time))
