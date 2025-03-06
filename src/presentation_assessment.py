from src.model_manager import generate_response, generate_response_parallel
from config.settings import PROMPTS

def assess_presentation(presentation_text: str) -> dict:
    """
    Analyzes the given presentation text, returning structured feedback.
    Scores Structure, Delivery, and Content (1-10) with detailed critique.
    """
    prompt = PROMPTS["presentation_assessment"] + f"\n\n📜 **User's Presentation:**\n{presentation_text}"
    raw_feedback = generate_response_parallel(prompt)

    result = {
        "raw_feedback": raw_feedback
    }
    return result
