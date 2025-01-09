import datetime

def convert_to_unix(datetime_str):
    """
    This function takes in a datetime string and returns an int that is the unix time equivalent. 

    Args:
        datetime_str (string): This is a string representing a date and time

    Returns:
        int: unix time equivalent to the datetime timestamp
    """    

    #specify format of datetime_str parameter
    fmt = "%Y-%m-%dT%H:%M"

    #converts datetime string to datetime object based on specified format 
    dt = datetime.datetime.strptime(datetime_str, fmt)

    #creates unix timestamp and cast to int
    unix_time = int(dt.timestamp())
    return unix_time