import pytest
from helpers.assign_boolean_value import assign_boolean_to_coordinates
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL_TEST = os.getenv("DB_URL_TEST")

def test_boolean_response_for_different_values(db_connection, populate_test_data):
    """
    This tests if correct outputs are received given different valid inputs.
    This is more of an integration test as this function calls both calculate_temperature and 
    get_data_from_database.
    """    
    #in range tests 
    hi = 87
    lo = -10
    start = 1735270873
    end = 1735270875
    response = assign_boolean_to_coordinates(DB_URL_TEST, hi, lo, start, end)
    assert(len(response) == 3)
    #first in list
    assert(response[2]["date"] == 1735270874)
    assert(response[2]["average_temp"] == 6.5)
    assert(response[2]["lat"] == 41)
    assert(response[2]["lon"] == 110)
    assert(response[2]["valid"] == True)
    #second in list
    assert(response[1]["date"] == 1735270874)
    assert(response[1]["average_temp"] == 76)
    assert(response[1]["lat"] == 41)
    assert(response[1]["lon"] == 109)
    assert(response[1]["valid"] == True)
    #third in list
    assert(response[0]["date"] == 1735270874)
    assert(response[0]["average_temp"] == 87)
    assert(response[0]["lat"] == 40)
    assert(response[0]["lon"] == 109)
    assert(response[0]["valid"] == True)

    hi = 76
    lo = 76
    start = 1735270894
    end = 1735270894
    response = assign_boolean_to_coordinates(DB_URL_TEST, hi, lo, start, end)
    assert(response[0]["date"] == 1735270894)
    assert(response[0]["average_temp"] == 76)
    assert(response[0]["lat"] == 41)
    assert(response[0]["lon"] == 109)
    assert(response[0]["valid"] == True)

def test_assign_boolean_values_invalid_inputs(db_connection,populate_test_data):
    """
    This function gives incorrect inputs and sees if correct errors are thrown
    """    
    #end comes before start
    hi = 75
    lo = 74
    start = 1735270897
    end = 1735270894
    with pytest.raises(ValueError, match="start time cannot be after end time"):
        assign_boolean_to_coordinates(DB_URL_TEST, hi, lo, start, end)

    #lo is bigger than hi
    hi = 74
    lo = 75
    start = 1735270873
    end = 1735270875
    with pytest.raises(ValueError, match="low can't be bigger than high"):
        assign_boolean_to_coordinates(DB_URL_TEST, hi, lo, start, end)
    

