# suggestions/suggestion_generator.py

from exceptions import SuggestionGenerationError
from typing import List, Dict, Any

def generate_suggestions(analyzed_data: Dict[str, Any]) -> List[str]:
    """
    Generates a list of 2-4 brief suggestions for a trainee based on analyzed data.

    Args:
        analyzed_data: A dictionary containing the analyzed workout and diet data
                       for a trainee.

    Returns:
        A list of strings, where each string is a brief suggestion.
    """
    suggestions = []

    workout_analysis = analyzed_data.get('workout_analysis', {})
    diet_analysis = analyzed_data.get('diet_analysis', {})

    # --- Generate Workout Suggestions ---
    workout_consistency = workout_analysis.get('consistency', 'unknown')
    workout_progress = workout_analysis.get('progress', 'unknown')
    perceived_exertion = workout_analysis.get('perceived_exertion', 'unknown')
    workout_notes = workout_analysis.get('notes', '').lower()

    if workout_consistency == 'low':
        suggestions.append("Workout Tip: Increasing workout frequency could help you reach your goals faster.")
    elif workout_progress == 'stalled':
        suggestions.append("Workout Adjustment: Consider slightly increasing intensity (weight, reps, or sets) on key exercises.")
    if perceived_exertion == 'high':
        suggestions.append("Warning Flag: High perceived exertion consistently could indicate overtraining. Prioritize rest and recovery.")
    if 'tired' in workout_notes or 'fatigue' in workout_notes:
        suggestions.append("Workout Tip: Pay extra attention to recovery and sleep this week.")

    # --- Generate Nutrition Suggestions ---
    diet_compliance = diet_analysis.get('compliance', 'unknown')
    calorie_intake = diet_analysis.get('calories', 'unknown')
    protein_intake = diet_analysis.get('protein', 'unknown')
    diet_notes = diet_analysis.get('notes', '').lower()

    if diet_compliance == 'low':
        suggestions.append("Nutrition Tip: Review your meal plan to identify barriers to consistency and find practical solutions.")
    if calorie_intake == 'low':
        suggestions.append("Nutrition Adjustment: Ensure your calorie intake supports your activity level and goals.")
    if protein_intake == 'low':
        suggestions.append("Nutrition Tip: Focus on incorporating more protein sources into your meals.")
    if 'hungry' in diet_notes:
        suggestions.append("Nutrition Tip: Consider adjusting meal timing or composition to manage hunger.")

    # --- Generate Motivational Messages ---
    # Add a motivational message if overall progress is good
    if workout_progress == 'good' and diet_compliance == 'high':
        suggestions.append("Suggestion: Great work this week! Keep up the consistent effort.")
    # Add a general motivational message if suggestions are less than 4 and no major flags
    if len(suggestions) < 4 and not any(flag in s for s in suggestions for flag in ["Warning Flag"]):
         suggestions.append("Motivation: Remember your goals and why you started! Stay disciplined.")

    # --- Generate Warning Flags ---
    if 'pain' in workout_notes:
        suggestions.append("Warning Flag: Trainee noted pain during workouts. Advise checking form or consulting a professional.")

    # --- Ensure 2-4 Suggestions ---
    # If less than 2 suggestions, add some general ones
    while len(suggestions) < 2:
        if len(suggestions) == 0:
            suggestions.append("General Tip: Review your workout intensity this week.")
        elif len(suggestions) == 1:
            suggestions.append("General Tip: Pay attention to your hydration and sleep.")

    # Trim to a maximum of 4 suggestions
    return suggestions[:4]

if __name__ == '__main__':
    suggestions = generate_suggestions(dummy_analyzed_data)
    print("Generated Suggestions:")
    for suggestion in suggestions:
        print(f"- {suggestion}")

    dummy_analyzed_data_with_issues = {
        'workout_analysis': {
            'consistency': 'low',
            'progress': 'poor',
            'perceived_exertion': 'high',
            'notes': 'Feeling tired, some knee pain'
        },
        'diet_analysis': {
            'calories': 'low',
            'carbs': 'adequate',
            'fats': 'adequate',
            'protein': 'low',
            'compliance': 'low',
            'notes': 'Hard to stick to the plan, always hungry'
        }
    }

    suggestions_with_issues = generate_suggestions(dummy_analyzed_data_with_issues)
    print("\nGenerated Suggestions (with issues):")
    for suggestion in suggestions_with_issues:
        print(f"- {suggestion}")
# suggestions/suggestion_generator.py

from typing import List, Dict, Any

def generate_suggestions(analyzed_data: Dict[str, Any]) -> List[str]:
    """
    Generates a list of 2-4 brief suggestions for a trainee based on analyzed data.

    Args:
        analyzed_data: A dictionary containing the analyzed workout and diet data
                       for a trainee.

    Returns:
        A list of strings, where each string is a brief suggestion.
    """
    suggestions = []

    try:
        workout_analysis = analyzed_data.get('workout_analysis', {})
        diet_analysis = analyzed_data.get('diet_analysis', {})

        # --- Generate Workout Suggestions ---
        workout_consistency = workout_analysis.get('consistency', 'unknown')
        workout_progress = workout_analysis.get('progress', 'unknown')
        perceived_exertion = workout_analysis.get('perceived_exertion', 'unknown')
        workout_notes = workout_analysis.get('notes', '').lower()

        if workout_consistency == 'low':
            suggestions.append("Workout Tip: Increasing workout frequency could help you reach your goals faster.")
        elif workout_progress == 'stalled':
            suggestions.append("Workout Adjustment: Consider slightly increasing intensity (weight, reps, or sets) on key exercises.")
        if perceived_exertion == 'high':
            suggestions.append("Warning Flag: High perceived exertion consistently could indicate overtraining. Prioritize rest and recovery.")
        if 'tired' in workout_notes or 'fatigue' in workout_notes:
            suggestions.append("Workout Tip: Pay extra attention to recovery and sleep this week.")

        # --- Generate Nutrition Suggestions ---
        diet_compliance = diet_analysis.get('compliance', 'unknown')
        calorie_intake = diet_analysis.get('calories', 'unknown')
        protein_intake = diet_analysis.get('protein', 'unknown')
        diet_notes = diet_analysis.get('notes', '').lower()

        if diet_compliance == 'low':
            suggestions.append("Nutrition Tip: Review your meal plan to identify barriers to consistency and find practical solutions.")
        if calorie_intake == 'low':
            suggestions.append("Nutrition Adjustment: Ensure your calorie intake supports your activity level and goals.")
        if protein_intake == 'low':
            suggestions.append("Nutrition Tip: Focus on incorporating more protein sources into your meals.")
        if 'hungry' in diet_notes:
            suggestions.append("Nutrition Tip: Consider adjusting meal timing or composition to manage hunger.")

        # Ensure we have between 2 and 4 suggestions (basic example)
        while len(suggestions) < 2 and (workout_analysis or diet_analysis):
            # Add more general suggestions if needed to meet the minimum
            if len(suggestions) == 0:
                suggestions.append("General Tip: Review your workout intensity this week.")
            elif len(suggestions) == 1:
                suggestions.append("General Tip: Pay attention to your hydration and sleep.")

        # Add a motivational message if suggestions are less than 4 and no major flags
        if len(suggestions) < 4 and not any(flag in s for s in suggestions for flag in ["Warning Flag"]):
             suggestions.append("Motivation: Remember your goals and why you started! Stay disciplined.")

        # --- Generate Warning Flags ---
        if 'pain' in workout_notes:
            suggestions.append("Warning Flag: Trainee noted pain during workouts. Advise checking form or consulting a professional.")

        # Trim to a maximum of 4 suggestions
        return suggestions[:4]

    except Exception as e:
        # Catch any unexpected errors during suggestion generation
        raise SuggestionGenerationError(f"Error generating suggestions: {e}") from e

if __name__ == '__main__':
    # Example usage with dummy analyzed data
    from exceptions import SuggestionGenerationError # Import for local testing
    dummy_analyzed_data_good = {
        'workout_analysis': {
            'consistency': 'high',
            'progress': 'good',
            'perceived_exertion': 'moderate',
            'notes': ''
        },
        'diet_analysis': {
            'calories': 'adequate',
            'carbs': 'adequate',
            'fats': 'adequate',
            'protein': 'adequate',
            'compliance': 'high',
            'notes': ''
        }
    }

    suggestions = generate_suggestions(dummy_analyzed_data_good)# Example usage with dummy analyzed data
    for suggestion in suggestions:
        print(f"- {suggestion}")

    dummy_analyzed_data_with_issues = {
        'workout_analysis': {
            'consistency': 'low',
            'progress': 'stalled',
            'perceived_exertion': 'high',
            'notes': 'Feeling tired, some knee pain'
        },
        'diet_analysis': {
            'calories': 'low',
            'carbs': 'low',
            'fats': 'adequate',
            'protein': 'adequate',
            'compliance': 'low',
            'notes': 'Hard to stick to the plan'
        }
    }

    suggestions_with_issues = generate_suggestions(dummy_analyzed_data_with_issues)    print("Generated Suggestions (Good Progress):")
    print("\nGenerated Suggestions (with issues):")
    for suggestion in suggestions_with_issues:
        print(f"- {suggestion}")