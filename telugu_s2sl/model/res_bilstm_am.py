"""Residual BiLSTM with Attention (Res-BiLSTM-AM).

Architecture used by the paper:

    input -> LayerNorm -> Multi-Head Attention (+ residual)
          -> BiLSTM -> Residual BiLSTM block
          -> GlobalAveragePooling -> Dense -> Softmax

The residual block follows the paper's ``LN -> ReLU -> BiLSTM -> + skip``
ordering, which keeps gradients stable in deeper recurrent stacks.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.layers import (
    Add,
    Bidirectional,
    Dense,
    Dropout,
    GlobalAveragePooling1D,
    Input,
    LSTM,
    LayerNormalization,
    MultiHeadAttention,
)
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

from ..config import MODEL_CONFIG, PATHS


class ResidualBiLSTMBlock(layers.Layer):
    """``LayerNorm -> ReLU -> BiLSTM -> Dropout`` with an identity skip."""

    def __init__(self, units: int, dropout_rate: float = 0.3, **kwargs) -> None:
        super().__init__(**kwargs)
        self.units = units
        self.dropout_rate = dropout_rate
        self.norm = LayerNormalization()
        self.relu = layers.Activation("relu")
        self.bilstm = Bidirectional(LSTM(units, return_sequences=True), merge_mode="concat")
        self.dropout = Dropout(dropout_rate)
        self.projection = None

    def build(self, input_shape) -> None:
        if input_shape[-1] != self.units * 2:
            self.projection = Dense(self.units * 2)
        super().build(input_shape)

    def call(self, inputs, training: bool = False):
        x = self.norm(inputs)
        x = self.relu(x)
        x = self.bilstm(x)
        x = self.dropout(x, training=training)

        residual = inputs if self.projection is None else self.projection(inputs)
        return x + residual

    def get_config(self) -> dict:
        config = super().get_config()
        config.update({"units": self.units, "dropout_rate": self.dropout_rate})
        return config


def build_res_bilstm_am_model(
    input_shape: tuple[int, int],
    num_classes: int,
    lstm_units: int = 128,
    attention_heads: int = 4,
    dropout_rate: float = 0.3,
    embedding_dim: int = 256,
) -> Model:
    """Build an uncompiled Res-BiLSTM-AM classifier."""
    inputs = Input(shape=input_shape, name="audio_features")

    x = LayerNormalization(name="initial_norm")(inputs)

    attention = MultiHeadAttention(
        num_heads=attention_heads,
        key_dim=max(1, embedding_dim // attention_heads),
        dropout=dropout_rate,
        name="attention_block",
    )(x, x)
    x = Add(name="attention_residual")([x, attention])
    x = LayerNormalization(name="attention_norm")(x)

    x = Bidirectional(
        LSTM(lstm_units, return_sequences=True), merge_mode="concat", name="initial_bilstm"
    )(x)
    x = ResidualBiLSTMBlock(lstm_units, dropout_rate, name="res_bilstm_block")(x)

    x = GlobalAveragePooling1D(name="temporal_pooling")(x)
    x = Dense(embedding_dim, activation="relu", name="dense_1")(x)
    x = Dropout(dropout_rate)(x)
    outputs = Dense(num_classes, activation="softmax", name="predictions")(x)

    return Model(inputs=inputs, outputs=outputs, name="Res_BiLSTM_AM")


def compile_model(model: Model, learning_rate: float = 0.001) -> Model:
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def create_model(config: dict | None = None) -> Model:
    """Create and compile a model from ``MODEL_CONFIG`` (or an override)."""
    config = {**MODEL_CONFIG, **(config or {})}
    input_shape = tuple(config.get("input_shape", MODEL_CONFIG["input_shape"]))

    model = build_res_bilstm_am_model(
        input_shape=input_shape,
        num_classes=config["num_classes"],
        lstm_units=config["lstm_units"],
        attention_heads=config["attention_heads"],
        dropout_rate=config["dropout_rate"],
        embedding_dim=config["embedding_dim"],
    )
    return compile_model(model, config["learning_rate"])


def get_callbacks(model_name: str = "res_bilstm_am") -> list:
    PATHS.trained.mkdir(parents=True, exist_ok=True)
    return [
        EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True, verbose=1),
        ModelCheckpoint(
            filepath=str(PATHS.trained / f"{model_name}_best.keras"),
            monitor="val_loss",
            save_best_only=True,
            verbose=1,
        ),
        ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=5, min_lr=1e-6, verbose=1
        ),
    ]


def load_model(model_path: str | Path | None = None) -> Model:
    path = Path(model_path or PATHS.trained_model)
    if not path.exists():
        raise FileNotFoundError(f"Model not found: {path}")
    return keras.models.load_model(
        str(path),
        custom_objects={"ResidualBiLSTMBlock": ResidualBiLSTMBlock},
    )


def predict_sign(
    model: Model, features: np.ndarray, class_names: list[str] | None = None
) -> dict:
    """Return the top-5 predictions for one ``(frames, features)`` array."""
    if features.ndim == 2:
        features = np.expand_dims(features, axis=0)

    predictions = model.predict(features, verbose=0)
    predicted_class = int(np.argmax(predictions[0]))
    top_indices = np.argsort(predictions[0])[-5:][::-1]

    return {
        "predicted_class": predicted_class,
        "predicted_name": class_names[predicted_class] if class_names else f"class_{predicted_class}",
        "confidence": float(predictions[0][predicted_class]),
        "top_predictions": [
            {
                "class": int(index),
                "name": class_names[index] if class_names else f"class_{index}",
                "confidence": float(predictions[0][index]),
            }
            for index in top_indices
        ],
    }
