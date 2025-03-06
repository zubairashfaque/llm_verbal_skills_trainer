import unittest
from unittest.mock import patch, MagicMock
from src.model_manager import generate_response
from src.skill_training import get_random_training_prompt
from src.voice_interface import transcribe_audio
from src.presentation_assessment import assess_presentation

class TestModelManager(unittest.TestCase):
    @patch("src.model_manager.requests.post")
    def test_generate_response(self, mock_post):
        """Test response generation from the model manager."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.iter_lines.return_value = [b'{"response": "Test output"}']

        response = generate_response("Test prompt")
        self.assertEqual(response, "Test output")


class TestSkillTraining(unittest.TestCase):
    def test_get_random_training_prompt(self):
        """Test if the prompt retrieval is working correctly."""
        prompt = get_random_training_prompt("impromptu_speaking")
        self.assertIsInstance(prompt, dict)
        self.assertIn("challenge", prompt)
        self.assertIn("instructions", prompt)
        self.assertTrue(len(prompt["challenge"]) > 0)  # Ensure prompt is not empty

class TestVoiceProcessing(unittest.TestCase):
    @patch("src.voice_interface.whisper.load_model")  # ✅ Mock Whisper model
    def test_transcribe_audio(self, mock_whisper_load):
        """Test if audio transcription is working with Whisper."""
        # Create a mock model
        mock_model = MagicMock()
        mock_model.transcribe.side_effect = [
            {"text": "Test transcription"},  # Mock response for first chunk
            {"text": "Test transcription"},  # Mock response for second chunk
            {"text": "Test transcription"},  # Mock response for third chunk
        ]  # Simulate multiple chunks being processed

        # Assign mock model to load_model call
        mock_whisper_load.return_value = mock_model

        # Call the function
        response = transcribe_audio("test_audio.wav")

        # ✅ Print the transcribed audio output for debugging
        print("\n🔊 **Transcribed Audio Output:**", response)

        # ✅ Check if the full response matches the expected concatenation
        expected_output = "Test transcription Test transcription Test transcription"
        self.assertEqual(response.strip(), expected_output)  # Ensure proper concatenation

class TestPresentationAssessment(unittest.TestCase):
    def test_assess_presentation(self):
        """Test if presentation assessment returns feedback."""
        response = assess_presentation("This is a test presentation.")
        self.assertIsInstance(response, dict)
        self.assertIn("raw_feedback", response)
        self.assertIsInstance(response["raw_feedback"], str)
        self.assertTrue(len(response["raw_feedback"]) > 0)  # Ensure non-empty feedback



if __name__ == "__main__":
    unittest.main()
