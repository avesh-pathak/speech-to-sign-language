"""
Configuration settings for Telugu Speech-to-Sign Language Translation System
"""
import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).parent.parent.absolute()
DATASETS_DIR = BASE_DIR / "datasets"
MODELS_DIR = BASE_DIR / "models"
TRAINED_DIR = MODELS_DIR / "trained"

# Audio Configuration
AUDIO_CONFIG = {
    "sample_rate": 16000,
    "n_mfcc": 40,
    "n_fft": 2048,
    "hop_length": 512,
    "max_audio_length": 10,  # seconds
    "frame_length": 25,  # milliseconds
    "frame_step": 10,  # milliseconds
}

# Model Configuration
MODEL_CONFIG = {
    "lstm_units": 128,
    "attention_heads": 4,
    "dropout_rate": 0.3,
    "learning_rate": 0.001,
    "batch_size": 32,
    "epochs": 50,
    "embedding_dim": 256,
    "num_classes": 100,  # Number of sign classes
}

# Dataset Paths
DATASET_PATHS = {
    "audio": DATASETS_DIR / "audio",
    "gifs_alphabets": DATASETS_DIR / "gifs" / "alphabets",
    "gifs_numbers": DATASETS_DIR / "gifs" / "numbers",
    "gifs_words": DATASETS_DIR / "gifs" / "words",
    "mappings": DATASETS_DIR / "mappings",
    "telugu_words": DATASETS_DIR / "mappings" / "telugu_words.json",
    "isl_mapping": DATASETS_DIR / "mappings" / "telugu_to_isl.json",
    "isl_corpus_mapping": DATASETS_DIR / "mappings" / "telugu_to_isl_corpus.json",
    "isl_real_frames": DATASETS_DIR / "ISL_Corpus" / "Frames_Word_Level",
    "isl_corpus_frames": DATASETS_DIR / "ISL_Corpus" / "Frames_Word_Level",
}

# Telugu Language Settings
TELUGU_CONFIG = {
    "language_code": "te-IN",
    "alphabet_count": 52,
    "vowels": ["అ", "ఆ", "ఇ", "ఈ", "ఉ", "ఊ", "ఋ", "ౠ", "ఎ", "ఏ", "ఐ", "ఒ", "ఓ", "ఔ", "అం", "అః"],
    "consonants": [
        "క", "ఖ", "గ", "ఘ", "ఙ",
        "చ", "ఛ", "జ", "ఝ", "ఞ",
        "ట", "ఠ", "డ", "ఢ", "ణ",
        "త", "థ", "ద", "ధ", "న",
        "ప", "ఫ", "బ", "భ", "మ",
        "య", "ర", "ల", "వ", "శ",
        "ష", "స", "హ", "ళ", "క్ష", "ఱ"
    ],
    "numbers": ["౦", "౧", "౨", "౩", "౪", "౫", "౬", "౭", "౮", "౯"],
}

# Common Telugu Words for ISL Mapping
COMMON_TELUGU_WORDS = {
    "నమస్కారం": "hello",
    "ధన్యవాదాలు": "thank_you",
    "దయచేసి": "please",
    "అవును": "yes",
    "కాదు": "no",
    "మంచిది": "good",
    "చెడ్డది": "bad",
    "నేను": "i",
    "నీవు": "you",
    "అతడు": "he",
    "ఆమె": "she",
    "మేము": "we",
    "వారు": "they",
    "ఇది": "this",
    "అది": "that",
    "ఎక్కడ": "where",
    "ఎప్పుడు": "when",
    "ఎందుకు": "why",
    "ఎలా": "how",
    "ఏమి": "what",
    "నీరు": "water",
    "ఆహారం": "food",
    "ఇల్లు": "house",
    "కుటుంబం": "family",
    "స్నేహితుడు": "friend",
    "పాఠశాల": "school",
    "పని": "work",
    "సహాయం": "help",
    "వెళ్ళు": "go",
    "రా": "come",
    "తిను": "eat",
    "తాగు": "drink",
    "చూడు": "see",
    "విను": "hear",
    "మాట్లాడు": "speak",
    "నేర్చుకో": "learn",
    "ప్రేమ": "love",
    "సంతోషం": "happy",
    "బాధ": "sad",
    "కోపం": "angry",
    "భయం": "fear",
    "అమ్మ": "mother",
    "నాన్న": "father",
    "అన్న": "brother",
    "అక్క": "sister",
    "తాత": "grandfather",
    "నానమ్మ": "grandmother",
    "డబ్బు": "money",
    "సమయం": "time",
    "రోజు": "day",
}

# GUI Configuration
GUI_CONFIG = {
    "window_title": "Telugu Speech-to-Sign Translator",
    "window_size": "1200x800",
    "theme": "dark",
    "gif_display_size": (400, 400),
    "font_family": "Segoe UI",  # Changed to standard Windows font
    "font_size": 14,
}

# ASR Configuration
ASR_CONFIG = {
    "language": "te-IN",
    "timeout": 5,
    "phrase_time_limit": 10,
    "energy_threshold": 300,
}

# Ensure directories exist
def ensure_directories():
    """Create all required directories if they don't exist"""
    for path in DATASET_PATHS.values():
        if isinstance(path, Path) and not path.suffix:
            path.mkdir(parents=True, exist_ok=True)
    TRAINED_DIR.mkdir(parents=True, exist_ok=True)

# Initialize directories on import
ensure_directories()
