from helpers.calculate_temperature import calculate_temperature
from helpers.get_data_from_database import pull_weather_data


def assign_boolean_to_coordinates(hi, low, min_lat, lat_increase, min_lon, lon_increase, startTime, endTime):
    values = []
    for i in range(min_lat,min_lat - lat_increase, -1):
        for j in range(min_lon, min_lon + lon_increase, 1):
            database_data = pull_weather_data(startTime, endTime, i, j)
            values.append(calculate_temperature(hi,low,database_data))
    return values

    