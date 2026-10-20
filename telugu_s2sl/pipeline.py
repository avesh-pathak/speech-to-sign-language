"""End-to-end speech/text -> ISL pipeline.

This is the single orchestration layer used by the GUI, the CLI and tests::

    pipeline = SpeechToSignPipeline()
    bundle = pipeline.translate_text("నమస్కారం")
    bundle.signs       # ['hello_hi']
    bundle.animation   # playback records with PIL frames
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional

from .animation.corpus import ISLCorpusAnimator
from .audio.asr import TeluguASR
from .nlp.translator import TeluguNLPTranslator


@dataclass
class TranslationBundle:
    """Everything the UI needs for one utterance."""

    source_text: str
    tokens: List[Dict] = field(default_factory=list)
    signs: List[str] = field(default_factory=list)
    animation: List[Dict] = field(default_factory=list)

    @property
    def available_steps(self) -> int:
        return sum(1 for step in self.animation if step.get("available"))

    @property
    def missing_steps(self) -> int:
        return len(self.animation) - self.available_steps

    @property
    def has_frames(self) -> bool:
        return self.available_steps > 0


class SpeechToSignPipeline:
    """Compose ASR, the Telugu translator and the ISL animator."""

    def __init__(
        self,
        translator: TeluguNLPTranslator | None = None,
        animator: ISLCorpusAnimator | None = None,
        asr: TeluguASR | None = None,
    ) -> None:
        self.translator = translator or TeluguNLPTranslator()
        self.animator = animator or ISLCorpusAnimator()
        self.asr = asr or TeluguASR()

    # ------------------------------------------------------------------ text
    def translate_text(self, text: str) -> TranslationBundle:
        tokens = self.translator.translate(text)
        signs = self.translator.signs_from_translation(tokens)
        animation = self.animator.create_animation_sequence(signs)
        return TranslationBundle(
            source_text=text,
            tokens=tokens,
            signs=signs,
            animation=animation,
        )

    # ----------------------------------------------------------------- audio
    def transcribe_file(self, audio_path: str | Path) -> str:
        return self.asr.recognize_from_file(audio_path)

    def translate_audio_file(self, audio_path: str | Path) -> TranslationBundle:
        return self.translate_text(self.transcribe_file(audio_path))

    def listen(
        self,
        on_status: Optional[Callable[[str], None]] = None,
        on_listen_complete: Optional[Callable[[], None]] = None,
    ) -> TranslationBundle:
        text = self.asr.recognize_from_microphone(
            on_listen_complete=on_listen_complete,
            on_status=on_status,
        )
        return self.translate_text(text)

    # ------------------------------------------------------------------ info
    def describe(self) -> Dict:
        corpus = self.animator.get_stats()
        return {
            "mappings": len(self.translator.word_mapping),
            "corpus_signs": corpus["total_signs"],
            "corpus_frames": corpus["total_images"],
            "asr_backend": "google" if self.asr.available else "unavailable",
        }
