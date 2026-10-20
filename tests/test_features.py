"""Tests for dual audio feature extraction."""
import numpy as np
import pytest

from telugu_s2sl.audio.features import AudioFeatureExtractor
from telugu_s2sl.config import N_AUDIO_FEATURES


@pytest.fixture()
def extractor():
    return AudioFeatureExtractor()


def _tone(seconds: float = 2.0, sample_rate: int = 16_000) -> np.ndarray:
    t = np.linspace(0, seconds, int(sample_rate * seconds), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * 440 * t)


def test_mfcc_shape(extractor):
    mfcc = extractor.extract_mfcc_features(_tone())
    assert mfcc.shape[0] == extractor.n_mfcc * 3
    assert mfcc.shape[1] > 0


def test_spectral_shape(extractor):
    spectral = extractor.extract_spectral_features(_tone())
    assert spectral.shape[0] == 23
    assert spectral.shape[1] > 0


def test_dual_features(extractor):
    features = extractor.extract_features_from_array(_tone())
    assert features.shape[0] == N_AUDIO_FEATURES
    assert features.shape[1] > 0


def test_prepare_for_model(extractor):
    prepared = extractor.prepare_for_model(np.zeros((N_AUDIO_FEATURES, 100)))
    assert prepared.shape == (200, N_AUDIO_FEATURES)
