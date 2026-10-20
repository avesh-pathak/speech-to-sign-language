"""Tests for the dictionary-first Telugu translator (offline)."""
from telugu_s2sl.nlp.translator import TeluguNLPTranslator


def test_loads_mapping_dictionary():
    translator = TeluguNLPTranslator()
    assert len(translator.word_mapping) > 200


def test_tokenize_keeps_telugu_words():
    translator = TeluguNLPTranslator()
    tokens = translator.tokenize("నమస్కారం, ధన్యవాదాలు!")
    assert tokens == ["నమస్కారం", "ధన్యవాదాలు"]


def test_direct_word_mapping():
    translator = TeluguNLPTranslator()
    sign, is_direct = translator.word_to_sign("నమస్కారం")
    assert is_direct is True
    assert sign in {"hello", "hello_hi"}


def test_unknown_word_is_not_direct():
    translator = TeluguNLPTranslator()
    _sign, is_direct = translator.word_to_sign("అజ్ఞాతపదం")
    assert is_direct is False


def test_translate_records():
    translator = TeluguNLPTranslator()
    result = translator.translate("నమస్కారం")
    assert len(result) == 1
    assert result[0]["telugu"] == "నమస్కారం"
    assert result[0]["direct_match"] is True


def test_sign_sequence():
    translator = TeluguNLPTranslator()
    signs = translator.get_sign_sequence("అవును కాదు")
    assert signs[0] == "yes"
    assert signs[1] in {"no", "not"}


def test_text_fallback_marker():
    translator = TeluguNLPTranslator()
    translation = [{"telugu": "x", "sign": "x", "direct_match": False}]
    assert translator.signs_from_translation(translation) == ["TEXT_x"]
