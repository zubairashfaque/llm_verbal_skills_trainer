"""
Comprehensive unit tests for conversation module.
"""
import pytest
from unittest.mock import patch, MagicMock
from src.conversation import get_chat_feedback


class TestGetChatFeedback:
    """Tests for get_chat_feedback function."""

    @patch("src.conversation.generate_response")
    def test_basic_feedback(self, mock_generate):
        """Test basic chat feedback generation."""
        mock_generate.return_value = "Great message! Try to be more specific."

        result = get_chat_feedback("Hello, how can I improve my communication?")

        assert result == "Great message! Try to be more specific."
        mock_generate.assert_called_once()

    @patch("src.conversation.generate_response")
    def test_empty_input(self, mock_generate):
        """Test feedback with empty input."""
        mock_generate.return_value = "Please provide a message to analyze."

        result = get_chat_feedback("")

        assert "Please provide" in result or result != ""

    @patch("src.conversation.generate_response")
    def test_long_input(self, mock_generate):
        """Test feedback with long input."""
        long_message = "This is a very long message. " * 50
        mock_generate.return_value = "Your message is comprehensive. Consider being more concise."

        result = get_chat_feedback(long_message)

        assert isinstance(result, str)
        assert len(result) > 0

    @patch("src.conversation.generate_response")
    def test_prompt_construction(self, mock_generate, capsys):
        """Test that the prompt is constructed correctly."""
        mock_generate.return_value = "Feedback"

        get_chat_feedback("Test message")

        # Check that generate_response was called with a prompt containing the user message
        call_args = mock_generate.call_args[0][0]
        assert "Test message" in call_args
        assert "conversation coach" in call_args.lower()

    @patch("src.conversation.generate_response")
    def test_special_characters(self, mock_generate):
        """Test feedback with special characters in input."""
        mock_generate.return_value = "Feedback for special chars"

        result = get_chat_feedback("Hello! How are you? 😊 #communication")

        assert isinstance(result, str)
        mock_generate.assert_called_once()

    @patch("src.conversation.generate_response")
    def test_multiline_input(self, mock_generate):
        """Test feedback with multiline input."""
        multiline_message = """Hello,
        This is a multiline message.
        How can I improve?"""
        mock_generate.return_value = "Good structure! Consider formatting."

        result = get_chat_feedback(multiline_message)

        assert isinstance(result, str)
        assert len(result) > 0
