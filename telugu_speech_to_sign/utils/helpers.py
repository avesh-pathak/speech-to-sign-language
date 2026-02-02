"""
Utility functions for Telugu Speech-to-Sign Language System
"""
import os
import json
import wave
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Union
from datetime import datetime


def ensure_dir(path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, create if not
    
    Args:
        path: Directory path
        
    Returns:
        Path object
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: dict, filepath: Union[str, Path], indent: int = 2):
    """
    Save dictionary to JSON file
    
    Args:
        data: Dictionary to save
        filepath: Output file path
        indent: JSON indentation
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


def load_json(filepath: Union[str, Path]) -> dict:
    """
    Load JSON file to dictionary
    
    Args:
        filepath: JSON file path
        
    Returns:
        Dictionary
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_audio_wav(
    audio: np.ndarray,
    filepath: Union[str, Path],
    sample_rate: int = 16000
):
    """
    Save numpy array as WAV file
    
    Args:
        audio: Audio signal as numpy array
        filepath: Output file path
        sample_rate: Sample rate
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    # Normalize and convert to int16
    audio = audio / np.max(np.abs(audio)) if np.max(np.abs(audio)) > 0 else audio
    audio_int16 = (audio * 32767).astype(np.int16)
    
    with wave.open(str(filepath), 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_int16.tobytes())


def get_timestamp() -> str:
    """Get current timestamp string"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def log_message(message: str, level: str = "INFO"):
    """
    Print formatted log message
    
    Args:
        message: Log message
        level: Log level (INFO, WARNING, ERROR)
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    symbols = {
        "INFO": "ℹ️",
        "WARNING": "⚠️",
        "ERROR": "❌",
        "SUCCESS": "✅"
    }
    symbol = symbols.get(level, "•")
    print(f"[{timestamp}] {symbol} {message}")


def is_telugu_text(text: str) -> bool:
    """
    Check if text contains Telugu characters
    
    Args:
        text: Text to check
        
    Returns:
        True if Telugu characters present
    """
    for char in text:
        # Telugu Unicode range: 0C00-0C7F
        if '\u0C00' <= char <= '\u0C7F':
            return True
    return False


def extract_telugu_words(text: str) -> List[str]:
    """
    Extract Telugu words from mixed text
    
    Args:
        text: Input text
        
    Returns:
        List of Telugu words
    """
    import re
    
    # Match Telugu word sequences
    pattern = r'[\u0C00-\u0C7F]+'
    matches = re.findall(pattern, text)
    
    return matches


def calculate_accuracy(predictions: np.ndarray, labels: np.ndarray) -> float:
    """
    Calculate classification accuracy
    
    Args:
        predictions: Predicted class indices
        labels: True class indices
        
    Returns:
        Accuracy as float
    """
    return np.mean(predictions == labels)


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "2m 30s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}m {secs}s"
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        return f"{hours}h {mins}m"


class ProgressTracker:
    """Simple progress tracker for long operations"""
    
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = datetime.now()
    
    def update(self, count: int = 1):
        """Update progress"""
        self.current += count
        self._print_progress()
    
    def _print_progress(self):
        """Print progress bar"""
        percent = self.current / self.total * 100
        bar_length = 30
        filled = int(bar_length * self.current / self.total)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        if self.current > 0:
            remaining = elapsed / self.current * (self.total - self.current)
            eta = format_duration(remaining)
        else:
            eta = "?"
        
        print(f"\r{self.description}: [{bar}] {percent:.1f}% | ETA: {eta}", end="")
        
        if self.current >= self.total:
            print()  # New line at completion
    
    def complete(self):
        """Mark as complete"""
        self.current = self.total
        self._print_progress()
        elapsed = format_duration((datetime.now() - self.start_time).total_seconds())
        log_message(f"{self.description} completed in {elapsed}", "SUCCESS")
