from collections import defaultdict
from datetime import datetime

from exceptions import ProcessingError

def analyze_diet_logs(diet_logs, target_calories=None, target_protein=None, target_carbs=None, target_fats=None):
    """
    Analyzes a trainee's diet logs to identify patterns and potential areas for suggestions.

    Args:
        diet_logs (list): A list of diet log entries for a trainee.

    Returns:
        dict: A dictionary containing insights from the diet log analysis.
              For now, this will be a basic representation.
    """
    if not isinstance(diet_logs, list):
        raise ProcessingError("Diet logs data is not in the expected list format.")

    try:
        # Sort logs by date for time-based analysis
        # Use 'created_at' for sorting as 'log_date' might be null
        diet_logs.sort(key=lambda x: datetime.strptime(x.get('created_at'), '%Y-%m-%dT%H:%M:%S.%fZ') if x.get('created_at') else datetime.min)

        analysis_results = {
            "total_calories": 0,
            "total_protein": 0,
            "total_carbs": 0,
            "total_fats": 0,
            "compliance_rate": 0,
            "meal_type_distribution": {},
            "notes_summary": [],
            "food_name_counts": {},
            "average_daily_calories": 0,
            "average_daily_protein": 0,
            "average_daily_carbs": 0,
            "average_daily_fats": 0,
    "food_name_counts": {} # Added for food item frequency
        }

    if not diet_logs:
        return analysis_results

    total_logs = len(diet_logs)
    compliant_logs = 0
    meal_type_counts = defaultdict(int)
    food_name_counts = defaultdict(int)
    daily_intake = defaultdict(lambda: defaultdict(float))

        for log in diet_logs:
            if not isinstance(log, dict):
                # Skip or log malformed individual log entries
                continue

        # Basic aggregation of macros and calories
            analysis_results["total_calories"] += log.get("calories", 0) or 0
            analysis_results["total_protein"] += log.get("protein", 0) or 0
        analysis_results["total_carbs"] += log.get("carbs", 0) or 0
        analysis_results["total_fats"] += log.get("fats", 0) or 0
        
        # Aggregate daily intake for averages
        log_date_str = log.get("log_date")
        if log_date_str:
            # Assuming log_date is in 'YYYY-MM-DD' format or similar
            # You might need to adjust the date parsing based on your actual schema
            try:
                log_date = datetime.strptime(log_date_str, '%Y-%m-%d').date()
                daily_intake[log_date]["calories"] += log.get("calories", 0) or 0
                daily_intake[log_date]["protein"] += log.get("protein", 0) or 0
                daily_intake[log_date]["carbs"] += log.get("carbs", 0) or 0
                daily_intake[log_date]["fats"] += log.get("fats", 0) or 0
            except ValueError:
                # Handle potential date parsing errors
                pass

        # Compliance check
        if log.get("compliance") is True:
                compliant_logs += 1
        # If compliance is False, note it
        elif log.get("compliance") is False:
                analysis_results["notes_summary"].append(f"Non-compliant entry on {log.get('log_date')}: {log.get('notes', 'No specific notes.')}")

        # Meal type counting
            meal_type = log.get("meal_type")
        if meal_type:
            meal_type_counts[meal_type] += 1

        # Food name counting
            food_name = log.get("food_name")
        if food_name: food_name_counts[food_name] += 1
            
        # Notes summary
        if log.get("notes"):
            analysis_results["notes_summary"].append(log["notes"])

    # Calculate compliance rate
    if total_logs > 0:
        analysis_results["compliance_rate"] = (compliant_logs / total_logs) * 100

    # Store common meal types
    analysis_results["meal_type_distribution"] = dict(meal_type_counts)

    # Calculate average daily intake
    num_logged_days = len(daily_intake)
    if num_logged_days > 0:
        analysis_results["average_daily_calories"] = sum(day["calories"] for day in daily_intake.values()) / num_logged_days
        analysis_results["average_daily_protein"] = sum(day["protein"] for day in daily_intake.values()) / num_logged_days
        analysis_results["average_daily_carbs"] = sum(day["carbs"] for day in daily_intake.values()) / num_logged_days
        analysis_results["average_daily_fats"] = sum(day["fats"] for day in daily_intake.values()) / num_logged_days

    # Add comparison to targets if provided
    if target_calories is not None:
        analysis_results["calories_vs_target"] = analysis_results["average_daily_calories"] - target_calories
    if target_protein is not None:
        analysis_results["protein_vs_target"] = analysis_results["average_daily_protein"] - target_protein
    if target_carbs is not None:
        analysis_results["carbs_vs_target"] = analysis_results["average_daily_carbs"] - target_carbs
        if target_fats is not None:
        analysis_results["fats_vs_target"] = analysis_results["average_daily_fats"] - target_fats

        # Store food name counts
        analysis_results["food_name_counts"] = food_name_counts

        return analysis_results

    except Exception as e:
        raise ProcessingError(f"Error analyzing diet logs: {e}") from e

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    sample_diet_logs = [
        {
            "calories": 500, "carbs": 50, "compliance": True, "created_at": "...",
            "diet_item_id": "...", "fats": 15, "food_name": "Chicken Salad", "id": "...",
            "log_date": "2023-10-26", "meal_type": "Lunch", "notes": "", "protein": 30,
            "quantity": "...", "trainee_id": "...", "updated_at": "..."
        },
        {
            "calories": 800, "carbs": 80, "compliance": False, "created_at": "...",
            "diet_item_id": "...", "fats": 30, "food_name": "Pasta with Meatballs", "id": "...",
            "log_date": "2023-10-26", "meal_type": "Dinner", "notes": "Ate out with friends.", "protein": 40,
            "quantity": "...", "trainee_id": "...", "updated_at": "..."
        },
        {
            "calories": 200, "carbs": 20, "compliance": True, "created_at": "...",
            "diet_item_id": "...", "fats": 5, "food_name": "Greek Yogurt", "id": "...",
            "log_date": "2023-10-27", "meal_type": "Breakfast", "notes": "", "protein": 20,
            "quantity": "...", "trainee_id": "...", "updated_at": "..."
        }
    ]

    diet_analysis = analyze_diet_logs(sample_diet_logs)
    print("Diet Analysis Results:")
    print(diet_analysis)