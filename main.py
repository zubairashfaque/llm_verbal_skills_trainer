# Gradio UI script
import time
import threading
import gradio as gr
import os
import json
import pandas as pd
from src.model_manager import generate_response
from src.conversation import get_chat_feedback
from src.skill_training import get_random_training_prompt, run_impromptu_speaking, run_storytelling, run_conflict_resolution, update_tracking
from src.voice_interface import process_voice_input, transcribe_audio
from src.presentation_assessment import assess_presentation

selected_topic = None
selected_time_limit = None

# Path to the task tracking JSON file
TRACKING_FILE = "config/task_tracking.json"

def start_countdown(time_limit, countdown_callback, submit_callback):
    for remaining in range(time_limit, 0, -1):
        time.sleep(1)
    submit_callback()

def generate_challenge(module: str) -> tuple:
    prompt = get_random_training_prompt(module)
    if not prompt or "challenge" not in prompt:
        return "⚠ **No challenge available. Please try again.**", ""
    challenge_text = f"🎭 **Your Challenge:** *{prompt['challenge']}*\n\n{prompt['instructions']}"
    global selected_challenge, selected_time_limit
    selected_challenge, selected_time_limit = prompt['challenge'], prompt['time_limit_seconds']
    return challenge_text, ""

# Common function for processing voice input and updating chat history
def process_voice_input_and_chat(audio_path, chat_history):
    if audio_path is None:
        chat_history.append({"role": "user", "content": "Error: No audio provided."})
        return chat_history, None
    chat_history.append({"role": "user", "content": "Transcribing..."})
    transcript = transcribe_audio(audio_path)
    if not transcript or transcript.startswith("Error"):
        chat_history[-1] = {"role": "user", "content": "Error: Could not transcribe audio."}
        return chat_history, None
    chat_history[-1] = {"role": "user", "content": transcript}
    return chat_history, transcript

# Chat with Coach (Text and Voice)
def chat_with_coach_text(user_input, history):
    if not user_input.strip():
        return history
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": "Thinking..."})
    response = get_chat_feedback(user_input)
    history[-1] = {"role": "assistant", "content": response}
    return history

def chat_with_coach_voice(audio_path, history):
    history, transcript = process_voice_input_and_chat(audio_path, history)
    if not transcript:
        return history
    history.append({"role": "assistant", "content": "Thinking..."})
    response = get_chat_feedback(transcript)
    history[-1] = {"role": "assistant", "content": response}
    return history

# Skill Training (Text and Voice)
# Skill Training (Text and Voice)
def skill_training_text(module: str, user_input: str, history) -> list:
    if selected_challenge is None or selected_time_limit is None:
        history.append(
            {"role": "user", "content": "Error: Please generate a challenge first by clicking 'Get Your Challenge'."})
        return history

    # Format the user input with the desired label and icon
    history.append({"role": "user", "content": f"👤 **You:** {user_input}"})
    history.append({"role": "assistant", "content": "‍🏫 **Coach:** Thinking..."})

    if module == "Impromptu Speaking":
        feedback = run_impromptu_speaking(user_input, selected_challenge, selected_time_limit)
        eval_text = f"‍🏫 **Coach:**\n**🔹 Topic:** {feedback['challenge']}\n\n### 📌 **LLM Evaluation**\n{feedback['evaluation']}"
    elif module == "Storytelling":
        feedback = run_storytelling(user_input, selected_challenge)
        eval_text = f"‍🏫 **Coach:**\n**📖 Story Prompt:** {feedback['challenge']}\n\n### 📌 **LLM Evaluation**\n{feedback['evaluation']}"
    elif module == "Conflict Resolution":
        feedback = run_conflict_resolution(user_input, selected_challenge)
        eval_text = f"‍🏫 **Coach:**\n**⚖️ Conflict Scenario:** {feedback['challenge']}\n\n### 📌 **LLM Evaluation**\n{feedback['evaluation']}"
    else:
        history[-1] = {"role": "assistant", "content": "‍🏫 **Coach:** Error: Invalid module selected."}
        return history

    history[-1] = {"role": "assistant", "content": eval_text}
    # Update tracking
    update_tracking(module, selected_challenge, user_input, feedback)
    return history


def skill_training_voice(module: str, audio_path, history) -> list:
    history, transcript = process_voice_input_and_chat(audio_path, history)
    if not transcript:
        return history
    if selected_challenge is None or selected_time_limit is None:
        history.append({"role": "assistant",
                        "content": "‍🏫 **Coach:** Error: Please generate a challenge first by clicking 'Get Your Challenge'."})
        return history

    # Format the user input with the desired label and icon
    history[-1] = {"role": "user", "content": f"👤 **You:** {transcript}"}
    history.append({"role": "assistant", "content": "‍🏫 **Coach:** Thinking..."})

    if module == "Impromptu Speaking":
        feedback = run_impromptu_speaking(transcript, selected_challenge, selected_time_limit)
        eval_text = f"‍🏫 **Coach:**\n**🔹 Topic:** {feedback['challenge']}\n\n### 📌 **LLM Evaluation**\n{feedback['evaluation']}"
    elif module == "Storytelling":
        feedback = run_storytelling(transcript, selected_challenge)
        eval_text = f"‍🏫 **Coach:**\n**📖 Story Prompt:** {feedback['challenge']}\n\n### 📌 **LLM Evaluation**\n{feedback['evaluation']}"
    elif module == "Conflict Resolution":
        feedback = run_conflict_resolution(transcript, selected_challenge)
        eval_text = f"‍🏫 **Coach:**\n**⚖️ Conflict Scenario:** {feedback['challenge']}\n\n### 📌 **LLM Evaluation**\n{feedback['evaluation']}"
    else:
        history[-1] = {"role": "assistant", "content": "‍🏫 **Coach:** Error: Invalid module selected."}
        return history

    history[-1] = {"role": "assistant", "content": eval_text}
    # Update tracking
    update_tracking(module, selected_challenge, transcript, feedback)
    return history
def skill_training_voice(module: str, audio_path, history) -> tuple:
    history, transcript = process_voice_input_and_chat(audio_path, history)
    if not transcript:
        return history
    if selected_challenge is None or selected_time_limit is None:
        history.append({"role": "assistant", "content": "Error: Please generate a challenge first by clicking 'Get Your Challenge'."})
        return history
    history.append({"role": "assistant", "content": "Thinking..."})
    if module == "Impromptu Speaking":
        feedback = run_impromptu_speaking(transcript, selected_challenge, selected_time_limit)
        eval_text = f"**🔹 Topic:** {feedback['challenge']}\n\n### 📌 **LLM Evaluation**\n{feedback['evaluation']}"
    elif module == "Storytelling":
        feedback = run_storytelling(transcript, selected_challenge)
        eval_text = f"**📖 Story Prompt:** {feedback['challenge']}\n\n### 📌 **LLM Evaluation**\n{feedback['evaluation']}"
    elif module == "Conflict Resolution":
        feedback = run_conflict_resolution(transcript, selected_challenge)
        eval_text = f"**⚖️ Conflict Scenario:** {feedback['challenge']}\n\n### 📌 **LLM Evaluation**\n{feedback['evaluation']}"
    else:
        history[-1] = {"role": "assistant", "content": "Error: Invalid module selected."}
        return history
    history[-1] = {"role": "assistant", "content": eval_text}
    # Update tracking
    update_tracking(module, selected_challenge, transcript, feedback)
    return history

# Presentation Assessment (Text and Voice with File Upload)
def presentation_assessment_text(text, history):
    if not text.strip():
        return history

    history.append({"role": "user", "content": f"👤 **You:** {text}"})
    history.append({"role": "assistant", "content": "‍🏫 **Coach:** Thinking..."})

    assessment = assess_presentation(text)

    # Format response in Markdown
    eval_text = f"""🏫 **Coach:**  
### 📌 **LLM Evaluation**  
{assessment["raw_feedback"]}
"""
    history[-1] = {"role": "assistant", "content": eval_text}
    return history



def presentation_assessment_voice(audio_path, history):
    history, transcript = process_voice_input_and_chat(audio_path, history)
    if not transcript:
        return history

    history[-1] = {"role": "user", "content": f"👤 **You:** {transcript}"}
    history.append({"role": "assistant", "content": "‍🏫 **Coach:** Thinking..."})

    assessment = assess_presentation(transcript)

    # Format response in Markdown
    eval_text = f"""🏫 **Coach:**  
### 📌 **LLM Evaluation**  
{assessment["raw_feedback"]}
"""
    history[-1] = {"role": "assistant", "content": eval_text}
    return history


# Tracking Functions
def load_tracking():
    try:
        with open(TRACKING_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_overall_stats():
    tracking_data = load_tracking()
    stats = []
    for module, data in tracking_data.items():
        stats.append({
            "Module": module.replace("_", " ").title(),
            "Task Count": data["task_count"],
            "Attempts": data["attempts"],
            "Average Score": round(data["average_score"], 2)
        })
    return pd.DataFrame(stats)

def get_detailed_history(module):
    tracking_data = load_tracking()
    formatted_module = module.lower().replace(" ", "_")
    history = tracking_data.get(formatted_module, {}).get("history", [])
    detailed_history = []
    for i, entry in enumerate(history, 1):
        detailed_history.append({
            "Attempt": i,
            "Challenge": entry["challenge"],
            "User Input": entry["user_input"],
            "Evaluation": entry["evaluation"],
            "Average Score": round(entry["average_score"], 2)
        })
    return pd.DataFrame(detailed_history) if detailed_history else pd.DataFrame(columns=["Attempt", "Challenge", "User Input", "Evaluation", "Average Score"])

# Gradio UI
with gr.Blocks(title="Verbal Communication Skills Trainer (LLM-Powered)") as demo:
    gr.Markdown("# 🎤 **Verbal Communication Skills Trainer (LLM-Powered)**")

    # Chat with Coach
    with gr.Tab("Chat with Coach"):
        gr.Markdown("## 💬 Chat with Your Coach")
        chat_with_coach_history_state = gr.State(value=[])
        with gr.Row():
            with gr.Column(scale=1):
                chat_input = gr.Textbox(label="💬 **Your Message**")
                chat_submit_btn = gr.Button("📩 Send Message via Text")
            with gr.Column(scale=1):
                chat_audio_input = gr.Audio(sources=["microphone", "upload"], type="filepath", label="🎤 Speak or Upload Audio")
                chat_voice_submit_btn = gr.Button("🚀 Send Message via Voice")
        chat_output = gr.Chatbot(label="🗣 **Chat with Your Coach**", type="messages")

        chat_submit_btn.click(fn=chat_with_coach_text, inputs=[chat_input, chat_with_coach_history_state], outputs=chat_output)
        chat_voice_submit_btn.click(fn=chat_with_coach_voice, inputs=[chat_audio_input, chat_with_coach_history_state], outputs=chat_output)

    # Skill Training
    with gr.Tab("Skill Training"):
        skill_training_history_state = gr.State(value=[])
        module_dropdown = gr.Dropdown(["Impromptu Speaking", "Storytelling", "Conflict Resolution"], label="🎭 **Choose a Skill Module**")
        generate_prompt_btn = gr.Button("🎲 **Get Your Challenge**")
        prompt_display = gr.Markdown()
        countdown_timer = gr.Markdown(visible=False)  # Hidden since countdown message is removed
        with gr.Row():
            with gr.Column(scale=1):
                user_response = gr.Textbox(label="✍️ **Your Response**", lines=4)
                skill_submit_btn = gr.Button("🚀 Submit Response via Text")
            with gr.Column(scale=1):
                skill_audio_input = gr.Audio(sources=["microphone", "upload"], type="filepath", label="🎤 Speak or Upload Audio")
                skill_voice_submit_btn = gr.Button("🚀 Submit Response via Voice")
        skill_chat_output = gr.Chatbot(label="🗣 **Skill Training Feedback**", type="messages")

        generate_prompt_btn.click(fn=generate_challenge, inputs=[module_dropdown], outputs=[prompt_display, countdown_timer])
        skill_submit_btn.click(fn=skill_training_text, inputs=[module_dropdown, user_response, skill_chat_output], outputs=skill_chat_output)
        skill_voice_submit_btn.click(fn=skill_training_voice, inputs=[module_dropdown, skill_audio_input, skill_chat_output], outputs=skill_chat_output)

    # Presentation Assessment (Text and Voice with File Upload)
    with gr.Tab("Presentation Assessment"):
        presentation_chat_history_state = gr.State(value=[])
        gr.Markdown("## 📜 Presentation Assessment")
        with gr.Row():
            with gr.Column(scale=1):
                presentation_text = gr.Textbox(lines=6, label="📜 **Paste Your Presentation Script**")
                presentation_submit_btn = gr.Button("🧐 Submit via Text")
            with gr.Column(scale=1):
                presentation_audio_input = gr.Audio(sources=["microphone", "upload"], type="filepath", label="🎤 Speak or Upload Audio")
                presentation_voice_submit_btn = gr.Button("🚀 Submit via Voice")
        presentation_chat_output = gr.Chatbot(label="🗣 **Presentation Feedback**", type="messages")

        presentation_submit_btn.click(fn=presentation_assessment_text, inputs=[presentation_text, presentation_chat_history_state], outputs=presentation_chat_output)
        presentation_voice_submit_btn.click(fn=presentation_assessment_voice, inputs=[presentation_audio_input, presentation_chat_history_state], outputs=presentation_chat_history_state)

    # Tracking Tab
    with gr.Tab("Tracking"):
        gr.Markdown("## 📊 Task Tracking")
        gr.Markdown("### Overall Statistics")
        overall_stats = gr.Dataframe(
            headers=["Module", "Task Count", "Attempts", "Average Score"],
            datatype=["str", "number", "number", "number"],
            value=get_overall_stats,
            interactive=False
        )

        gr.Markdown("### Detailed History by Module")
        history_module_dropdown = gr.Dropdown(
            choices=["Impromptu Speaking", "Storytelling", "Conflict Resolution"],
            label="Select Module to View History",
            value="Impromptu Speaking"
        )
        detailed_history = gr.Dataframe(
            headers=["Attempt", "Challenge", "User Input", "Evaluation", "Average Score"],
            datatype=["number", "str", "str", "str", "number"],
            value=get_detailed_history("Impromptu Speaking"),
            interactive=False
        )
        history_module_dropdown.change(fn=get_detailed_history, inputs=history_module_dropdown, outputs=detailed_history)

demo.launch()