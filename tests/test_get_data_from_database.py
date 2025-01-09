from helpers.get_data_from_database import pull_weather_data
from dotenv import load_dotenv
import pytest
import os

load_dotenv()

#setting up DBURL to be test URL instead of actual URL 
DB_URL_TEST = os.getenv("DB_URL_TEST")

def test_get_data_from_database_response():
    """
    This is a test for pull_weather_data function to see if it can grab data from the test database. 
    """
    startTime = 1735270000
    endTime = 17352770001

    weather = pull_weather_data(DB_URL_TEST, startTime, endTime)
    assert weather[0] == (4, 1735270874, 87, 40, 109)

def test_get_data_from_database_sorted():
    """
    This method checks that the returned values from pull_weather_data are sorted by lat and lon
    """    
    startTime = 1735270000
    endTime = 17352770001
    weather = pull_weather_data(DB_URL_TEST, startTime, endTime)
    latLon = [(row[3],row[4]) for row in weather]
    assert latLon == sorted(latLon)

def test_get_data_from_database_invalid_times():
    """
    This checks if error is correctly thrown if start time is after end time
    """    
    startTime = 1735280001
    endTime = 1735280000
    with pytest.raises(ValueError, match="start time cannot be after end time"):
        pull_weather_data(DB_URL_TEST, startTime, endTime)

def test_get_data_from_database_no_matches():
    """
    Test to see if no data is returned for valid times that are not in the database
    """    
    startTime = 1735280000
    endTime = 1735280000
    weather = pull_weather_data(DB_URL_TEST, startTime, endTime)
    assert len(weather) == 0

def test_get_data_from_database_specific_match():
    """
    Test that database only pulls the correct data based on time values from the test database
    """    
    startTime = 1735270895
    endTime = 1735270895
    weather = pull_weather_data(DB_URL_TEST, startTime, endTime)
    assert weather[0] == (6, 1735270895, 87, 42, 108)