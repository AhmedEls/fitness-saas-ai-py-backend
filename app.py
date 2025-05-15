from flask import Flask, request, jsonify
import logging

# Import processing and suggestion modules
from processing.data_processor import process_trainee_data
from suggestions.suggestion_generator import generate_suggestions
from exceptions import AppException, ProcessingError, SuggestionGenerationError

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# TODO: Replace with a securely stored secret key in production
API_KEY = "your_super_secret_api_key" 

@app.route('/process_logs', methods=['POST'])
def process_logs():
    """
    Endpoint to receive and process workout and diet logs.
    """
    # API Key authentication
    provided_api_key = request.headers.get('X-API-Key')
 if not provided_api_key or provided_api_key != API_KEY:
 return jsonify({"error": "Unauthorized: Invalid or missing API key"}), 401

    # Validate incoming JSON data
 try:
 data = request.get_json()
 if data is None:
 return jsonify({"error": "Invalid JSON data"}), 400

 # Ensure the top level data is a dictionary
 if not isinstance(data, dict):
 return jsonify({"error": "Invalid data structure: Top level should be a dictionary with trainee_ids as keys"}), 400

 suggestions_by_trainee = {}

 for trainee_id, trainee_data in data.items():
 # Validate trainee data structure
 if not isinstance(trainee_data, dict):
 suggestions_by_trainee[trainee_id] = {"error": "Invalid data structure for trainee"}
 continue

 if 'workout_logs' not in trainee_data or 'diet_logs' not in trainee_data:
 suggestions_by_trainee[trainee_id] = {"error": "Missing 'workout_logs' or 'diet_logs'"}
 continue

 workout_logs = trainee_data['workout_logs']
 diet_logs = trainee_data['diet_logs']

 # Validate workout_logs structure (assuming a list of dictionaries)
 if not isinstance(workout_logs, list) or not all(isinstance(log, dict) for log in workout_logs):
 suggestions_by_trainee[trainee_id] = {"error": "Invalid data structure for 'workout_logs'"}
 continue

 # Validate diet_logs structure (assuming a list of dictionaries)
 if not isinstance(diet_logs, list) or not all(isinstance(log, dict) for log in diet_logs):
 suggestions_by_trainee[trainee_id] = {"error": "Invalid data structure for 'diet_logs'"}
 continue

 # Basic validation of required fields within logs (can be expanded)
 # For brevity, not validating every single field here, but highly recommended
 # to add more specific checks based on your schemas.
 if any('created_at' not in log or 'trainee_id' not in log for log in workout_logs):
 suggestions_by_trainee[trainee_id] = {"error": "Missing required field in workout logs"}
 continue
 if any('created_at' not in log or 'trainee_id' not in log for log in diet_logs):
 suggestions_by_trainee[trainee_id] = {"error": "Missing required field in diet logs"}
 continue

 # Process the trainee's data and generate suggestions
 # Processing and suggestion generation might raise custom exceptions
 analyzed_data = process_trainee_data(trainee_data)
 suggestions = generate_suggestions(analyzed_data)
 suggestions_by_trainee[trainee_id] = suggestions

 return jsonify({"suggestions": suggestions_by_trainee}), 200
 except Exception as e:
 logging.error(f"An unexpected error occurred: {e}", exc_info=True)
 return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # You can run this Flask app for testing purposes.
    # In a production environment, you would typically use a more robust server.
    app.run(debug=True, port=5000)

@app.errorhandler(AppException)
def handle_app_exception(error):
 """
 Centralized error handler for custom application exceptions.
 """
 logging.error(f"Application exception: {error}", exc_info=True)
 response = jsonify({"error": str(error)})
 # Set appropriate status code based on exception type if needed,
 # otherwise default to a generic server error
 response.status_code = 500
 return response