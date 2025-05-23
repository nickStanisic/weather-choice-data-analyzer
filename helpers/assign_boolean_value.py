from helpers.calculate_temperature import calculate_temperature
from helpers.get_data_from_database import pull_weather_data
import itertools

def assign_boolean_to_coordinates(hi, low, start_time, end_time):
    """
    this function loops over lat, lon pairs and adds their calculated temperature to a list. 

    Args:
        hi (float): high temperature bound
        low (float): low temperature bound
        start_time (int): unix time to start looking at weather
        end_time (int): unix time to stop looking at weather

    Returns:
        list: list of dicts returned by calculate_temperature. For each lat, lon pair a tuple is added to the list
    """    
    values = []
    
    # Get database data (no longer need DBURL parameter)
    database_data = pull_weather_data(start_time, end_time)
    
    if database_data is None:
        return []
    
    # It is already ordered by lat, lon so iterate over lat, lon groups 
    for (lat, lon), group_iter in itertools.groupby(database_data, key=lambda row: (row[3], row[4])):
        # Turn group into a list
        group_list = list(group_iter)
        # Calculate if temperature for list is valid or not
        values.append(calculate_temperature(hi, low, group_list))
    
    return values