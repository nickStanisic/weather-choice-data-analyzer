import pytest
from helpers.calculate_temperature import calculate_temperature

def test_is_temp_good_within_range():
    """
    Test temperatures when temperatures in db_data are within high and low
    """    
    db_data = [
        (1, 1, 20.0, 39.0, -105.5),
        (2, 2, 25.0, 40.0, -106.0)
    ]
    low = 15.0
    high = 30.0

    result = calculate_temperature(high, low, db_data)

    assert(result['valid'] == True)

def test_is_temp_above_range():
    """
    Test calculate_temperature for cases where a temperature is higher than the high given. 
    """
    db_data = [
        (1, 1, 40.0, 39.0, -105.5),
        (2, 2, 25.0, 40.0, -106.0)
    ]
    low = 15.0
    high = 30.0

    result = calculate_temperature(high, low, db_data)

    assert(result['valid'] == False)

def test_is_temp_below_range():
    """
    Test calculate_temperature to assess if valid is false for temperatures below the low given. 
    """
    db_data = [
        (1, 1, -40.0, 39.0, -105.5),
        (2, 2, 25.0, 40.0, -106.0)
    ]
    low = 15.0
    high = 30.0

    result = calculate_temperature(high, low, db_data)

    assert(result['valid'] == False)