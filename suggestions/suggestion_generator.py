# suggestions/suggestion_generator.py
from exceptions import SuggestionGenerationError
from typing import List, Dict, Any

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


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

    api_key = os.getenv("GOOGLE_API_KEY")
    model = None  # Initialize model to None
    if not api_key:
        print(
            "Warning: GOOGLE_API_KEY environment variable not set. Skipping AI suggestion generation."
        )
    else:
        try:
            # Initialize the Gemini model
            model = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                google_api_key=api_key,
            )
        except Exception as e:
            print(f"Error initializing AI model: {e}")
            model = None  # Ensure model is None if initialization fails

    try:
        workout_analysis = analyzed_data.get("workout_analysis", {})
        diet_analysis = analyzed_data.get("diet_analysis", {})

        # --- Generate Workout Suggestions ---
        workout_consistency = workout_analysis.get("consistency", "unknown")
        workout_progress = workout_analysis.get("progress", "unknown")
        perceived_exertion = workout_analysis.get("perceived_exertion", "unknown")
        workout_notes = workout_analysis.get("notes", "").lower()

        if workout_consistency == "low":
            suggestions.append(
                "Workout Tip: Increasing workout frequency could help you reach your goals faster."
            )
        elif workout_progress == "stalled":
            suggestions.append(
                "Workout Adjustment: Consider slightly increasing intensity (weight, reps, or sets) on key exercises."
            )
        if perceived_exertion == "high":
            suggestions.append(
                "Warning Flag: High perceived exertion consistently could indicate overtraining. Prioritize rest and recovery."
            )
        if "tired" in workout_notes or "fatigue" in workout_notes:
            suggestions.append(
                "Workout Tip: Pay extra attention to recovery and sleep this week."
            )

        # --- Generate Nutrition Suggestions ---
        diet_compliance = diet_analysis.get("compliance", "unknown")
        calorie_intake = diet_analysis.get("calories", "unknown")
        protein_intake = diet_analysis.get("protein", "unknown")
        diet_notes = diet_analysis.get("notes", "").lower()

        if diet_compliance == "low":
            suggestions.append(
                "Nutrition Tip: Review your meal plan to identify barriers to consistency and find practical solutions."
            )
        if calorie_intake == "low":
            suggestions.append(
                "Nutrition Adjustment: Ensure your calorie intake supports your activity level and goals."
            )
        if protein_intake == "low":
            suggestions.append(
                "Nutrition Tip: Focus on incorporating more protein sources into your meals."
            )
        if "hungry" in diet_notes:
            suggestions.append(
                "Nutrition Tip: Consider adjusting meal timing or composition to manage hunger."
            )

        ai_suggestions = []
        if model:  # Check if the model was successfully initialized
            try:
                # Construct the prompt using analyzed_data
                prompt_text = f"""Analyze the following fitness and nutrition data for a trainee:
                {analyzed_data}

                Based on this analysis, provide 2 to 4 concise and actionable suggestions for the trainee to improve their fitness and nutrition. Format the suggestions as a numbered list or bullet points.
                """

                # Invoke the model
                ai_response = model.invoke([HumanMessage(content=prompt_text)])
                ai_generated_text = ai_response.content

                # Parse AI response (basic parsing assuming numbered or bulleted list)
                ai_suggestions = [
                    s.strip()
                    for s in ai_generated_text.split("\n")
                    if s.strip()
                    and (s.strip()[0].isdigit() or s.strip().startswith("-"))
                ]

            except Exception as ai_e:
                print(f"Error calling AI model: {ai_e}")
                # ai_suggestions remains empty, and we'll rely on existing/generic suggestions

        # --- Combine and Refine Suggestions ---
        # Combine existing and AI suggestions, removing duplicates
        # Preserve order as much as possible, prioritizing warnings and existing.
        combined_suggestions = []
        seen_suggestions = set()

        # Add existing suggestions first, maintaining order and uniqueness
        for s in suggestions:
            if s not in seen_suggestions:
                combined_suggestions.append(s)
                seen_suggestions.add(s)

        # Add AI suggestions, ensuring uniqueness and not adding duplicates of existing
        for s in ai_suggestions:
            if s not in seen_suggestions:
                combined_suggestions.append(s)
                seen_suggestions.add(s)

        # Ensure minimum 2 suggestions, add generic if needed
        while len(combined_suggestions) < 2:
            if len(combined_suggestions) == 0:
                combined_suggestions.append(
                    "General Tip: Review your workout intensity this week."
                )
            elif len(combined_suggestions) == 1:
                combined_suggestions.append(
                    "General Tip: Pay attention to your hydration and sleep."
                )

        # Trim to a maximum of 4 suggestions
        suggestions = combined_suggestions[:4]

        return suggestions

    except Exception as e:
        # Catch any unexpected errors during suggestion generation
        raise SuggestionGenerationError(f"Error generating suggestions: {e}") from e


if __name__ == "__main__":
    # Example usage with dummy analyzed data
    from exceptions import SuggestionGenerationError  # Import for local testing

    dummy_analyzed_data_good = {
        "workout_analysis": {
            "consistency": "high",
            "progress": "good",
            "perceived_exertion": "moderate",
            "notes": "",
        },
        "diet_analysis": {
            "calories": "adequate",
            "carbs": "adequate",
            "fats": "adequate",
            "protein": "adequate",
            "compliance": "high",
            "notes": "",
        },
    }

    suggestions = generate_suggestions(
        dummy_analyzed_data_good
    )  # Example usage with dummy analyzed data
    for suggestion in suggestions:
        print(f"- {suggestion}")

    dummy_analyzed_data_with_issues = {
        "workout_analysis": {
            "consistency": "low",
            "progress": "stalled",
            "perceived_exertion": "high",
            "notes": "Feeling tired, some knee pain",
        },
        "diet_analysis": {
            "calories": "low",
            "carbs": "low",
            "fats": "adequate",
            "protein": "adequate",
            "compliance": "low",
            "notes": "Hard to stick to the plan",
        },
    }

    suggestions_with_issues = generate_suggestions(dummy_analyzed_data_with_issues)
    print("Generated Suggestions (Good Progress):")
    print("\nGenerated Suggestions (with issues):")
    for suggestion in suggestions_with_issues:
        print(f"- {suggestion}")
