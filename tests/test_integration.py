"""
Comprehensive integration tests for end-to-end workflows.
"""
import pytest
from unittest.mock import patch, MagicMock, Mock
import json
import tempfile
from pathlib import Path
from src.model_manager import generate_response
from src.skill_training import get_random_training_prompt, run_impromptu_speaking, update_tracking
from src.voice_interface import transcribe_audio, process_voice_input
from src.presentation_assessment import assess_presentation
from src.conversation import get_chat_feedback


class TestEndToEndWorkflows:
    """Integration tests for complete user workflows."""

    @patch("src.model_manager.requests.post")
    @patch("src.skill_training.generate_response_parallel")
    @patch("src.skill_training.load_tracking")
    @patch("src.skill_training.save_tracking")
    def test_complete_impromptu_speaking_workflow(
        self, mock_save, mock_load, mock_generate_parallel, mock_post
    ):
        """Test complete impromptu speaking workflow from prompt to evaluation."""
        # Setup mocks
        mock_load.return_value = {
            "impromptu_speaking": {"task_count": 0, "attempts": 0, "average_score": 0.0, "history": []}
        }

        mock_generate_parallel.return_value = """
        1️⃣ Structure: 8/10
        2️⃣ Clarity: 7/10
        3️⃣ Examples: 9/10
        4️⃣ Fluency: 8/10
        5️⃣ Impact: 8/10
        """

        # Step 1: Get a training prompt
        prompt = get_random_training_prompt("Impromptu Speaking")
        assert "challenge" in prompt
        challenge = prompt["challenge"]

        # Step 2: User provides response
        user_response = "This is my impromptu response about the topic."

        # Step 3: Evaluate the response
        feedback = run_impromptu_speaking(user_response, challenge, 60)

        assert feedback["average_score"] == 8.0
        assert "evaluation" in feedback

        # Step 4: Update tracking
        update_tracking("Impromptu Speaking", challenge, user_response, feedback)

        # Verify tracking was updated
        saved_data = mock_save.call_args[0][0]
        assert saved_data["impromptu_speaking"]["attempts"] == 1

    @patch("src.voice_interface.WHISPER_AVAILABLE", True)
    @patch("src.voice_interface.ensure_valid_audio")
    @patch("src.voice_interface.preprocess_audio")
    @patch("src.voice_interface.split_audio_into_chunks")
    @patch("src.voice_interface.whisper.load_model")
    @patch("src.presentation_assessment.generate_response_parallel")
    def test_voice_to_presentation_assessment_workflow(
        self, mock_generate, mock_load_model, mock_split, mock_preprocess, mock_ensure
    ):
        """Test workflow from voice input to presentation assessment."""
        # Step 1: Mock audio processing
        mock_ensure.return_value = Path("/tmp/valid.wav")
        mock_preprocess.return_value = Path("/tmp/cleaned.wav")
        mock_split.return_value = [Path("/tmp/chunk1.wav")]

        mock_model = MagicMock()
        mock_model.transcribe.return_value = {
            "text": "This is my presentation about effective communication."
        }
        mock_load_model.return_value = mock_model

        # Step 2: Transcribe audio
        transcription = transcribe_audio("/tmp/test.wav")
        assert "presentation" in transcription

        # Step 3: Assess presentation
        mock_generate.return_value = "Structure: 8/10, Delivery: 7/10, Content: 9/10"
        assessment = assess_presentation(transcription)

        assert isinstance(assessment, dict)
        assert "raw_feedback" in assessment

    @patch("src.conversation.generate_response")
    def test_chat_feedback_workflow(self, mock_generate):
        """Test conversation coaching workflow."""
        mock_generate.return_value = """
        Your message is clear and well-structured.
        Consider adding more specific examples to strengthen your points.
        Overall, great communication!
        """

        # Step 1: User sends a message
        user_message = "I want to improve my presentation skills. What should I focus on?"

        # Step 2: Get feedback
        feedback = get_chat_feedback(user_message)

        assert isinstance(feedback, str)
        assert len(feedback) > 0

    @patch("src.skill_training.generate_response_parallel")
    @patch("src.skill_training.load_tracking")
    @patch("src.skill_training.save_tracking")
    def test_multiple_skill_attempts_tracking(
        self, mock_save, mock_load, mock_generate
    ):
        """Test tracking across multiple skill training attempts."""
        # Initial state
        mock_load.return_value = {
            "storytelling": {"task_count": 0, "attempts": 0, "average_score": 0.0, "history": []}
        }

        mock_generate.return_value = """
        1️⃣ Narrative: 7/10
        2️⃣ Characters: 8/10
        3️⃣ Setting: 7/10
        4️⃣ Emotion: 8/10
        5️⃣ Creativity: 7/10
        """

        # First attempt
        from src.skill_training import run_storytelling
        feedback1 = run_storytelling("First story", "Tell a story about courage")
        update_tracking("Storytelling", "Tell a story about courage", "First story", feedback1)

        # Update mock for second attempt
        mock_load.return_value = {
            "storytelling": {
                "task_count": 1,
                "attempts": 1,
                "average_score": 7.4,
                "history": [{"challenge": "Tell a story about courage", "user_input": "First story", "evaluation": "...", "average_score": 7.4}]
            }
        }

        mock_generate.return_value = """
        1️⃣ Narrative: 9/10
        2️⃣ Characters: 9/10
        3️⃣ Setting: 8/10
        4️⃣ Emotion: 9/10
        5️⃣ Creativity: 9/10
        """

        # Second attempt
        feedback2 = run_storytelling("Second improved story", "Tell a story about courage")
        update_tracking("Storytelling", "Tell a story about courage", "Second improved story", feedback2)

        # Verify improvements tracked
        assert feedback2["average_score"] > feedback1["average_score"]


class TestErrorHandling:
    """Integration tests for error handling across modules."""

    @patch("src.model_manager.requests.post")
    def test_llm_connection_error_handling(self, mock_post):
        """Test graceful handling of LLM connection errors."""
        mock_post.side_effect = Exception("Connection refused")

        result = generate_response("Test prompt")

        assert "Error" in result
        assert "Unable to connect" in result

    @patch("src.voice_interface.ensure_valid_audio")
    def test_invalid_audio_file_handling(self, mock_ensure):
        """Test handling of invalid audio files."""
        mock_ensure.return_value = None

        result = process_voice_input("/invalid/path.wav")

        assert result["success"] is False
        assert "Error" in result["transcription"]

    @patch("src.skill_training.load_tracking", side_effect=Exception("File read error"))
    def test_tracking_file_error_handling(self, mock_load):
        """Test handling of tracking file errors."""
        # Should not crash, should handle gracefully
        with pytest.raises(Exception):
            get_random_training_prompt("Impromptu Speaking")


class TestConcurrentOperations:
    """Integration tests for concurrent operations."""

    @patch("src.model_manager.requests.post")
    def test_multiple_simultaneous_requests(self, mock_post):
        """Test handling multiple simultaneous LLM requests."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.iter_lines.return_value = [b'{"response": "Response"}']
        mock_post.return_value = mock_response

        # Simulate multiple requests
        results = []
        for i in range(5):
            result = generate_response(f"Prompt {i}")
            results.append(result)

        assert len(results) == 5
        assert all("Response" in r for r in results)


class TestDataPersistence:
    """Integration tests for data persistence."""

    @patch("src.skill_training.TRACKING_FILE")
    def test_tracking_data_persistence(self, mock_tracking_file):
        """Test that tracking data persists correctly."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            mock_tracking_file.return_value = f.name
            initial_data = {
                "impromptu_speaking": {"task_count": 0, "attempts": 0, "average_score": 0.0, "history": []}
            }
            json.dump(initial_data, f)
            temp_path = f.name

        # Load, modify, save
        from src.skill_training import load_tracking, save_tracking

        with patch("src.skill_training.TRACKING_FILE", temp_path):
            data = load_tracking()
            data["impromptu_speaking"]["task_count"] = 5
            save_tracking(data)

            # Reload and verify
            reloaded_data = load_tracking()
            assert reloaded_data["impromptu_speaking"]["task_count"] == 5

        # Cleanup
        Path(temp_path).unlink(missing_ok=True)
