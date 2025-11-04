"""
Comprehensive unit tests for skill_training module.
"""
import pytest
import json
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
from src.skill_training import (
    get_random_training_prompt,
    extract_scores,
    run_impromptu_speaking,
    run_storytelling,
    run_conflict_resolution,
    update_tracking,
    initialize_tracking,
    load_tracking,
    save_tracking
)


class TestExtractScores:
    """Tests for extract_scores function."""

    def test_extract_single_score(self):
        """Test extracting a single score."""
        evaluation = "Overall score: 8/10"
        scores = extract_scores(evaluation)
        assert scores == [8.0]

    def test_extract_multiple_scores(self):
        """Test extracting multiple scores."""
        evaluation = """
        1️⃣ Structure: 8/10
        2️⃣ Clarity: 7/10
        3️⃣ Examples: 9/10
        4️⃣ Fluency: 8/10
        5️⃣ Impact: 7/10
        """
        scores = extract_scores(evaluation)
        assert scores == [8.0, 7.0, 9.0, 8.0, 7.0]

    def test_extract_decimal_scores(self):
        """Test extracting decimal scores."""
        evaluation = "Score: 7.5/10 and 8.5/10"
        scores = extract_scores(evaluation)
        assert scores == [7.5, 8.5]

    def test_no_scores(self):
        """Test when no scores are present."""
        evaluation = "Great job! Keep improving."
        scores = extract_scores(evaluation)
        assert scores == []


class TestGetRandomTrainingPrompt:
    """Tests for get_random_training_prompt function."""

    @patch("src.skill_training.load_tracking")
    @patch("src.skill_training.save_tracking")
    def test_impromptu_speaking_prompt(self, mock_save, mock_load):
        """Test getting an impromptu speaking prompt."""
        mock_load.return_value = {
            "impromptu_speaking": {"task_count": 0, "attempts": 0, "average_score": 0.0, "history": []}
        }

        result = get_random_training_prompt("Impromptu Speaking")

        assert "challenge" in result
        assert "time_limit_seconds" in result
        assert "instructions" in result
        assert result["time_limit_seconds"] == 60
        mock_save.assert_called_once()

    @patch("src.skill_training.load_tracking")
    @patch("src.skill_training.save_tracking")
    def test_storytelling_prompt(self, mock_save, mock_load):
        """Test getting a storytelling prompt."""
        mock_load.return_value = {
            "storytelling": {"task_count": 0, "attempts": 0, "average_score": 0.0, "history": []}
        }

        result = get_random_training_prompt("Storytelling")

        assert "challenge" in result
        assert len(result["challenge"]) > 0
        mock_save.assert_called_once()

    @patch("src.skill_training.load_tracking")
    @patch("src.skill_training.save_tracking")
    def test_invalid_module(self, mock_save, mock_load):
        """Test handling of invalid module name."""
        mock_load.return_value = {}

        result = get_random_training_prompt("Invalid Module")

        assert "No prompts available" in result["challenge"]
        assert result["time_limit_seconds"] == 0


class TestRunImpromptuSpeaking:
    """Tests for run_impromptu_speaking function."""

    @patch("src.skill_training.generate_response_parallel")
    def test_successful_evaluation(self, mock_generate):
        """Test successful impromptu speaking evaluation."""
        mock_generate.return_value = """
        1️⃣ Structure: 8/10
        2️⃣ Clarity: 7/10
        3️⃣ Examples: 9/10
        4️⃣ Fluency: 8/10
        5️⃣ Impact: 8/10
        """

        result = run_impromptu_speaking(
            "My response text",
            "Test topic",
            60
        )

        assert result["challenge"] == "Test topic"
        assert "evaluation" in result
        assert result["average_score"] == 8.0  # (8+7+9+8+8)/5
        assert result["success"] is True

    @patch("src.skill_training.generate_response_parallel")
    def test_evaluation_with_no_scores(self, mock_generate):
        """Test evaluation when no scores are extracted."""
        mock_generate.return_value = "Great job! Keep practicing."

        result = run_impromptu_speaking(
            "My response",
            "Test topic",
            60
        )

        assert result["average_score"] == 0


class TestRunStorytelling:
    """Tests for run_storytelling function."""

    @patch("src.skill_training.generate_response_parallel")
    def test_successful_evaluation(self, mock_generate):
        """Test successful storytelling evaluation."""
        mock_generate.return_value = """
        1️⃣ Narrative: 9/10
        2️⃣ Characters: 8/10
        3️⃣ Setting: 7/10
        4️⃣ Emotion: 9/10
        5️⃣ Creativity: 8/10
        """

        result = run_storytelling(
            "Once upon a time...",
            "Tell a story about courage"
        )

        assert result["challenge"] == "Tell a story about courage"
        assert result["average_score"] == 8.2  # (9+8+7+9+8)/5


class TestRunConflictResolution:
    """Tests for run_conflict_resolution function."""

    @patch("src.skill_training.generate_response_parallel")
    def test_successful_evaluation(self, mock_generate):
        """Test successful conflict resolution evaluation."""
        mock_generate.return_value = """
        1️⃣ Empathy: 8/10
        2️⃣ Problem-solving: 9/10
        3️⃣ Communication: 7/10
        4️⃣ Persuasiveness: 8/10
        5️⃣ Resolution: 8/10
        """

        result = run_conflict_resolution(
            "I would approach this by...",
            "Teammate frustrated with deadlines"
        )

        assert result["challenge"] == "Teammate frustrated with deadlines"
        assert result["average_score"] == 8.0


class TestUpdateTracking:
    """Tests for update_tracking function."""

    @patch("src.skill_training.load_tracking")
    @patch("src.skill_training.save_tracking")
    def test_first_attempt(self, mock_save, mock_load):
        """Test tracking update for first attempt."""
        mock_load.return_value = {
            "impromptu_speaking": {
                "task_count": 1,
                "attempts": 0,
                "average_score": 0.0,
                "history": []
            }
        }

        feedback = {
            "evaluation": "Great job!",
            "average_score": 8.5
        }

        update_tracking("Impromptu Speaking", "Test topic", "My response", feedback)

        # Verify save was called
        mock_save.assert_called_once()
        saved_data = mock_save.call_args[0][0]

        assert saved_data["impromptu_speaking"]["attempts"] == 1
        assert saved_data["impromptu_speaking"]["average_score"] == 8.5
        assert len(saved_data["impromptu_speaking"]["history"]) == 1

    @patch("src.skill_training.load_tracking")
    @patch("src.skill_training.save_tracking")
    def test_multiple_attempts(self, mock_save, mock_load):
        """Test tracking update for multiple attempts."""
        mock_load.return_value = {
            "storytelling": {
                "task_count": 2,
                "attempts": 1,
                "average_score": 7.0,
                "history": [
                    {
                        "challenge": "Previous challenge",
                        "user_input": "Previous response",
                        "evaluation": "Previous eval",
                        "average_score": 7.0
                    }
                ]
            }
        }

        feedback = {
            "evaluation": "Improved!",
            "average_score": 9.0
        }

        update_tracking("Storytelling", "New challenge", "New response", feedback)

        saved_data = mock_save.call_args[0][0]

        assert saved_data["storytelling"]["attempts"] == 2
        # Average of 7.0 and 9.0 = 8.0
        assert saved_data["storytelling"]["average_score"] == 8.0
        assert len(saved_data["storytelling"]["history"]) == 2


class TestTrackingFileOperations:
    """Tests for tracking file operations."""

    @patch("src.skill_training.os.path.exists")
    @patch("src.skill_training.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    def test_initialize_tracking(self, mock_file, mock_makedirs, mock_exists):
        """Test tracking file initialization."""
        mock_exists.return_value = False

        result = initialize_tracking()

        assert "impromptu_speaking" in result
        assert "storytelling" in result
        assert "conflict_resolution" in result
        mock_makedirs.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data='{"test": "data"}')
    def test_load_tracking_success(self, mock_file):
        """Test successful tracking data loading."""
        result = load_tracking()

        assert result == {"test": "data"}

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("src.skill_training.initialize_tracking")
    def test_load_tracking_file_not_found(self, mock_init, mock_file):
        """Test loading when file doesn't exist."""
        mock_init.return_value = {"initialized": "data"}

        result = load_tracking()

        mock_init.assert_called_once()
        assert result == {"initialized": "data"}
