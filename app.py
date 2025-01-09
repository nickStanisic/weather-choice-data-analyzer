import os
from dotenv import load_dotenv
from flask import jsonify, request, Flask
from helpers.convert_time import convert_to_unix
from helpers.assign_boolean_value import assign_boolean_to_coordinates

load_dotenv()

DBURL = os.getenv("DB_URL")

def create_app():
    """Creates an instance of a flask app. 
    This is an app for receiving post requests from outside sources. 
    Specifically, it is made for the weather-choice frontend app. 

    Returns:
        app: Instance of a Flask app
    """   
    app = Flask(__name__)

    @app.route('/analyze', methods=['POST'])
    def analyze_data():
        """It takes post data including high, low, startTime and endTime. It then performs 
        calcuations with helper methods lead by assign_boolean_to_coordinates which assesses 
        wether a lat, lon location to see if it's temperature is inside or outside the specified 
        high/low boundaries. It then returns this information. 

        Returns:
            string: list of dict objects with labels {"date", "average_temp", "lat", "lon", "valid"}
            that is jsonified
        """      
        try: 
            #get data from request  
            front_end_data = request.get_json()

            #check if data is received
            if not front_end_data:
                return jsonify({"error": "No input data provided."}), 400

            #get prevelant information
            high = front_end_data.get('high')
            low = front_end_data.get('low')
            start_time = front_end_data.get('startTime')
            end_time = front_end_data.get('endTime')

            #convert times to unix timestamp
            start_time = convert_to_unix(start_time)
            end_time = convert_to_unix(end_time)
            
            #calculate if temperatures are within or outside range for each lat/lon pair
            data_with_boolean = assign_boolean_to_coordinates(DBURL, high, low, start_time, end_time)
            return jsonify(data_with_boolean), 200
        
        except ValueError as ve:
            # catch incorrect data formatting
            app.logger.error(f"ValueError in /analyze endpoint: {ve}")
            return jsonify({"error": "Invalid input data format."}), 400
        except Exception as e:
            # Handles other errors
            app.logger.error(f"Unexpected error in /analyze endpoint: {e}")
            return jsonify({"error": "An unexpected error occurred."}), 500
        
    return app


if __name__ == '__main__':
    """
    Entry point of flask app. 
    """
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)

