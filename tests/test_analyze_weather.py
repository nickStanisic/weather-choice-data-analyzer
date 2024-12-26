from datetime import datetime

def test_analyze_weather_success(client):
    """Test the /analyze-weather route with valid data and existing records."""
    # Arrange: Insert sample data directly into the database
    conn = client.application.config['DATABASE_CONNECTION']  # Assuming you have this setup
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO weather_readings (lat, lon, temp, reading_time)
        VALUES (%s, %s, %s, %s);
    """
    sample_data = [
        (39.0, -105.5, 20.0, datetime(2024, 1, 11, 12, 0)),
        (40.0, -106.0, 25.0, datetime(2024, 1, 12, 12, 0)),
    ]
    cursor.executemany(insert_query, sample_data)
    conn.commit()

    # Define POST data
    post_data = {
        'low': 15.0,
        'high': 30.0,
        'start_datetime': '2024-01-10T12:00',
        'end_datetime': '2024-01-14T12:00'
    }

    # Act: Send POST request
    response = client.post('/analyze-weather', json=post_data)

    # Assert: Check response status and data
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['count'] == 2
    assert len(json_data['records']) == 2
    assert json_data['records'][0]['lat'] == 39.0
    assert json_data['records'][1]['lat'] == 40.0
    assert json_data['records'][0]['valid'] is True
    assert json_data['records'][1]['valid'] is True

    # Clean up
    cursor.close()
    conn.close()