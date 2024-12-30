import pytest
from helpers.calculate_temperature import calculate_temperature

def test_is_temp_good_within_range():
    """Test is_temp_inside function with temperatures within the specified range."""
    db_data = [
        (1, 1, 20.0, 39.0, -105.5),
        (2, 2, 25.0, 40.0, -106.0)
    ]
    low = 15.0
    high = 30.0

    result = calculate_temperature(high, low, db_data)

    print(result)
    assert(result['valid'] == True)

def test_is_temp_above_range():
    """Test if function with temperatures above the specified range are False."""
    db_data = [
        (1, 1, 40.0, 39.0, -105.5),
        (2, 2, 25.0, 40.0, -106.0)
    ]
    low = 15.0
    high = 30.0

    result = calculate_temperature(high, low, db_data)

    assert(result['valid'] == False)

def test_is_temp_below_range():
    """Test if function with temperatures below the specified range are marked as False."""
    db_data = [
        (1, 1, -40.0, 39.0, -105.5),
        (2, 2, 25.0, 40.0, -106.0)
    ]
    low = 15.0
    high = 30.0

    result = calculate_temperature(high, low, db_data)

    assert(result['valid'] == False)