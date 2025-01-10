from helpers.calculate_temperature import calculate_temperature
from helpers.get_data_from_database import pull_weather_data
import itertools

def assign_boolean_to_coordinates(DBURL, hi, low, start_time, end_time):
    """
    this function loops over lat, lon pairs and adds their caculated temperature to a list. 

    Args:
        DBURL (string): This is the URL for the postgres Database
        hi (float): high temerature bound
        low (float): low temperature bound
        startTime (int): unix time to start looking at weather
        endTime (int): unix time to stop looking at weather

    Returns:
        list: list of dicts returned by calculate_temperature. For each lat, lon pair a tuple is added to the list
    """    
    values = []
    #get database data
    print(DBURL)
    database_data = pull_weather_data(DBURL, start_time, end_time)
    print(database_data, "HERE2")
    #it is already ordered by lat, lon so iterate over lat, lon groups 
    for (lat, lon), group_iter in itertools.groupby(database_data, key=lambda row: (row[3], row[4])):
        #turn group into a list
        group_list = list(group_iter)
        #calculate if temperature for list is valid or not
        values.append(calculate_temperature(hi,low,group_list))
    return values

    