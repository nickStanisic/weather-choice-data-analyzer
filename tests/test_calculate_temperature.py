import pytest
from helpers.calculate_temperature import calculate_temperature

def test_is_temp_good_within_range():
    """Test is_temp_good function with temperatures within the specified range."""
    # Arrange
    db_data = [
        {'id': 1, 'lat': 39.0, 'lon': -105.5, 'temp': 20.0, 'reading_time': '2024-01-11T12:00:00'},
        {'id': 2, 'lat': 40.0, 'lon': -106.0, 'temp': 25.0, 'reading_time': '2024-01-12T12:00:00'},
    ]
    low = 15.0
    high = 30.0

    # Act
    result = calculate_temperature(high, low, db_data)

    # Assert
    assert result[0]['valid'] is True
    assert result[1]['valid'] is True
