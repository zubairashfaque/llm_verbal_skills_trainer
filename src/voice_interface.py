# voice_interface.py
import os
import tempfile
import subprocess
import logging
from pathlib import Path
import numpy as np
from typing import Optional, Union
import soundfile as sf
from pydub import AudioSegment
import noisereduce as nr

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Optional whisper model loading with fallback
try:
    import whisper

    WHISPER_AVAILABLE = True
except ImportError:
    logger.warning("Whisper not installed. Using fallback transcription.")
    WHISPER_AVAILABLE = False

# Constants
DEFAULT_WHISPER_MODEL = "base"  # Smaller model for faster loading
TEMP_DIR = Path(tempfile.gettempdir()) / "voice_interface"
os.makedirs(TEMP_DIR, exist_ok=True)
CHUNK_DURATION_MS = 5000  # Process audio in 5-second chunks to reduce latency

# Initialize model to None
_stt_model = None


def ensure_valid_audio(audio_file_path: Union[str, Path]) -> Optional[Path]:
    """
    Ensures the audio file is valid and in the correct format for processing.
    Converts to WAV format if necessary.
    """
    audio_file_path = Path(audio_file_path)
    if not audio_file_path.exists():
        logger.error(f"Audio file not found: {audio_file_path}")
        return None
    if audio_file_path.stat().st_size == 0:
        logger.error(f"Audio file is empty: {audio_file_path}")
        return None
    output_path = TEMP_DIR / f"{audio_file_path.stem}_converted.wav"
    try:
        cmd = ["ffmpeg", "-y", "-i", str(audio_file_path), "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
               str(output_path)]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            logger.error(f"FFmpeg conversion failed: {result.stderr}")
            return None
        logger.info(f"Successfully converted audio to: {output_path}")
        return output_path
    except FileNotFoundError:
        logger.error("FFmpeg is not installed or not found in PATH. Please install FFmpeg to process audio files.")
        return None
    except Exception as e:
        logger.error(f"Error during audio conversion: {str(e)}")
        return None


def preprocess_audio(audio_path: Path) -> Optional[Path]:
    """
    Pre-processes the audio file to remove noise.
    Returns the path to the cleaned audio file.
    """
    try:
        # Read the audio file
        audio_data, sample_rate = sf.read(audio_path)

        # Perform noise reduction
        reduced_noise = nr.reduce_noise(y=audio_data, sr=sample_rate, stationary=True)

        # Save the cleaned audio
        output_path = TEMP_DIR / f"{audio_path.stem}_cleaned.wav"
        sf.write(output_path, reduced_noise, sample_rate)
        logger.info(f"Successfully pre-processed audio to remove noise: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error during audio pre-processing: {str(e)}")
        return None


def split_audio_into_chunks(audio_path: Path, chunk_duration_ms: int = CHUNK_DURATION_MS) -> list:
    """
    Splits the audio file into chunks of specified duration.
    Returns a list of paths to the chunk files.
    """
    try:
        # Load the audio file using pydub
        audio = AudioSegment.from_wav(audio_path)
        duration_ms = len(audio)
        chunks = []

        for i in range(0, duration_ms, chunk_duration_ms):
            chunk = audio[i:i + chunk_duration_ms]
            chunk_path = TEMP_DIR / f"{audio_path.stem}_chunk_{i // chunk_duration_ms}.wav"
            chunk.export(chunk_path, format="wav")
            chunks.append(chunk_path)
            logger.info(f"Created audio chunk: {chunk_path}")

        return chunks
    except Exception as e:
        logger.error(f"Error splitting audio into chunks: {str(e)}")
        return []


def transcribe_audio(audio_file_path: Union[str, Path]) -> str:
    """
    Transcribes an audio file to text using Whisper or fallback method.
    Processes the audio in chunks to reduce latency.
    """
    global _stt_model
    valid_audio_path = ensure_valid_audio(audio_file_path)
    if not valid_audio_path:
        return "Error: Could not process the audio file. Please check the file format and ensure FFmpeg is installed."

    # Pre-process the audio to remove noise
    cleaned_audio_path = preprocess_audio(valid_audio_path)
    if not cleaned_audio_path:
        return "Error: Could not pre-process the audio file to remove noise."

    if WHISPER_AVAILABLE:
        try:
            if _stt_model is None:
                logger.info(f"Loading Whisper model: {DEFAULT_WHISPER_MODEL}")
                _stt_model = whisper.load_model(DEFAULT_WHISPER_MODEL)

            # Split the cleaned audio into chunks
            chunks = split_audio_into_chunks(cleaned_audio_path)
            if not chunks:
                return "Error: Could not split audio into chunks for transcription."

            # Transcribe each chunk
            transcribed_text = []
            for chunk_path in chunks:
                logger.info(f"Transcribing audio chunk: {chunk_path}")
                result = _stt_model.transcribe(str(chunk_path))
                chunk_text = result["text"].strip()
                if chunk_text:
                    transcribed_text.append(chunk_text)

            # Combine the transcribed text from all chunks
            full_text = " ".join(transcribed_text).strip()
            if not full_text:
                return "No speech detected in the audio."
            return full_text
        except Exception as e:
            logger.error(f"Whisper transcription error: {str(e)}")
            return f"Error transcribing audio: {str(e)}"
    else:
        return "Transcription service not available. Please install Whisper or configure an alternative service."


def process_voice_input(audio_data: Union[str, Path, np.ndarray]) -> dict:
    """
    High-level function to process voice input and return results.
    """
    if isinstance(audio_data, np.ndarray):
        temp_path = TEMP_DIR / f"temp_recording_{int(time.time())}.wav"
        try:
            import soundfile as sf
            sf.write(str(temp_path), audio_data, 16000)
            audio_path = temp_path
        except ImportError:
            return {"success": False,
                    "transcription": "Error: soundfile library not available for processing audio data."}
    else:
        audio_path = audio_data
    transcription = transcribe_audio(audio_path)
    return {"success": not transcription.startswith("Error:"), "transcription": transcription}


def cleanup_temp_files(max_age_hours: int = 24):
    """Removes temporary files older than the specified age"""
    current_time = time.time()
    for file_path in TEMP_DIR.glob("*"):
        file_age_hours = (current_time - file_path.stat().st_mtime) / 3600
        if file_age_hours > max_age_hours:
            try:
                os.remove(file_path)
                logger.info(f"Removed old temporary file: {file_path}")
            except Exception as e:
                logger.error(f"Failed to remove temporary file {file_path}: {str(e)}")


import time


def schedule_cleanup():
    cleanup_temp_files()
    threading.Timer(6 * 60 * 60, schedule_cleanup).start()