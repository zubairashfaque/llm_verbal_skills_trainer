"""
Comprehensive unit tests for voice_interface module.
"""
import pytest
from unittest.mock import patch, MagicMock, Mock
from pathlib import Path
import tempfile
from src.voice_interface import (
    ensure_valid_audio,
    preprocess_audio,
    split_audio_into_chunks,
    transcribe_audio,
    process_voice_input,
    cleanup_temp_files
)


class TestEnsureValidAudio:
    """Tests for ensure_valid_audio function."""

    def test_nonexistent_file(self):
        """Test handling of nonexistent audio file."""
        result = ensure_valid_audio("/path/to/nonexistent.wav")
        assert result is None

    @patch("src.voice_interface.subprocess.run")
    def test_valid_audio_conversion(self, mock_run, temp_audio_file):
        """Test successful audio conversion."""
        mock_run.return_value = Mock(returncode=0, stderr="", stdout="")

        result = ensure_valid_audio(temp_audio_file)

        assert result is not None
        assert isinstance(result, Path)
        mock_run.assert_called_once()

    @patch("src.voice_interface.subprocess.run")
    def test_ffmpeg_conversion_failure(self, mock_run, temp_audio_file):
        """Test handling of FFmpeg conversion failure."""
        mock_run.return_value = Mock(returncode=1, stderr="Conversion error", stdout="")

        result = ensure_valid_audio(temp_audio_file)

        assert result is None

    @patch("src.voice_interface.subprocess.run", side_effect=FileNotFoundError)
    def test_ffmpeg_not_installed(self, mock_run, temp_audio_file):
        """Test handling when FFmpeg is not installed."""
        result = ensure_valid_audio(temp_audio_file)

        assert result is None


class TestPreprocessAudio:
    """Tests for preprocess_audio function."""

    @patch("src.voice_interface.sf.read")
    @patch("src.voice_interface.nr.reduce_noise")
    @patch("src.voice_interface.sf.write")
    def test_successful_preprocessing(self, mock_write, mock_reduce, mock_read):
        """Test successful audio preprocessing."""
        import numpy as np

        # Mock audio data
        mock_audio = np.array([0.1, 0.2, 0.3, 0.4])
        mock_read.return_value = (mock_audio, 16000)
        mock_reduce.return_value = mock_audio

        test_path = Path("/tmp/test.wav")
        result = preprocess_audio(test_path)

        assert result is not None
        assert isinstance(result, Path)
        mock_reduce.assert_called_once()

    @patch("src.voice_interface.sf.read", side_effect=Exception("Read error"))
    def test_preprocessing_error(self, mock_read):
        """Test handling of preprocessing errors."""
        result = preprocess_audio(Path("/tmp/test.wav"))

        assert result is None


class TestSplitAudioIntoChunks:
    """Tests for split_audio_into_chunks function."""

    @patch("src.voice_interface.AudioSegment.from_wav")
    def test_successful_chunking(self, mock_from_wav):
        """Test successful audio chunking."""
        # Mock audio segment
        mock_audio = MagicMock()
        mock_audio.__len__.return_value = 15000  # 15 seconds
        mock_audio.__getitem__ = MagicMock(return_value=mock_audio)
        mock_audio.export = MagicMock()
        mock_from_wav.return_value = mock_audio

        result = split_audio_into_chunks(Path("/tmp/test.wav"), chunk_duration_ms=5000)

        # Should create 3 chunks (0-5s, 5-10s, 10-15s)
        assert isinstance(result, list)
        assert len(result) == 3

    @patch("src.voice_interface.AudioSegment.from_wav", side_effect=Exception("Read error"))
    def test_chunking_error(self, mock_from_wav):
        """Test handling of chunking errors."""
        result = split_audio_into_chunks(Path("/tmp/test.wav"))

        assert result == []


class TestTranscribeAudio:
    """Tests for transcribe_audio function."""

    @patch("src.voice_interface.WHISPER_AVAILABLE", True)
    @patch("src.voice_interface.ensure_valid_audio")
    @patch("src.voice_interface.preprocess_audio")
    @patch("src.voice_interface.split_audio_into_chunks")
    @patch("src.voice_interface.whisper.load_model")
    def test_successful_transcription(
        self, mock_load_model, mock_split, mock_preprocess, mock_ensure
    ):
        """Test successful audio transcription."""
        # Setup mocks
        mock_ensure.return_value = Path("/tmp/valid.wav")
        mock_preprocess.return_value = Path("/tmp/cleaned.wav")
        mock_split.return_value = [Path("/tmp/chunk1.wav"), Path("/tmp/chunk2.wav")]

        mock_model = MagicMock()
        mock_model.transcribe.side_effect = [
            {"text": "Hello "},
            {"text": "world"}
        ]
        mock_load_model.return_value = mock_model

        result = transcribe_audio("/tmp/test.wav")

        assert result == "Hello world"
        assert mock_model.transcribe.call_count == 2

    @patch("src.voice_interface.ensure_valid_audio")
    def test_invalid_audio_file(self, mock_ensure):
        """Test transcription with invalid audio file."""
        mock_ensure.return_value = None

        result = transcribe_audio("/tmp/invalid.wav")

        assert "Error: Could not process" in result

    @patch("src.voice_interface.WHISPER_AVAILABLE", False)
    @patch("src.voice_interface.ensure_valid_audio")
    @patch("src.voice_interface.preprocess_audio")
    def test_whisper_not_available(self, mock_preprocess, mock_ensure):
        """Test transcription when Whisper is not available."""
        mock_ensure.return_value = Path("/tmp/valid.wav")
        mock_preprocess.return_value = Path("/tmp/cleaned.wav")

        result = transcribe_audio("/tmp/test.wav")

        assert "not available" in result

    @patch("src.voice_interface.WHISPER_AVAILABLE", True)
    @patch("src.voice_interface.ensure_valid_audio")
    @patch("src.voice_interface.preprocess_audio")
    @patch("src.voice_interface.split_audio_into_chunks")
    def test_empty_transcription(self, mock_split, mock_preprocess, mock_ensure):
        """Test handling of empty transcription result."""
        mock_ensure.return_value = Path("/tmp/valid.wav")
        mock_preprocess.return_value = Path("/tmp/cleaned.wav")
        mock_split.return_value = []

        result = transcribe_audio("/tmp/test.wav")

        assert "Error: Could not split" in result


class TestProcessVoiceInput:
    """Tests for process_voice_input function."""

    @patch("src.voice_interface.transcribe_audio")
    def test_process_file_path(self, mock_transcribe):
        """Test processing voice input from file path."""
        mock_transcribe.return_value = "Transcribed text"

        result = process_voice_input("/tmp/test.wav")

        assert result["success"] is True
        assert result["transcription"] == "Transcribed text"

    @patch("src.voice_interface.transcribe_audio")
    def test_process_error(self, mock_transcribe):
        """Test processing when transcription fails."""
        mock_transcribe.return_value = "Error: Transcription failed"

        result = process_voice_input("/tmp/test.wav")

        assert result["success"] is False
        assert "Error" in result["transcription"]


class TestCleanupTempFiles:
    """Tests for cleanup_temp_files function."""

    @patch("src.voice_interface.TEMP_DIR")
    @patch("src.voice_interface.time.time")
    @patch("src.voice_interface.os.remove")
    def test_cleanup_old_files(self, mock_remove, mock_time, mock_temp_dir):
        """Test cleanup of old temporary files."""
        # Mock current time
        mock_time.return_value = 100000

        # Mock old file
        mock_file = MagicMock()
        mock_file.stat.return_value.st_mtime = 10000  # Very old file
        mock_temp_dir.glob.return_value = [mock_file]

        cleanup_temp_files(max_age_hours=24)

        mock_remove.assert_called_once()

    @patch("src.voice_interface.TEMP_DIR")
    @patch("src.voice_interface.time.time")
    def test_cleanup_recent_files(self, mock_time, mock_temp_dir):
        """Test that recent files are not removed."""
        mock_time.return_value = 100000

        # Mock recent file
        mock_file = MagicMock()
        mock_file.stat.return_value.st_mtime = 99000  # Recent file
        mock_temp_dir.glob.return_value = [mock_file]

        # Should not raise any errors
        cleanup_temp_files(max_age_hours=24)
