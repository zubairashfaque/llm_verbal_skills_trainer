"""
Custom exception classes for the LLM Verbal Skills Trainer.
"""


class VerbalsSkillsTrainerError(Exception):
    """Base exception for all application-specific errors."""
    pass


class ModelError(VerbalsSkillsTrainerError):
    """Errors related to LLM model operations."""
    pass


class OllamaConnectionError(ModelError):
    """Failed to connect to Ollama server."""
    pass


class ModelResponseError(ModelError):
    """Invalid or empty response from model."""
    pass


class AudioProcessingError(VerbalsSkillsTrainerError):
    """Errors related to audio processing."""
    pass


class AudioFileNotFoundError(AudioProcessingError):
    """Audio file not found or inaccessible."""
    pass


class AudioConversionError(AudioProcessingError):
    """Failed to convert audio file."""
    pass


class TranscriptionError(AudioProcessingError):
    """Failed to transcribe audio."""
    pass


class WhisperNotAvailableError(AudioProcessingError):
    """Whisper model not available or not installed."""
    pass


class TrackingError(VerbalsSkillsTrainerError):
    """Errors related to tracking data."""
    pass


class TrackingFileError(TrackingError):
    """Failed to read or write tracking file."""
    pass


class InvalidModuleError(VerbalsSkillsTrainerError):
    """Invalid training module specified."""
    pass


class ConfigurationError(VerbalsSkillsTrainerError):
    """Configuration is invalid or missing."""
    pass


class ValidationError(VerbalsSkillsTrainerError):
    """Input validation failed."""
    pass


# Error messages
ERROR_MESSAGES = {
    "ollama_connection": "Unable to connect to Ollama server. Please ensure Ollama is running.",
    "audio_file_not_found": "Audio file not found: {path}",
    "audio_conversion_failed": "Failed to convert audio file. Ensure FFmpeg is installed.",
    "transcription_failed": "Audio transcription failed: {error}",
    "whisper_not_available": "Whisper is not installed. Please install it with: pip install openai-whisper",
    "tracking_file_error": "Failed to access tracking file: {error}",
    "invalid_module": "Invalid module: {module}. Valid modules are: impromptu_speaking, storytelling, conflict_resolution",
    "empty_response": "Model returned an empty response. Please try again.",
    "validation_failed": "Input validation failed: {errors}",
}


def get_error_message(key: str, **kwargs) -> str:
    """
    Get formatted error message.

    Args:
        key: Error message key
        **kwargs: Formatting parameters

    Returns:
        Formatted error message
    """
    message = ERROR_MESSAGES.get(key, "An unexpected error occurred")
    return message.format(**kwargs) if kwargs else message
