import pytest
import json
import os

def test_analyze_data(mock_db_url, app, client, populate_test_data, db_connection):
    """
    Test the /analyze endpoint with valid input data.
    """

    input_data = {
        "high": 100,
        "low": 0,
        "startTime": "2024-12-20T11:35",
        "endTime": "2024-12-30T11:35"
    }

    # Send a POST request to the /analyze endpoint
    response = client.post('/analyze', json=input_data)

    assert response.status_code == 200

    # Check the response JSON contains the expected data
    response_json = json.loads(response.data)
    assert isinstance(response_json, list)
    assert len(response_json) > 0  # Should be multiple responses

def test_analyze_data_no_input(client):
    """
    Test the /analyze endpoint when no input data is provided.
    """
    response = client.post('/analyze', json={})
    assert response.status_code == 400
    response_json = json.loads(response.data)
    assert response_json["error"] == "No input data provided."