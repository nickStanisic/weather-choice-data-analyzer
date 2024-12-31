import os
from dotenv import load_dotenv
from flask import jsonify, request, Flask
from config import NormalConfig, TestConfig
from helpers.convert_time import convert_to_unix
from helpers.assign_boolean_value import assign_boolean_to_coordinates

load_dotenv()

DBURL = os.getenv("DB_URL")

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
        print(endTime, startTime)
        startTime = convert_to_unix(startTime)
        endTime = convert_to_unix(endTime)

        data_with_boolean = assign_boolean_to_coordinates(DBURL, high, low, startTime, endTime)
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

