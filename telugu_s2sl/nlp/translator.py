"""Telugu -> Indian Sign Language gloss translation.

The translator uses a three-layer strategy:

1. **Direct mapping** from the curated Telugu/ISL dictionary.
2. **English pivot** for words that have no direct entry (Telugu -> English).
3. **Fuzzy matching** against the corpus sign vocabulary (stemming and
   substring fallback).  Anything still unmatched is returned as
   ``TEXT_<word>`` so the UI can show an alphabetic/text fallback instead of
   silently dropping meaning.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ..config import COMMON_TELUGU_WORDS, PATHS, TELUGU_CONFIG

try:
    from deep_translator import GoogleTranslator
except ImportError:  # pragma: no cover - optional until requirements are installed
    GoogleTranslator = None  # type: ignore[assignment]


class TeluguNLPTranslator:
    """Rule-based, dictionary-first Telugu to ISL gloss translator."""

    _SUFFIXES = ("ing", "ed", "ly", "ness", "ment", "s", "es")

    def __init__(self) -> None:
        self.word_mapping: Dict[str, str] = dict(COMMON_TELUGU_WORDS)
        self.vowels = set(TELUGU_CONFIG["vowels"])
        self.consonants = set(TELUGU_CONFIG["consonants"])
        self.numbers_map = {num: str(i) for i, num in enumerate(TELUGU_CONFIG["numbers"])}

        self.corpus_signs_map: Dict[str, str] = {}
        self._translation_cache: Dict[str, str] = {}
        self._result_cache: Dict[str, List[Dict]] = {}

        self._load_mappings()
        self._index_corpus_signs()

        self.en_translator = None
        if GoogleTranslator is not None:
            try:
                self.en_translator = GoogleTranslator(source="te", target="en")
            except Exception:
                self.en_translator = None

    # ------------------------------------------------------------------ loading
    def _load_mappings(self) -> None:
        for path in (PATHS.telugu_to_isl, PATHS.isl_corpus_mapping):
            if not path.exists():
                continue
            try:
                with open(path, "r", encoding="utf-8") as handle:
                    mappings = json.load(handle)
                if isinstance(mappings, dict):
                    self.word_mapping.update(mappings)
                    print(f"Loaded {len(mappings):>3} mappings from {path.name}")
            except Exception as exc:
                print(f"Warning: could not load {path.name}: {exc}")

    def _index_corpus_signs(self) -> None:
        """Index generated corpus metadata for fuzzy English matching."""
        if not PATHS.isl_signs.exists():
            return
        try:
            with open(PATHS.isl_signs, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except Exception as exc:
            print(f"Warning: could not index corpus signs: {exc}")
            return

        for key, info in data.items():
            original = info.get("original_name", key)
            self.corpus_signs_map[key.lower()] = original
            self.corpus_signs_map[original.lower()] = original
            for part in re.split(r"[\s_\-]+", original):
                if len(part) > 2:
                    self.corpus_signs_map.setdefault(part.lower(), original)

        print(f"Indexed {len(self.corpus_signs_map)} corpus keywords")

    # --------------------------------------------------------------- English
    def translate_to_english(self, text: str) -> str:
        """Pivot a Telugu token to English, with a tiny in-process cache."""
        if not text or self.en_translator is None:
            return text
        if text in self._translation_cache:
            return self._translation_cache[text]
        try:
            translated = self.en_translator.translate(text) or text
        except Exception as exc:
            print(f"Translation error for '{text}': {exc}")
            translated = text
        self._translation_cache[text] = translated
        return translated

    def find_sign_match(self, english_word: str) -> Optional[str]:
        """Match an English word to a corpus sign name."""
        word = (english_word or "").lower().strip()
        if not word:
            return None

        if word in self.corpus_signs_map:
            return self.corpus_signs_map[word]

        for suffix in self._SUFFIXES:
            if not word.endswith(suffix):
                continue
            stem = word[: -len(suffix)]
            if stem in self.corpus_signs_map:
                return self.corpus_signs_map[stem]
            if suffix == "ness" and word.endswith("iness"):
                stem = word[:-4] + "y"
                if stem in self.corpus_signs_map:
                    return self.corpus_signs_map[stem]
            if suffix == "es" and word[:-2] + "e" in self.corpus_signs_map:
                return self.corpus_signs_map[word[:-2] + "e"]

        if len(word) > 4:
            for key, sign_name in self.corpus_signs_map.items():
                if len(key) > 3 and key in word:
                    return sign_name
        return None

    # -------------------------------------------------------------- tokenising
    def tokenize(self, text: str) -> List[str]:
        """Keep Telugu characters, Latin letters and digits; drop punctuation."""
        cleaned = re.sub(r"[^\u0C00-\u0C7F\sA-Za-z0-9]", " ", text or "")
        return [token for token in cleaned.split() if token]

    def transliterate_number(self, text: str) -> str:
        for telugu_num, arabic_num in self.numbers_map.items():
            text = text.replace(telugu_num, arabic_num)
        return text

    def word_to_sign(self, word: str) -> Tuple[str, bool]:
        """Return ``(sign_name, is_direct)`` for one token."""
        if word in self.word_mapping:
            return self.word_mapping[word], True
        if word.isdigit():
            return f"number_{word}", True
        if word in self.numbers_map:
            return f"number_{self.numbers_map[word]}", True
        return word, False

    def word_to_alphabets(self, word: str) -> List[str]:
        """Split a Telugu word into Unicode characters for alphabet signing."""
        return [char for char in word if "\u0C00" <= char <= "\u0C7F"]

    def transform_grammar(self, tokens: List[str]) -> List[str]:
        """Telugu and ISL both prefer SOV ordering, so order is preserved.

        A production system would move time expressions to the front and drop
        copulas; that requires a POS tagger and is intentionally out of scope
        for the dictionary-first runtime path.
        """
        return tokens

    # --------------------------------------------------------------- translate
    def translate(self, text: str) -> List[Dict]:
        """Translate Telugu text into a list of token/sign records."""
        if text in self._result_cache:
            return [dict(item) for item in self._result_cache[text]]

        normalized = self.transliterate_number(text or "")
        tokens = self.transform_grammar(self.tokenize(normalized))
        result: List[Dict] = []

        for token in tokens:
            sign_name, is_direct = self.word_to_sign(token)

            # A direct entry is used as-is unless the corpus index says the
            # sign has no frames *and* an English pivot finds a better match.
            if is_direct and not self._should_try_bridge(sign_name):
                result.append(
                    {"telugu": token, "sign": sign_name, "type": "word", "direct_match": True}
                )
                continue

            english = self.translate_to_english(token)
            match = self.find_sign_match(english)

            if match:
                result.append(
                    {
                        "telugu": token,
                        "sign": match,
                        "type": "english_bridge",
                        "english": english,
                        "direct_match": True,
                    }
                )
            elif is_direct:
                result.append(
                    {"telugu": token, "sign": sign_name, "type": "word", "direct_match": True}
                )
            else:
                display = english if english and english.lower() != token.lower() else token
                result.append(
                    {
                        "telugu": token,
                        "sign": display,
                        "type": "text_only",
                        "english": english,
                        "direct_match": False,
                    }
                )

        self._result_cache[text] = [dict(item) for item in result]
        return result

    def _should_try_bridge(self, sign_name: str) -> bool:
        if not self.corpus_signs_map:
            return False
        normalized = sign_name.lower().replace(" ", "_").replace("-", "_")
        return (
            normalized not in self.corpus_signs_map
            and sign_name.lower() not in self.corpus_signs_map
        )

    def signs_from_translation(self, translation: List[Dict]) -> List[str]:
        signs: List[str] = []
        for item in translation:
            if item.get("direct_match"):
                signs.append(str(item["sign"]))
            else:
                signs.append(f"TEXT_{item['sign']}")
        return signs

    def get_sign_sequence(self, text: str) -> List[str]:
        """Return the gloss sequence, with ``TEXT_`` markers for fallbacks."""
        return self.signs_from_translation(self.translate(text))

    # ------------------------------------------------------------------ extras
    def add_word_mapping(self, telugu_word: str, sign_name: str) -> None:
        self.word_mapping[telugu_word] = sign_name
        self._result_cache.clear()

    def save_mappings(self, filepath: Path | None = None) -> None:
        filepath = Path(filepath or PATHS.telugu_to_isl)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as handle:
            json.dump(self.word_mapping, handle, ensure_ascii=False, indent=2)


def translate_telugu(text: str) -> List[Dict]:
    """Convenience helper."""
    return TeluguNLPTranslator().translate(text)
