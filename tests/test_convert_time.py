import pytest
from helpers.convert_time import convert_to_unix


def test_convert_to_unix():
    """
    Check if a time stamp is converted correctly to unix time.
    """    
    time = "2024-12-30T11:35"
    new_time = convert_to_unix(time)
    assert(new_time == 1735583700)

def test_convert_to_unix_invalid_value():
    """    
    This method will check to see if an error is thrown for a incorrect format for time parameter.
    """    
    with pytest.raises(ValueError) as exc_info:
        convert_to_unix("2024-123-30T11:35")
    
    with pytest.raises(ValueError) as exc_info:
        convert_to_unix("2024-12-30T11:")

    with pytest.raises(ValueError) as exc_info:
        convert_to_unix("2024-12-30T11:100")

    with pytest.raises(ValueError) as exc_info:
        convert_to_unix("2024-12-38T11:35")

    with pytest.raises(ValueError) as exc_info:
        convert_to_unix("202-12-30T11:35")

