import os
from dotenv import load_dotenv
from flask import jsonify, request, Flask
from helpers.convert_time import convert_to_unix
from helpers.assign_boolean_value import assign_boolean_to_coordinates

load_dotenv()

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
        calculations with helper methods lead by assign_boolean_to_coordinates which assesses 
        whether a lat, lon location to see if it's temperature is inside or outside the specified 
        high/low boundaries. It then returns this information. 

        Returns:
            string: list of dict objects with labels {"date", "average_temp", "lat", "lon", "valid"}
            that is jsonified
        """      
        try: 
            # Get data from request  
            front_end_data = request.get_json()

            # Check if data is received
            if not front_end_data:
                return jsonify({"error": "No input data provided."}), 400

            # Get prevalent information
            high = front_end_data.get('high')
            low = front_end_data.get('low')
            start_time = front_end_data.get('startTime')
            end_time = front_end_data.get('endTime')

            # Convert times to unix timestamp
            start_time = convert_to_unix(start_time)
            end_time = convert_to_unix(end_time)

            # Calculate if temperatures are within or outside range for each lat/lon pair
            # No longer need to pass DBURL
            data_with_boolean = assign_boolean_to_coordinates(high, low, start_time, end_time)
            return jsonify(data_with_boolean), 200
        
        except ValueError as ve:
            # Catch incorrect data formatting
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
    # Use PORT environment variable for Cloud Run, default to 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)