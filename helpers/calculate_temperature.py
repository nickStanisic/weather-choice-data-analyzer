def calculate_temperature(high, low, database_data):
    """ 
    This function calculates if the database temperatures are within the high and low specified.
    It loops over all rows in the database data. 
    This data should only be for one lat, lon pair but can have multiple times

    Args:
        high (int): The high temperature specified by user
        low (int): The low temperature specified by the user
        database_data (list): weather data for a given lat, lon pair. this is format (id, dt, temperature, lat, lon)

    Returns:
        dict: date, average temperature, lat, lon and valid information.
    """    
    #True if temperature is between high and low, False if temperature is found outside the range
    inside = True 

    #Two variables used for average temperature calculation
    temperature_average = 0
    count = 0

    if low > high:
        raise ValueError("low can't be bigger than high")
    #Check that each rows temperature is within high and low bounds
    for row in database_data:
        if row[2] > float(high) or row[2] < float(low):
            inside = False
        temperature_average += row[2]
        count += 1

    data = {
        "date": row[1],
        "average_temp": temperature_average/count,
        "lat": row[3],
        "lon": row[4],
        "valid": inside
    }

    return data