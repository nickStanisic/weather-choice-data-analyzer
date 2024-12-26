import datetime

def convert_to_unix(datetime_str):
    fmt = "%Y-%m-%dT%H:%M" 
    dt = datetime.datetime.strptime(datetime_str, fmt)
    unix_time = int(dt.timestamp())
    return unix_time