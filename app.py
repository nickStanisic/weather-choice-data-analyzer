import os
from flask import jsonify, request, Flask
from config import NormalConfig, TestConfig
from helpers.get_data_from_database import pull_weather_data
from helpers.calculate_temperature import calculate_temperature
from helpers.convert_time import convert_to_unix
from helpers.assign_boolean_value import assign_boolean_to_coordinates

def create_app(config_class=NormalConfig):
   
    app = Flask(__name__)
    app.config.from_object(config_class) 

    @app.route('/analyze', methods=['POST'])
    def analyze_data():
        front_end_data = request.get_json()

        high = front_end_data.get('high')
        low = front_end_data.get('low')
        startTime = front_end_data.get('startTime')
        endTime = front_end_data.get('endTime')

        startTime = convert_to_unix(startTime)
        endTime = convert_to_unix(endTime)

        data_with_boolean = assign_boolean_to_coordinates(high, low, min_lat=41, lat_increase=2, min_lon=-109, lon_increase=2, startTime=startTime, endTime=endTime)
        return jsonify(data_with_boolean)
    return app


if __name__ == '__main__':
    config_name = os.getenv('FLASK_CONFIG', 'NormalConfig')
    if config_name == 'TestConfig':
        config = TestConfig
    else:
        config = NormalConfig

    app = create_app(config)
    app.run(host='0.0.0.0', port=5001, debug=True)

