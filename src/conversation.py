from src.model_manager import generate_response

def get_chat_feedback(user_input: str) -> str:
    """
    Provides real-time conversation coaching feedback based on user input.
    """
    prompt = (
        "You are a conversation coach. Respond to the user's message with feedback "
        "on clarity, tone, and suggestions for improvement.\n\n"
        f"User Message:\n{user_input}\n\n"
        "Coach Response:"
    )

    print(f"DEBUG: Prompt being sent to Ollama:\n{prompt}")  # ✅ Debugging print statement
    response = generate_response(prompt)

    print(f"DEBUG: Generated Response from Ollama:\n{response}")  # ✅ Debugging print statement

    return response

