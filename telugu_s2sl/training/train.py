"""Training pipeline for the Res-BiLSTM-AM acoustic classifier.

The model learns a mapping from dual audio features to ISL gloss classes.  It
is the paper's acoustic branch; the GUI's default runtime uses Google ASR plus
the dictionary translator, and can be switched to a trained checkpoint once a
labelled Telugu/ISL audio set is available.

Run with::

    python app.py --mode train
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from sklearn.model_selection import train_test_split

from ..animation.corpus import ISLCorpusAnimator
from ..audio.features import AudioFeatureExtractor
from ..config import COMMON_TELUGU_WORDS, MAX_FRAMES, MODEL_CONFIG, N_AUDIO_FEATURES, PATHS

try:
    from tqdm import tqdm
except ImportError:  # pragma: no cover
    def tqdm(iterable, **kwargs):
        return iterable


class TeluguSignDataset:
    """Load OpenSLR-style Telugu audio and map transcripts to sign classes."""

    def __init__(self, audio_dir: Path | None = None) -> None:
        self.audio_dir = Path(audio_dir or PATHS.audio)
        self.extractor = AudioFeatureExtractor()
        self.animator = ISLCorpusAnimator()

        self.telugu_to_class: Dict[str, int] = {}
        self.class_names: List[str] = []
        self._load_classes()

        self.max_frames = MAX_FRAMES
        self.n_features = N_AUDIO_FEATURES

    def _load_classes(self) -> None:
        mapping: Dict[str, str] = dict(COMMON_TELUGU_WORDS)
        if PATHS.telugu_to_isl.exists():
            with open(PATHS.telugu_to_isl, "r", encoding="utf-8") as handle:
                mapping.update(json.load(handle))

        has_corpus = bool(self.animator.available_signs)
        sign_to_index: Dict[str, int] = {}

        for telugu, sign in mapping.items():
            if has_corpus and not self.animator.has_sign(sign):
                continue
            if sign not in sign_to_index:
                sign_to_index[sign] = len(self.class_names)
                self.class_names.append(sign)
            self.telugu_to_class[telugu] = sign_to_index[sign]

        source = "corpus-filtered mapping" if has_corpus else "mapping (no corpus found)"
        print(f"Loaded {len(self.class_names)} classes from {source}")

    # ------------------------------------------------------------------ data
    def load_audio_samples(self) -> Tuple[np.ndarray, np.ndarray]:
        """Extract features for every audio file whose transcript matches a class."""
        transcripts: Dict[str, str] = {}
        for gender in ("female", "male"):
            index_file = self.audio_dir / f"line_index_{gender}.tsv"
            if not index_file.exists():
                continue
            with open(index_file, "r", encoding="utf-8") as handle:
                for line in handle:
                    parts = line.rstrip("\n").split("\t")
                    if len(parts) >= 2:
                        transcripts[parts[0]] = parts[1]

        audio_files = sorted(self.audio_dir.rglob("*.wav")) + sorted(self.audio_dir.rglob("*.mp3"))
        print(f"Found {len(transcripts)} transcripts and {len(audio_files)} audio files")

        features: List[np.ndarray] = []
        labels: List[int] = []

        for audio_file in tqdm(audio_files, desc="Extracting features"):
            transcript = transcripts.get(audio_file.stem)
            if not transcript:
                continue

            label = next(
                (index for word, index in self.telugu_to_class.items() if word in transcript),
                None,
            )
            if label is None:
                continue

            try:
                dual = self.extractor.extract_dual_features(audio_file)
                features.append(self.extractor.prepare_for_model(dual, self.max_frames))
                labels.append(label)
            except Exception as exc:
                print(f"Skipping {audio_file.name}: {exc}")
                continue

            if len(features) >= 1000:
                print("Reached the 1,000-sample demo limit.")
                break

        if not features:
            print("No labelled audio found; falling back to synthetic data.")
            return self.create_synthetic_dataset(samples_per_class=20)

        print(f"Loaded {len(features)} real samples")
        return np.asarray(features, dtype=np.float32), np.asarray(labels, dtype=np.int64)

    def create_synthetic_dataset(
        self, samples_per_class: int = 30
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Generate separable noise so the training loop can be smoke-tested."""
        if not self.class_names:
            return np.empty((0, self.max_frames, self.n_features)), np.empty((0,), dtype=np.int64)

        print(f"Creating synthetic dataset: {samples_per_class} samples/class")
        rng = np.random.default_rng(42)
        features, labels = [], []

        for class_index in range(len(self.class_names)):
            pattern = rng.standard_normal((1, self.n_features)) * 0.1 + class_index * 0.1
            for _ in range(samples_per_class):
                sample = rng.standard_normal((self.max_frames, self.n_features)) * 0.3 + pattern
                features.append(sample.astype(np.float32))
                labels.append(class_index)

        permutation = rng.permutation(len(features))
        x = np.asarray(features, dtype=np.float32)[permutation]
        y = np.asarray(labels, dtype=np.int64)[permutation]
        print(f"Created dataset: X={x.shape}, y={y.shape}")
        return x, y


def train_model(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_val: np.ndarray,
    y_val: np.ndarray,
    config: dict | None = None,
):
    from ..model.res_bilstm_am import create_model, get_callbacks

    config = {**MODEL_CONFIG, **(config or {})}
    print(f"Training on {len(x_train)} samples, validating on {len(x_val)}")
    model = create_model(config)

    history = model.fit(
        x_train,
        y_train,
        validation_data=(x_val, y_val),
        epochs=config["epochs"],
        batch_size=config["batch_size"],
        callbacks=get_callbacks("res_bilstm_am"),
        verbose=1,
    )

    PATHS.trained.mkdir(parents=True, exist_ok=True)
    model.save(str(PATHS.trained / "res_bilstm_am_final.keras"))
    with open(PATHS.trained / "training_history.json", "w", encoding="utf-8") as handle:
        json.dump(
            {key: [float(value) for value in values] for key, values in history.history.items()},
            handle,
            indent=2,
        )
    return model


def evaluate_model(model, x_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
    loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"Test loss: {loss:.4f} | accuracy: {accuracy * 100:.2f}%")
    return {"loss": float(loss), "accuracy": float(accuracy)}


def main() -> None:
    print("=" * 64)
    print("Telugu Speech-to-Sign — Res-BiLSTM-AM training")
    print(f"Started: {datetime.now():%Y-%m-%d %H:%M:%S}")
    print("=" * 64)

    dataset = TeluguSignDataset()
    audio_files = list(PATHS.audio.rglob("*.wav")) + list(PATHS.audio.rglob("*.mp3"))

    if len(audio_files) > 10:
        x, y = dataset.load_audio_samples()
    else:
        print("No audio dataset found; using synthetic data for a pipeline smoke test.")
        x, y = dataset.create_synthetic_dataset(samples_per_class=30)

    if len(x) == 0:
        print("No data available for training.")
        return

    # Keep classes with at least 5 samples so a stratified split is valid.
    unique, counts = np.unique(y, return_counts=True)
    valid = unique[counts >= 5]
    if len(valid) < len(unique):
        mask = np.isin(y, valid)
        x, y = x[mask], y[mask]
        print(f"Filtered rare classes; {len(x)} samples remain")

    if len(x) == 0:
        print("No valid data after filtering.")
        return

    config = {
        **MODEL_CONFIG,
        "num_classes": len(dataset.class_names),
        "input_shape": (dataset.max_frames, dataset.n_features),
    }

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y
    )

    model = train_model(x_train, y_train, x_test, y_test, config)
    results = evaluate_model(model, x_test, y_test)

    with open(PATHS.class_mapping, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "class_names": dataset.class_names,
                "telugu_to_class": dataset.telugu_to_class,
                "num_classes": len(dataset.class_names),
                "input_shape": [dataset.max_frames, dataset.n_features],
                "test_accuracy": results["accuracy"],
            },
            handle,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Saved model and class map to {PATHS.trained}")


if __name__ == "__main__":
    main()
