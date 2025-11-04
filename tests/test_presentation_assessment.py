"""
Comprehensive unit tests for presentation_assessment module.
"""
import pytest
from unittest.mock import patch, MagicMock
from src.presentation_assessment import assess_presentation


class TestAssessPresentation:
    """Tests for assess_presentation function."""

    @patch("src.presentation_assessment.generate_response_parallel")
    def test_basic_assessment(self, mock_generate):
        """Test basic presentation assessment."""
        mock_feedback = """
        📊 Overall Assessment Table
        | Criteria | Score 🎯 |
        |----------|---------|
        | Structure | 8/10 |
        | Delivery | 7/10 |
        | Content | 9/10 |
        """
        mock_generate.return_value = mock_feedback

        result = assess_presentation("This is my presentation about AI.")

        assert isinstance(result, dict)
        assert "raw_feedback" in result
        assert result["raw_feedback"] == mock_feedback
        mock_generate.assert_called_once()

    @patch("src.presentation_assessment.generate_response_parallel")
    def test_empty_presentation(self, mock_generate):
        """Test assessment of empty presentation."""
        mock_generate.return_value = "Please provide presentation content."

        result = assess_presentation("")

        assert isinstance(result, dict)
        assert "raw_feedback" in result

    @patch("src.presentation_assessment.generate_response_parallel")
    def test_short_presentation(self, mock_generate):
        """Test assessment of very short presentation."""
        mock_generate.return_value = "Presentation is too brief. Add more content."

        result = assess_presentation("Hello")

        assert isinstance(result, dict)
        assert isinstance(result["raw_feedback"], str)

    @patch("src.presentation_assessment.generate_response_parallel")
    def test_long_presentation(self, mock_generate):
        """Test assessment of long presentation."""
        long_text = "In today's world, effective communication is crucial. " * 100
        mock_generate.return_value = "Comprehensive presentation. Well structured."

        result = assess_presentation(long_text)

        assert isinstance(result, dict)
        assert "raw_feedback" in result

    @patch("src.presentation_assessment.generate_response_parallel")
    def test_presentation_with_formatting(self, mock_generate):
        """Test assessment of presentation with markdown formatting."""
        formatted_text = """
        # Introduction
        This is my presentation.

        ## Main Points
        - Point 1
        - Point 2

        ## Conclusion
        Thank you!
        """
        mock_generate.return_value = "Good use of structure!"

        result = assess_presentation(formatted_text)

        assert isinstance(result, dict)
        call_args = mock_generate.call_args[0][0]
        assert formatted_text in call_args

    @patch("src.presentation_assessment.generate_response_parallel")
    def test_prompt_includes_presentation(self, mock_generate):
        """Test that the assessment prompt includes the presentation text."""
        test_presentation = "My test presentation content"
        mock_generate.return_value = "Feedback"

        assess_presentation(test_presentation)

        call_args = mock_generate.call_args[0][0]
        assert test_presentation in call_args
        assert "presentation" in call_args.lower()

    @patch("src.presentation_assessment.generate_response_parallel")
    def test_return_structure(self, mock_generate):
        """Test the return value structure."""
        mock_generate.return_value = "Test feedback"

        result = assess_presentation("Test presentation")

        assert isinstance(result, dict)
        assert len(result.keys()) >= 1
        assert "raw_feedback" in result
        assert isinstance(result["raw_feedback"], str)
