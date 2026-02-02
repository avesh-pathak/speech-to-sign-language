"""
Residual Bidirectional LSTM with Attention Mechanism (Res-BiLSTM-AM)
Deep Learning Model for Telugu Speech to Sign Language Translation
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from tensorflow.keras.layers import (
    Input, Dense, LSTM, Bidirectional, Dropout, 
    Add, LayerNormalization, MultiHeadAttention,
    GlobalAveragePooling1D, Concatenate, BatchNormalization
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from pathlib import Path
import sys

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import MODEL_CONFIG, TRAINED_DIR


class AttentionLayer(layers.Layer):
    """
    Custom Attention Layer for sequence-to-sequence attention
    """
    
    def __init__(self, units: int, **kwargs):
        super().__init__(**kwargs)
        self.units = units
        self.W = Dense(units)
        self.U = Dense(units)
        self.V = Dense(1)
    
    def call(self, hidden_states, encoder_output):
        """
        Compute attention weights and context vector
        
        Args:
            hidden_states: Current decoder hidden state
            encoder_output: All encoder outputs
            
        Returns:
            Context vector weighted by attention
        """
        # hidden_states shape: (batch, features)
        # encoder_output shape: (batch, time_steps, features)
        
        # Expand hidden states for addition
        hidden_with_time = tf.expand_dims(hidden_states, 1)
        
        # Score calculation
        score = self.V(tf.nn.tanh(
            self.W(encoder_output) + self.U(hidden_with_time)
        ))
        
        # Attention weights
        attention_weights = tf.nn.softmax(score, axis=1)
        
        # Context vector
        context = attention_weights * encoder_output
        context = tf.reduce_sum(context, axis=1)
        
        return context, attention_weights
    
    def get_config(self):
        config = super().get_config()
        config.update({"units": self.units})
        return config


class ResidualBiLSTMBlock(layers.Layer):
    """
    Residual Bidirectional LSTM Block as per paper Fig 3 logic:
    Normalization -> ReLU -> BiLSTM -> Addition (Skip)
    """
    
    def __init__(self, units: int, dropout_rate: float = 0.3, **kwargs):
        super().__init__(**kwargs)
        self.units = units
        self.dropout_rate = dropout_rate
        
        # Components
        self.norm = LayerNormalization()
        self.relu = layers.Activation('relu')
        self.bilstm = Bidirectional(
            LSTM(units, return_sequences=True),
            merge_mode='concat'
        )
        self.dropout = Dropout(dropout_rate)
        self.projection = None
    
    def build(self, input_shape):
        # Result of concat BiLSTM is units * 2
        if input_shape[-1] != self.units * 2:
            self.projection = Dense(self.units * 2)
        super().build(input_shape)
    
    def call(self, inputs, training=False):
        # Normalization -> ReLU -> BiLSTM
        x = self.norm(inputs)
        x = self.relu(x)
        x = self.bilstm(x)
        x = self.dropout(x, training=training)
        
        # Residual connection
        residual = inputs
        if self.projection is not None:
            residual = self.projection(inputs)
            
        return x + residual

    def get_config(self):
        config = super().get_config()
        config.update({
            "units": self.units,
            "dropout_rate": self.dropout_rate
        })
        return config


def build_res_bilstm_am_model(
    input_shape: tuple,
    num_classes: int,
    lstm_units: int = 128,
    attention_heads: int = 4,
    dropout_rate: float = 0.3,
    embedding_dim: int = 256
) -> Model:
    """
    Build the Residual BiLSTM with Attention Mechanism model 
    following the PDF methodology.
    
    Architecture (Fig 3 interpretation):
    Input -> Norm -> Attention -> BiLSTM -> Residual Block -> Pool -> Dense
    """
    
    # Input layer
    inputs = Input(shape=input_shape, name='audio_features')
    
    # 1. Normalization (Preferred in paper text)
    x = LayerNormalization(name='initial_norm')(inputs)
    
    # 2. Attention Mechanism (Focus on relevant audio segments)
    # Using MultiHeadAttention as the "AM" implementation
    attn_out = MultiHeadAttention(
        num_heads=attention_heads,
        key_dim=embedding_dim // attention_heads,
        dropout=dropout_rate,
        name='attention_block'
    )(x, x)
    x = Add(name='attn_residual')([x, attn_out])
    x = LayerNormalization(name='attn_norm')(x)
    
    # 3. Bi-LSTM Layer (Initial temporal context)
    x = Bidirectional(
        LSTM(lstm_units, return_sequences=True),
        merge_mode='concat',
        name='initial_bilstm'
    )(x)
    
    # 4. Residual BiLSTM Block (Fig 3: BN -> ReLU -> BiLSTM + Skip)
    x = ResidualBiLSTMBlock(lstm_units, dropout_rate, name='res_bilstm_block')(x)
    
    # 5. Global Aggregation
    x = GlobalAveragePooling1D(name='temporal_pooling')(x)
    
    # 6. Classification Layers
    x = Dense(embedding_dim, activation='relu', name='dense_1')(x)
    x = Dropout(dropout_rate)(x)
    
    # Output
    outputs = Dense(num_classes, activation='softmax', name='predictions')(x)
    
    model = Model(inputs=inputs, outputs=outputs, name='Paper_Res_BiLSTM_AM')
    
    return model


def compile_model(model: Model, learning_rate: float = 0.001) -> Model:
    """
    Compile the model with optimizer and loss function
    
    Args:
        model: Keras Model
        learning_rate: Learning rate for Adam optimizer
        
    Returns:
        Compiled model
    """
    optimizer = Adam(learning_rate=learning_rate)
    
    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def get_callbacks(model_name: str = 'res_bilstm_am') -> list:
    """
    Get training callbacks
    
    Args:
        model_name: Name for saved model files
        
    Returns:
        List of Keras callbacks
    """
    # Ensure trained directory exists
    TRAINED_DIR.mkdir(parents=True, exist_ok=True)
    
    callbacks = [
        # Early stopping to prevent overfitting
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        
        # Save best model
        ModelCheckpoint(
            filepath=str(TRAINED_DIR / f'{model_name}_best.keras'),
            monitor='val_loss',
            save_best_only=True,
            verbose=1
        ),
        
        # Reduce learning rate on plateau
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6,
            verbose=1
        )
    ]
    
    return callbacks


def create_model(config: dict = None) -> Model:
    """
    Create and compile the Res-BiLSTM-AM model with default configuration
    
    Args:
        config: Model configuration dictionary (uses MODEL_CONFIG if None)
        
    Returns:
        Compiled Keras Model
    """
    config = config or MODEL_CONFIG
    
    # Default input shape: (200 time steps, 140 features)
    # 140 = 40 MFCCs * 3 (mfcc + delta + delta2) + 20 spectral features
    input_shape = config.get('input_shape', (200, 140))
    
    model = build_res_bilstm_am_model(
        input_shape=input_shape,
        num_classes=config['num_classes'],
        lstm_units=config['lstm_units'],
        attention_heads=config['attention_heads'],
        dropout_rate=config['dropout_rate'],
        embedding_dim=config['embedding_dim']
    )
    
    model = compile_model(model, config['learning_rate'])
    
    return model


def load_model(model_path: str = None) -> Model:
    """
    Load a trained model from file
    
    Args:
        model_path: Path to saved model (uses default if None)
        
    Returns:
        Loaded Keras Model
    """
    if model_path is None:
        model_path = TRAINED_DIR / 'res_bilstm_am_best.keras'
    
    model_path = Path(model_path)
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")
    
    # Register custom layers
    custom_objects = {
        'AttentionLayer': AttentionLayer,
        'ResidualBiLSTMBlock': ResidualBiLSTMBlock
    }
    
    model = keras.models.load_model(str(model_path), custom_objects=custom_objects)
    return model


def predict_sign(model: Model, features: np.ndarray, class_names: list = None) -> dict:
    """
    Predict sign class from audio features
    
    Args:
        model: Trained model
        features: Audio features array of shape (time_steps, n_features)
        class_names: List of class names for mapping
        
    Returns:
        Dictionary with prediction results
    """
    # Ensure correct shape (add batch dimension if needed)
    if len(features.shape) == 2:
        features = np.expand_dims(features, axis=0)
    
    # Get predictions
    predictions = model.predict(features, verbose=0)
    
    # Get top predictions
    predicted_class = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_class])
    
    # Get top 5 predictions
    top_indices = np.argsort(predictions[0])[-5:][::-1]
    top_predictions = [
        {
            'class': int(idx),
            'name': class_names[idx] if class_names else f'class_{idx}',
            'confidence': float(predictions[0][idx])
        }
        for idx in top_indices
    ]
    
    return {
        'predicted_class': int(predicted_class),
        'predicted_name': class_names[predicted_class] if class_names else f'class_{predicted_class}',
        'confidence': confidence,
        'top_predictions': top_predictions
    }


if __name__ == "__main__":
    print("=" * 60)
    print("Res-BiLSTM-AM Model Test")
    print("=" * 60)
    
    # Create model
    print("\nCreating model...")
    model = create_model()
    
    # Print model summary
    print("\nModel Architecture:")
    print("-" * 60)
    model.summary()
    
    # Test with dummy data
    print("\n" + "-" * 60)
    print("Testing with dummy data...")
    
    # Create dummy input: (batch=1, time_steps=200, features=140)
    dummy_input = np.random.randn(1, 200, 140).astype(np.float32)
    
    # Get prediction
    output = model.predict(dummy_input, verbose=0)
    print(f"Input shape: {dummy_input.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Output (first 5 classes): {output[0][:5]}")
    
    # Save model path
    model_path = TRAINED_DIR / 'res_bilstm_am_test.keras'
    print(f"\nModel can be saved to: {model_path}")
    
    print("\n✅ Res-BiLSTM-AM Model Test Passed!")
