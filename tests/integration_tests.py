import unittest
from unittest.mock import patch
from main import chat_with_coach_text, skill_training_text, presentation_assessment_text


class TestUserFlow(unittest.TestCase):
    @patch("src.main.get_chat_feedback")
    def test_chat_flow(self, mock_chat_feedback):
        """Test chat interaction with the AI coach."""
        mock_chat_feedback.return_value = "AI-generated response"
        history = chat_with_coach_text("Hello, Coach!", [])
        self.assertEqual(history[-1]["content"], "AI-generated response")

    @patch("src.skill_training.run_impromptu_speaking")
    def test_skill_training_flow(self, mock_training_feedback):
        """Test the skill training process."""
        mock_training_feedback.return_value = {"challenge": "Test challenge", "evaluation": "Great job!"}
        history = skill_training_text("Impromptu Speaking", "User response", [])
        self.assertEqual(history[-1]["content"], "‍🏫 **Coach:**\n**🔹 Topic:** Test challenge\n\n### 📌 **LLM Evaluation**\nGreat job!")

    @patch("src.presentation_assessment.assess_presentation")
    def test_presentation_assessment_flow(self, mock_presentation_feedback):
        """Test the presentation assessment process."""
        mock_presentation_feedback.return_value = {"raw_feedback": "Your speech was well-structured."}
        history = presentation_assessment_text("My presentation content", [])
        self.assertIn("Your speech was well-structured.", history[-1]["content"])


if __name__ == "__main__":
    unittest.main()
