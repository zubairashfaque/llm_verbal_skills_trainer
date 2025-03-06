# skill_training.py
import re
import random
import json
import os
from config.settings import PROMPTS
from src.model_manager import generate_response, generate_response_parallel

# Path to the task tracking JSON file
TRACKING_FILE = "config/task_tracking.json"

# Initialize the tracking file if it doesn't exist
def initialize_tracking():
    default_tracking = {
        "impromptu_speaking": {"task_count": 0, "attempts": 0, "average_score": 0.0, "history": []},
        "storytelling": {"task_count": 0, "attempts": 0, "average_score": 0.0, "history": []},
        "conflict_resolution": {"task_count": 0, "attempts": 0, "average_score": 0.0, "history": []}
    }
    if not os.path.exists(TRACKING_FILE):
        os.makedirs(os.path.dirname(TRACKING_FILE), exist_ok=True)
        with open(TRACKING_FILE, 'w') as f:
            json.dump(default_tracking, f, indent=4)
    return default_tracking

# Load tracking data
def load_tracking():
    try:
        with open(TRACKING_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return initialize_tracking()

# Save tracking data
def save_tracking(tracking_data):
    with open(TRACKING_FILE, 'w') as f:
        json.dump(tracking_data, f, indent=4)

def extract_scores(evaluation: str) -> list:
    """
    Extracts numerical scores from the evaluation text.

    Args:
        evaluation (str): The LLM-generated evaluation string.

    Returns:
        list: A list of float scores extracted from patterns like 'score/10'.
    """
    score_pattern = r"(\d+(?:\.\d+)?)/10"  # Matches integers or decimals followed by '/10'
    matches = re.findall(score_pattern, evaluation)
    return [float(match) for match in matches]

def run_impromptu_speaking(user_input: str, challenge: str, time_limit: int) -> dict:
    """
    Evaluates the user's impromptu speaking response and calculates the average score.
    """
    critique_prompt = PROMPTS["impromptu_speaking"]["critique_prompt"].format(
        challenge=challenge, user_input=user_input
    )
    evaluation = generate_response_parallel(critique_prompt)
    scores = extract_scores(evaluation)
    average_score = sum(scores) / 5 if len(scores) == 5 else 0
    return {
        "challenge": challenge,
        "evaluation": evaluation,
        "average_score": average_score,
        "success": True
    }

def run_storytelling(user_input: str, challenge: str) -> dict:
    """
    Evaluates the user's story and calculates the average score.
    """
    critique_prompt = PROMPTS["storytelling"]["critique_prompt"].format(
        challenge=challenge, user_input=user_input
    )
    evaluation = generate_response_parallel(critique_prompt)
    scores = extract_scores(evaluation)
    average_score = sum(scores) / 5 if len(scores) == 5 else 0
    return {
        "challenge": challenge,
        "evaluation": evaluation,
        "average_score": average_score
    }

def run_conflict_resolution(user_input: str, challenge: str) -> dict:
    """
    Evaluates the user's conflict resolution response and calculates the average score.
    """
    critique_prompt = PROMPTS["conflict_resolution"]["critique_prompt"].format(
        challenge=challenge, user_input=user_input
    )
    evaluation = generate_response_parallel(critique_prompt)
    scores = extract_scores(evaluation)
    average_score = sum(scores) / 5 if len(scores) == 5 else 0
    return {
        "challenge": challenge,
        "evaluation": evaluation,
        "average_score": average_score
    }

def get_random_training_prompt(module: str) -> dict:
    """
    Generates a random challenge for the specified module and updates task count.
    """
    formatted_module = module.lower().replace(" ", "_")
    tracking_data = load_tracking()

    if formatted_module not in PROMPTS or not PROMPTS[formatted_module]["topics"]:
        return {
            "challenge": "⚠ No prompts available for this module.",
            "time_limit_seconds": 0,
            "instructions": "No challenge available."
        }

    challenge = random.choice(PROMPTS[formatted_module]["topics"])
    time_limit = 60  # Default time limit in seconds
    instructions = PROMPTS[formatted_module]["instructions"].format(time_limit=time_limit)

    # Update task count
    tracking_data[formatted_module]["task_count"] += 1
    save_tracking(tracking_data)

    return {
        "challenge": challenge,
        "time_limit_seconds": time_limit,
        "instructions": instructions
    }

def update_tracking(module: str, challenge: str, user_input: str, feedback: dict):
    """
    Updates the tracking data after a challenge attempt.
    """
    formatted_module = module.lower().replace(" ", "_")
    tracking_data = load_tracking()

    # Update attempts
    tracking_data[formatted_module]["attempts"] += 1

    # Update average score
    average_score = feedback.get("average_score", 0.0)
    current_attempts = tracking_data[formatted_module]["attempts"]
    current_avg = tracking_data[formatted_module]["average_score"]
    tracking_data[formatted_module]["average_score"] = (
        (current_avg * (current_attempts - 1) + average_score) / current_attempts
    )

    # Update history
    tracking_data[formatted_module]["history"].append({
        "challenge": challenge,
        "user_input": user_input,
        "evaluation": feedback["evaluation"],
        "average_score": average_score
    })

    save_tracking(tracking_data)