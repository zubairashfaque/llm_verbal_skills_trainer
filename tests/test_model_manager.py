"""
Comprehensive unit tests for model_manager module.
"""
import pytest
from unittest.mock import patch, MagicMock, Mock
import json
from src.model_manager import generate_response, generate_response_parallel


class TestGenerateResponse:
    """Tests for generate_response function."""

    @patch("src.model_manager.requests.post")
    def test_successful_response(self, mock_post):
        """Test successful LLM response generation."""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.iter_lines.return_value = [
            b'{"response": "Hello "}',
            b'{"response": "World"}',
            b'{"response": "!"}',
        ]
        mock_post.return_value = mock_response

        # Call function
        result = generate_response("Test prompt")

        # Assertions
        assert result == "Hello World!"
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[1]['json']['prompt'] == "Test prompt"

    @patch("src.model_manager.requests.post")
    def test_empty_response(self, mock_post):
        """Test handling of empty LLM response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.iter_lines.return_value = [b'{"response": ""}']
        mock_post.return_value = mock_response

        result = generate_response("Test prompt")

        assert "Error: No meaningful response" in result

    @patch("src.model_manager.requests.post")
    def test_connection_error(self, mock_post):
        """Test handling of connection errors."""
        mock_post.side_effect = Exception("Connection failed")

        result = generate_response("Test prompt")

        assert "Error: Unable to connect to Ollama" in result

    @patch("src.model_manager.requests.post")
    def test_json_decode_error(self, mock_post):
        """Test handling of malformed JSON responses."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.iter_lines.return_value = [
            b'{"response": "Valid"}',
            b'Invalid JSON',
            b'{"response": " response"}',
        ]
        mock_post.return_value = mock_response

        result = generate_response("Test prompt")

        # Should still return valid parts
        assert "Valid response" in result

    @patch("src.model_manager.requests.post")
    def test_custom_max_tokens(self, mock_post):
        """Test generation with custom max_tokens parameter."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.iter_lines.return_value = [b'{"response": "Response"}']
        mock_post.return_value = mock_response

        generate_response("Test prompt", max_tokens=1024)

        call_args = mock_post.call_args
        assert call_args[1]['json']['max_tokens'] == 1024

    @patch("src.model_manager.requests.post")
    def test_streaming_response(self, mock_post):
        """Test streaming response handling."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        # Simulate streaming with multiple chunks
        mock_response.iter_lines.return_value = [
            b'{"response": "This "}',
            b'{"response": "is "}',
            b'{"response": "a "}',
            b'{"response": "streaming "}',
            b'{"response": "response"}',
        ]
        mock_post.return_value = mock_response

        result = generate_response("Test prompt")

        assert result == "This is a streaming response"


class TestGenerateResponseParallel:
    """Tests for generate_response_parallel function."""

    @patch("src.model_manager.generate_response")
    @patch("src.model_manager.multiprocessing.Pool")
    def test_parallel_execution(self, mock_pool, mock_generate):
        """Test parallel response generation."""
        # Setup mocks
        mock_result = MagicMock()
        mock_result.get.return_value = "Parallel response"
        mock_pool_instance = MagicMock()
        mock_pool_instance.apply_async.return_value = mock_result
        mock_pool.return_value.__enter__.return_value = mock_pool_instance

        # Call function
        result = generate_response_parallel("Test prompt")

        # Assertions
        assert result == "Parallel response"
        mock_pool_instance.apply_async.assert_called_once()

    @patch("src.model_manager.generate_response")
    @patch("src.model_manager.multiprocessing.Pool")
    def test_parallel_with_max_tokens(self, mock_pool, mock_generate):
        """Test parallel generation with custom max_tokens."""
        mock_result = MagicMock()
        mock_result.get.return_value = "Response"
        mock_pool_instance = MagicMock()
        mock_pool_instance.apply_async.return_value = mock_result
        mock_pool.return_value.__enter__.return_value = mock_pool_instance

        generate_response_parallel("Test prompt", max_tokens=2048)

        # Verify apply_async was called with correct arguments
        call_args = mock_pool_instance.apply_async.call_args
        assert call_args[0][1] == ("Test prompt", 2048)
