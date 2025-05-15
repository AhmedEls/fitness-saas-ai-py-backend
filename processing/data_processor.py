# processing/data_processor.py

from .workout_analyzer import analyze_workout_logs
from exceptions import ProcessingError # Assuming exceptions.py is at the project root
from .diet_analyzer import analyze_diet_logs

def process_trainee_data(trainee_data):
    """
    Processes workout and diet logs for a trainee and returns the combined analysis.

    Args:
        trainee_data (dict): A dictionary containing a trainee's data,
                             expected to have 'workout_logs' and 'diet_logs' keys.

    Returns:
        dict: A dictionary containing the analysis results from workout and diet logs.
    """
    if not isinstance(trainee_data, dict):
        raise ProcessingError("Invalid trainee data format. Expected a dictionary.")

    workout_logs = trainee_data.get('workout_logs')
    diet_logs = trainee_data.get('diet_logs')

    if not isinstance(workout_logs, list):
        raise ProcessingError("Invalid workout logs format. Expected a list.")
    if not isinstance(diet_logs, list):
        raise ProcessingError("Invalid diet logs format. Expected a list.")

    try:
        workout_analysis = analyze_workout_logs(workout_logs)
        diet_analysis = analyze_diet_logs(diet_logs)
    except Exception as e:
        raise ProcessingError(f"Error during analysis: {e}") from e

 # Combine the analysis results. The structure of this combined result
 # can be refined based on what the suggestion generator needs.
 combined_analysis = {
 'workout_analysis': workout_analysis,
 'diet_analysis': diet_analysis
    }

    return combined_analysis

if __name__ == '__main__':
 # Example usage (for testing purposes)
 sample_trainee_data = {
 'workout_logs': [
 # Sample workout log data based on your schema
 {'completion_status': 'completed', 'created_at': '...', 'id': '...', 'notes': 'Feeling strong', 'perceived_exertion': 7, 'reps_per_set': [10, 10, 10], 'sets_completed': 3, 'trainee_id': 'trainee1', 'updated_at': '...', 'weight_per_set': [100, 105, 105], 'workout_date': '2023-10-26', 'workout_exercise_id': '...'},
 # Add more sample workout logs
 ],
 'diet_logs': [
 # Sample diet log data based on your schema
 {'calories': 2000, 'carbs': 250, 'compliance': True, 'created_at': '...', 'diet_item_id': '...', 'fats': 70, 'food_name': 'Chicken Breast', 'id': '...', 'log_date': '2023-10-26', 'meal_type': 'Lunch', 'notes': '...', 'protein': 150, 'quantity': '150g', 'trainee_id': 'trainee1', 'updated_at': '...'},
 # Add more sample diet logs
 ]
    }

    analyzed_data = process_trainee_data(sample_trainee_data)
    print(analyzed_data)