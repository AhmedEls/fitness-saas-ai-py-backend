# processing/workout_analyzer.py

from typing import List, Dict, Any
from collections import defaultdict
import datetime
from exceptions import ProcessingError


def analyze_workout_logs(workout_logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyzes a list of workout logs for a trainee.

    Args:
        workout_logs: A list of dictionaries, where each dictionary
                      represents a single workout log entry.

    Returns:
        A dictionary containing the analysis results, including insights
        on consistency, progress, perceived exertion, and notes.
    """
    analysis_results = {
        "consistency": {},
        "completion_summary": {},
        "progress_trends": {},
        "perceived_exertion": "N/A",
        "notes_summary": [],
    }

    if not workout_logs:
        analysis_results["consistency"]["message"] = "No workout logs provided."
        return analysis_results

    # Sort logs by date for consistent analysis
    workout_logs.sort(key=lambda log: log.get("workout_date", ""))

    # --- Consistency Analysis ---
    # This is a basic check. More sophisticated analysis would involve
    # looking at expected workout frequency. Added error handling for date parsing.
    try:
        unique_dates = set(
            log.get("workout_date") for log in workout_logs if log.get("workout_date")
        )
    except Exception as e:
        raise ProcessingError(f"Error processing workout dates: {e}")
    analysis_results["consistency"]["unique_workout_dates"] = len(unique_dates)
    if unique_dates:
        dates = sorted(
            [datetime.datetime.strptime(str(d), "%Y-%m-%d") for d in unique_dates]
        )
        time_span = (dates[-1] - dates[0]).days if len(dates) > 1 else 0
        analysis_results["consistency"]["time_span_days"] = time_span
        if time_span > 0:
            analysis_results["consistency"]["workouts_per_day_average"] = (
                len(unique_dates) / time_span if time_span > 0 else len(unique_dates)
            )

    # --- Completion Status Analysis --- Added error handling for completion status.
    completion_counts = defaultdict(int)
    for log in workout_logs:
        try:
            status = log.get("completion_status", "unknown")
        except Exception as e:
            raise ProcessingError(f"Error processing completion status: {e}")
        completion_counts[status] += 1
    analysis_results["completion_summary"] = dict(completion_counts)

    # --- Progress Analysis (Per Exercise) ---
    exercise_progress = defaultdict(lambda: {"weights": [], "reps": [], "sets": []})
    for log in workout_logs:
        try:
            exercise_id = log.get("workout_exercise_id")
            if exercise_id:
                # Basic validation for list types to prevent errors

                if log.get("weight_per_set"):
                    exercise_progress[exercise_id]["weights"].extend(
                        [w for w in log["weight_per_set"] if w is not None]
                    )
                if log.get("reps_per_set"):
                    exercise_progress[exercise_id]["reps"].extend(
                        [r for r in log["reps_per_set"] if r is not None]
                    )
                if log.get("sets_completed") is not None:
                    exercise_progress[exercise_id]["sets"].append(log["sets_completed"])

        except Exception as e:
            raise ProcessingError(
                f"Error processing exercise data for log ID {log.get('id', 'N/A')}: {e}"
            )
    for exercise_id, data in exercise_progress.items():
        progress_status = "No significant change"
        if data["weights"] and max(data["weights"]) > min(data["weights"]):
            progress_status = "Weight increased"
        elif data["reps"] and max(data["reps"]) > min(data["reps"]):
            if progress_status == "No significant change":
                progress_status = "Reps increased"
            else:
                progress_status += " and Reps increased"
        elif data["sets"] and max(data["sets"]) > min(data["sets"]):
            if progress_status == "No significant change":
                progress_status = "Sets increased"
            else:
                progress_status += " and Sets increased"

        analysis_results["progress_trends"][exercise_id] = progress_status

    # --- Perceived Exertion Analysis --- Added error handling for perceived exertion.
    perceived_exertions = [
        log.get("perceived_exertion")
        for log in workout_logs
        if log.get("perceived_exertion") is not None
    ]
    if perceived_exertions:
        try:
            avg_pe = sum(perceived_exertions) / len(perceived_exertions)
        except Exception as e:
            raise ProcessingError(f"Error calculating average perceived exertion: {e}")
        analysis_results["perceived_exertion"] = (
            f"Average perceived exertion: {avg_pe:.1f}"
        )
        if avg_pe > 7:  # Example threshold
            analysis_results["perceived_exertion"] += " (Potentially high)"

    # Added error handling for notes.
    # --- Notes Analysis ---
    notes = [log.get("notes") for log in workout_logs if log.get("notes")]
    # Added error handling for notes.
    if notes:
        try:
            # In a real app, you might use NLP here to summarize or extract keywords
            # In a real app, you might use NLP here to summarize or extract keywords
            analysis_results["notes_summary"] = notes[
                :3
            ]  # Just include the first 3 notes for brevity
        except Exception as e:
            raise ProcessingError(f"Error processing workout notes: {e}")

    return analysis_results


if __name__ == "__main__":
    # Example Usage:
    sample_workout_logs = [
        {
            "completion_status": "completed",
            "created_at": "2023-10-26T10:00:00Z",
            "id": "wl1",
            "notes": "Felt good today",
            "perceived_exertion": 7,
            "reps_per_set": [10, 10, 10],
            "sets_completed": 3,
            "trainee_id": "trainee1",
            "updated_at": "2023-10-26T10:30:00Z",
            "weight_per_set": [100, 105, 110],
            "workout_date": "2023-10-26",
            "workout_exercise_id": "ex1",
        },
        {
            "completion_status": "completed",
            "created_at": "2023-10-28T10:00:00Z",
            "id": "wl2",
            "notes": None,
            "perceived_exertion": 8,
            "reps_per_set": [10, 10, 10],
            "sets_completed": 3,
            "trainee_id": "trainee1",
            "updated_at": "2023-10-28T10:30:00Z",
            "weight_per_set": [110, 115, 115],
            "workout_date": "2023-10-28",
            "workout_exercise_id": "ex1",
        },
        {
            "completion_status": "incomplete",
            "created_at": "2023-10-29T10:00:00Z",
            "id": "wl3",
            "notes": "Felt tired, stopped early",
            "perceived_exertion": 9,
            "reps_per_set": [8, 8],
            "sets_completed": 2,
            "trainee_id": "trainee1",
            "updated_at": "2023-10-29T10:20:00Z",
            "weight_per_set": [115, 115],
            "workout_date": "2023-10-29",
            "workout_exercise_id": "ex1",
        },
    ]

    analysis = analyze_workout_logs(sample_workout_logs)
    print(analysis)
