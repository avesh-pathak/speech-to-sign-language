"""Model architecture smoke tests (skipped when TensorFlow is unavailable)."""
import numpy as np
import pytest

pytest.importorskip("tensorflow")

from telugu_s2sl.model.res_bilstm_am import create_model  # noqa: E402


def test_model_forward_pass():
    model = create_model(
        {
            "lstm_units": 8,
            "attention_heads": 2,
            "dropout_rate": 0.1,
            "learning_rate": 0.001,
            "embedding_dim": 16,
            "num_classes": 5,
            "input_shape": (32, 143),
        }
    )

    output = model.predict(np.random.randn(2, 32, 143).astype(np.float32), verbose=0)
    assert output.shape == (2, 5)
    assert np.allclose(output.sum(axis=1), 1.0, atol=1e-5)
    assert model.name == "Res_BiLSTM_AM"
