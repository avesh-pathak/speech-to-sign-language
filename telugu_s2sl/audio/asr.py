"""Telugu automatic speech recognition.

The runtime path uses Google's speech endpoint through ``SpeechRecognition``
because it gives usable Telugu transcripts without a local acoustic model.
The Res-BiLSTM-AM model in ``telugu_s2sl.model`` is the trainable alternative
described in the paper and can be used as a word-level acoustic classifier.
"""
from __future__ import annotations

import io
import wave
from pathlib import Path
from typing import Callable, Optional, Union

import numpy as np

try:  # SpeechRecognition is an optional runtime dependency for the CLI/tests.
    import speech_recognition as sr
except ImportError:  # pragma: no cover - depends on the local environment
    sr = None  # type: ignore[assignment]

from ..config import ASR_CONFIG, AUDIO_CONFIG

_WAV_LIKE = {".wav", ".aiff", ".aif", ".flac"}


class TeluguASR:
    """Thin, defensive wrapper around Google Speech Recognition for ``te-IN``."""

    def __init__(self, config: dict | None = None) -> None:
        self.config = config or ASR_CONFIG
        self.language: str = self.config["language"]
        self.timeout: int = self.config["timeout"]
        self.phrase_time_limit: int = self.config["phrase_time_limit"]

        self.recognizer = None
        if sr is not None:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = self.config["energy_threshold"]

    @property
    def available(self) -> bool:
        return self.recognizer is not None

    def _require_backend(self) -> None:
        if self.recognizer is None:
            raise RuntimeError(
                "SpeechRecognition is not installed. Run: pip install SpeechRecognition"
            )

    # ------------------------------------------------------------------ files
    def recognize_from_file(self, audio_path: Union[str, Path]) -> str:
        """Transcribe a WAV/FLAC/AIFF/MP3 file.

        Formats SpeechRecognition cannot open directly are decoded with librosa
        and sent through the in-memory path.
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        self._require_backend()

        if audio_path.suffix.lower() in _WAV_LIKE:
            try:
                with sr.AudioFile(str(audio_path)) as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
                    audio_data = self.recognizer.record(source)
                return self._recognize(audio_data)
            except sr.UnknownValueError:
                return "[గుర్తించలేదు - Speech not recognized]"
            except sr.RequestError as exc:
                return f"[API లోపం - API Error: {exc}]"
            except Exception:
                # Fall through to the librosa decoder for unusual WAV encodings.
                pass

        try:
            import librosa

            audio, sr_rate = librosa.load(
                str(audio_path), sr=AUDIO_CONFIG["sample_rate"], mono=True
            )
            return self.recognize_from_audio_data(audio, sr_rate)
        except Exception as exc:
            return f"[లోపం - Error: {exc}]"

    # ------------------------------------------------------------- microphone
    def recognize_from_microphone(
        self,
        timeout: int | None = None,
        phrase_time_limit: int | None = None,
        on_listen_complete: Optional[Callable[[], None]] = None,
        on_status: Optional[Callable[[str], None]] = None,
    ) -> str:
        """Record one phrase and return its Telugu transcript."""
        self._require_backend()
        timeout = timeout or self.timeout
        phrase_time_limit = phrase_time_limit or self.phrase_time_limit

        try:
            with sr.Microphone() as source:
                if on_status:
                    on_status("🎤 మాట్లాడండి... (Speak now)")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                audio_data = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )

            if on_listen_complete:
                on_listen_complete()
            if on_status:
                on_status("📝 గుర్తిస్తోంది... (Recognizing)")
            return self._recognize(audio_data)

        except sr.WaitTimeoutError:
            return "[సమయం ముగిసింది - Timeout: No speech detected]"
        except sr.UnknownValueError:
            return "[గుర్తించలేదు - Speech not recognized]"
        except sr.RequestError as exc:
            return f"[API లోపం - API Error: {exc}]"
        except AttributeError as exc:
            if "NoneType" in str(exc):
                return "[మైక్రోఫోన్ లోపం - Mic unavailable: install PyAudio]"
            return f"[లోపం - Error: {exc}]"
        except Exception as exc:
            return f"[లోపం - Error: {exc}]"

    # ----------------------------------------------------------------- arrays
    def recognize_from_audio_data(
        self, audio_data: np.ndarray, sample_rate: int | None = None
    ) -> str:
        """Transcribe a float mono signal in ``[-1, 1]``."""
        self._require_backend()
        sample_rate = sample_rate or AUDIO_CONFIG["sample_rate"]

        try:
            audio = np.asarray(audio_data, dtype=np.float32)
            if audio.ndim > 1:
                audio = audio.mean(axis=1)
            peak = float(np.max(np.abs(audio))) if audio.size else 0.0
            if peak > 0:
                audio = audio / peak

            buffer = io.BytesIO()
            with wave.open(buffer, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes((audio * 32767).astype(np.int16).tobytes())
            buffer.seek(0)

            with sr.AudioFile(buffer) as source:
                data = self.recognizer.record(source)
            return self._recognize(data)

        except sr.UnknownValueError:
            return "[గుర్తించలేదు - Speech not recognized]"
        except sr.RequestError as exc:
            return f"[API లోపం - API Error: {exc}]"
        except Exception as exc:
            return f"[లోపం - Error: {exc}]"

    # ---------------------------------------------------------------- helpers
    def _recognize(self, audio_data) -> str:
        return self.recognizer.recognize_google(audio_data, language=self.language)

    def get_available_microphones(self) -> list[str]:
        if sr is None:
            return []
        try:
            return sr.Microphone.list_microphone_names()
        except Exception:
            return []


def recognize_telugu(audio_path: str) -> str:
    """Convenience helper used by scripts and tests."""
    return TeluguASR().recognize_from_file(audio_path)
