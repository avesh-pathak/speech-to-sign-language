"""Inference wrapper for a trained Res-BiLSTM-AM checkpoint."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from ..audio.features import AudioFeatureExtractor
from ..config import PATHS
from .res_bilstm_am import load_model, predict_sign


class SignClassifier:
    """Classify an audio file into one of the trained ISL gloss classes."""

    def __init__(
        self,
        model_path: Path | None = None,
        mapping_path: Path | None = None,
    ) -> None:
        self.model_path = Path(model_path or PATHS.trained_model)
        self.mapping_path = Path(mapping_path or PATHS.class_mapping)

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"No trained model at {self.model_path}. Run: python app.py --mode train"
            )

        self.model = load_model(self.model_path)
        self.class_names: List[str] = self._load_class_names()
        self.extractor = AudioFeatureExtractor()

    def _load_class_names(self) -> List[str]:
        if not self.mapping_path.exists():
            return []
        with open(self.mapping_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return list(data.get("class_names", []))

    def predict_audio(self, audio_path: str | Path) -> Dict:
        features = self.extractor.extract_dual_features(audio_path)
        prepared = self.extractor.prepare_for_model(features)
        return predict_sign(self.model, prepared, self.class_names)
