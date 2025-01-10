import datetime
import pytz

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

    # Define Colorado's timezone (Mountain Time)
    colorado_tz = pytz.timezone("America/Denver")

    try:
        # Attempt to convert the datetime string to a datetime object
        naive_dt = datetime.datetime.strptime(datetime_str, fmt)
        colorado_dt = colorado_tz.localize(naive_dt)
    except ValueError:
        raise ValueError(f"The provided datetime string '{datetime_str}' does not match the format '{fmt}'.")
    
    #creates unix timestamp and cast to int
    return int(colorado_dt.timestamp())
   