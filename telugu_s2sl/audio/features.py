"""Dual audio feature extraction: MFCC (with deltas) + spectral descriptors.

The Res-BiLSTM-AM model receives a ``(200, 143)`` tensor per utterance:

* 40 MFCCs + 40 first deltas + 40 second deltas = 120
* centroid, bandwidth, rolloff, zero-crossing rate            = 4
* spectral contrast (7 bands) + chroma (12 pitch classes)     = 19
"""
from __future__ import annotations

import warnings
from pathlib import Path
from typing import Tuple, Union

import librosa
import numpy as np

from ..config import AUDIO_CONFIG, MAX_FRAMES, N_AUDIO_FEATURES

warnings.filterwarnings("ignore")


class AudioFeatureExtractor:
    """Extract the paper's dual spectral + MFCC representation from audio."""

    def __init__(self, config: dict | None = None) -> None:
        self.config = config or AUDIO_CONFIG
        self.sample_rate: int = self.config["sample_rate"]
        self.n_mfcc: int = self.config["n_mfcc"]
        self.n_fft: int = self.config["n_fft"]
        self.hop_length: int = self.config["hop_length"]
        self.max_length: int = self.config["max_audio_length"]

    # ------------------------------------------------------------------ input
    def load_audio(self, audio_path: Union[str, Path]) -> Tuple[np.ndarray, int]:
        """Load a mono 16 kHz signal, normalised to ``[-1, 1]``."""
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        audio, sr = librosa.load(
            str(audio_path),
            sr=self.sample_rate,
            mono=True,
            duration=self.max_length,
        )
        return self._normalize_audio(audio), sr

    def _normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        peak = float(np.max(np.abs(audio))) if audio.size else 0.0
        return audio / peak if peak > 0 else audio

    # --------------------------------------------------------------- features
    def extract_mfcc_features(self, audio: np.ndarray, sr: int | None = None) -> np.ndarray:
        """Return ``(3 * n_mfcc, frames)``: MFCC, delta and delta-delta."""
        sr = sr or self.sample_rate
        mfccs = librosa.feature.mfcc(
            y=audio,
            sr=sr,
            n_mfcc=self.n_mfcc,
            n_fft=self.n_fft,
            hop_length=self.hop_length,
        )
        mfcc_delta = librosa.feature.delta(mfccs)
        mfcc_delta2 = librosa.feature.delta(mfccs, order=2)
        return np.vstack([mfccs, mfcc_delta, mfcc_delta2])

    def extract_spectral_features(self, audio: np.ndarray, sr: int | None = None) -> np.ndarray:
        """Return ``(23, frames)`` spectral descriptors."""
        sr = sr or self.sample_rate

        centroid = librosa.feature.spectral_centroid(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )
        bandwidth = librosa.feature.spectral_bandwidth(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )
        rolloff = librosa.feature.spectral_rolloff(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )
        zcr = librosa.feature.zero_crossing_rate(
            audio, frame_length=self.n_fft, hop_length=self.hop_length
        )
        contrast = librosa.feature.spectral_contrast(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )
        chroma = librosa.feature.chroma_stft(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )

        return np.vstack([centroid, bandwidth, rolloff, zcr, contrast, chroma])

    def extract_dual_features(self, audio_path: Union[str, Path]) -> np.ndarray:
        """Return ``(143, frames)`` for an audio file."""
        audio, sr = self.load_audio(audio_path)
        return self.extract_features_from_array(audio, sr)

    def extract_features_from_array(
        self, audio: np.ndarray, sr: int | None = None
    ) -> np.ndarray:
        """Return ``(143, frames)`` for an in-memory signal."""
        sr = sr or self.sample_rate
        audio = self._normalize_audio(audio)

        mfcc = self.extract_mfcc_features(audio, sr)
        spectral = self.extract_spectral_features(audio, sr)

        min_frames = min(mfcc.shape[1], spectral.shape[1])
        return np.vstack([mfcc[:, :min_frames], spectral[:, :min_frames]])

    # --------------------------------------------------------------- model I/O
    def prepare_for_model(
        self, features: np.ndarray, max_frames: int = MAX_FRAMES
    ) -> np.ndarray:
        """Transpose, pad/truncate to ``(max_frames, 143)``."""
        features = features.T
        frames = features.shape[0]

        if frames > max_frames:
            return features[:max_frames, :]
        if frames < max_frames:
            padding = np.zeros((max_frames - frames, features.shape[1]), dtype=features.dtype)
            return np.vstack([features, padding])
        return features

    @property
    def n_features(self) -> int:
        return N_AUDIO_FEATURES


# Backwards-compatible alias for the original project API.
AudioProcessor = AudioFeatureExtractor


def extract_features(audio_path: str) -> np.ndarray:
    """Convenience helper: audio file -> ``(200, 143)`` model input."""
    extractor = AudioFeatureExtractor()
    return extractor.prepare_for_model(extractor.extract_dual_features(audio_path))
