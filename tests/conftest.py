"""
Pytest configuration and fixtures for testing.
"""
import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import MagicMock


@pytest.fixture
def temp_tracking_file():
    """Create a temporary tracking file for tests."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        tracking_data = {
            "impromptu_speaking": {"task_count": 0, "attempts": 0, "average_score": 0.0, "history": []},
            "storytelling": {"task_count": 0, "attempts": 0, "average_score": 0.0, "history": []},
            "conflict_resolution": {"task_count": 0, "attempts": 0, "average_score": 0.0, "history": []}
        }
        json.dump(tracking_data, f)
        temp_path = f.name

    yield temp_path

    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def temp_audio_file():
    """Create a temporary WAV audio file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        # Write minimal WAV header
        f.write(b'RIFF')
        f.write((36).to_bytes(4, 'little'))  # File size - 8
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write((16).to_bytes(4, 'little'))  # fmt chunk size
        f.write((1).to_bytes(2, 'little'))   # Audio format (1 = PCM)
        f.write((1).to_bytes(2, 'little'))   # Number of channels
        f.write((16000).to_bytes(4, 'little'))  # Sample rate
        f.write((32000).to_bytes(4, 'little'))  # Byte rate
        f.write((2).to_bytes(2, 'little'))   # Block align
        f.write((16).to_bytes(2, 'little'))  # Bits per sample
        f.write(b'data')
        f.write((0).to_bytes(4, 'little'))   # Data chunk size
        temp_path = f.name

    yield temp_path

    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing."""
    return """
    1️⃣ Structure & Organization: 8/10
    2️⃣ Clarity & Coherence: 7/10
    3️⃣ Use of Examples & Evidence: 6/10
    4️⃣ Fluency & Natural Delivery: 8/10
    5️⃣ Overall Impact & Persuasiveness: 7/10

    Total Average Score: 7.2/10
    """


@pytest.fixture
def mock_whisper_model():
    """Create a mock Whisper model."""
    mock_model = MagicMock()
    mock_model.transcribe.return_value = {"text": "This is a test transcription"}
    return mock_model


@pytest.fixture
def sample_presentation_text():
    """Sample presentation text for testing."""
    return """
    In today's fast-paced world, effective communication is essential.
    Our AI-powered system helps improve public speaking skills through
    real-time feedback and intelligent assessments.
    """


@pytest.fixture
def sample_prompts():
    """Sample prompts for testing."""
    return {
        "impromptu_speaking": {
            "topics": ["Test topic 1", "Test topic 2"],
            "instructions": "Test instructions for {time_limit} seconds",
            "critique_prompt": "Evaluate: {challenge}\nResponse: {user_input}"
        }
    }
