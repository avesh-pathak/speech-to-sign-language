"""Utility tests."""
from telugu_s2sl.utils import extract_telugu_words, format_duration, is_telugu_text


def test_is_telugu_text():
    assert is_telugu_text("నమస్కారం") is True
    assert is_telugu_text("Hello") is False
    assert is_telugu_text("Hello నమస్కారం") is True


def test_extract_telugu_words():
    words = extract_telugu_words("Hello నమస్కారం World ధన్యవాదాలు")
    assert "నమస్కారం" in words
    assert "ధన్యవాదాలు" in words
    assert "Hello" not in words


def test_format_duration():
    assert format_duration(2.5) == "2.5s"
    assert format_duration(90) == "1m 30s"
