from helpers.calculate_temperature import calculate_temperature
from helpers.get_data_from_database import pull_weather_data
import itertools

def assign_boolean_to_coordinates(DBURL, hi, low, startTime, endTime):
    values = []
    database_data = pull_weather_data(DBURL, startTime, endTime)
    
    for (lat, lon), group_iter in itertools.groupby(database_data, key=lambda row: (row[3], row[4])):
        group_list = list(group_iter)
        values.append(calculate_temperature(hi,low,group_list))
    return values

    