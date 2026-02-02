"""
Training Pipeline for Telugu Speech-to-Sign Language Model
"""
import os
import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Dict

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))

# Set environment variable before importing TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from config.config import (
    MODEL_CONFIG, DATASET_PATHS, TRAINED_DIR,
    COMMON_TELUGU_WORDS, AUDIO_CONFIG
)
from models.res_bilstm_am import (
    create_model, get_callbacks, compile_model
)
from modules.audio_processor import AudioProcessor


from modules.sign_animator import SignAnimator

class TeluguSignDataset:
    """
    Dataset handler for Telugu Speech to Sign Language training
    """
    
    def __init__(self, audio_dir: Path = None):
        """Initialize dataset handler"""
        self.audio_dir = audio_dir or DATASET_PATHS["audio"]
        self.audio_processor = AudioProcessor()
        self.animator = SignAnimator()
        
        # Load mappings from file (synced with ISL Corpus)
        mapping_file = DATASET_PATHS["isl_mapping"]
        with open(mapping_file, 'r', encoding='utf-8') as f:
            full_mapping = json.load(f)
            
        # Filter to only include words that have available animations
        self.telugu_to_class = {}
        valid_words = []
        
        for telugu, isl_sign in full_mapping.items():
            if self.animator.has_sign(isl_sign):
                self.telugu_to_class[telugu] = len(valid_words)
                valid_words.append(isl_sign)
        
        self.class_names = valid_words
        self.num_classes = len(self.class_names)
        
        print(f"Initialized Dataset with {self.num_classes} classes (filtered from mapping)")
        
        # Feature dimensions
        self.max_frames = 200
        self.n_features = 143  # MFCC(40*3) + Spectral(23)
    
    def load_audio_samples(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load and process audio samples from the dataset directory
        
        Returns:
            Tuple of (features array, labels array)
        """
        features_list = []
        labels_list = []
        
        # 1. Load Transcriptions
        transcript_map = {}
        for gender in ['female', 'male']:
            index_file = self.audio_dir / f'line_index_{gender}.tsv'
            if index_file.exists():
                print(f"Loading transcriptions from {index_file.name}...")
                with open(index_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        parts = line.strip().split('\t')
                        if len(parts) >= 2:
                            file_id = parts[0]
                            text = parts[1]
                            transcript_map[file_id] = text
        
        print(f"Loaded {len(transcript_map)} transcriptions")

        audio_files = list(self.audio_dir.glob("**/*.wav"))
        audio_files.extend(list(self.audio_dir.glob("**/*.mp3")))
        
        print(f"Found {len(audio_files)} audio files")
        
        # 2. Match Audio to Classes
        processed_count = 0
        for audio_file in tqdm(audio_files, desc="Processing audio"):
            try:
                # Extract file_id (filename without extension)
                file_id = audio_file.stem
                
                if file_id not in transcript_map:
                    continue
                
                transcript = transcript_map[file_id]
                
                # Check if transcript contains any of our class words
                # Relaxed logic: keyword spotting in sentence
                matched_label = None
                
                # Check for any keyword occurrence
                for word, idx in self.telugu_to_class.items():
                    if word in transcript:
                        matched_label = idx
                        break
                
                if matched_label is None:
                    continue

                # Extract features
                try:
                    dual_features = self.audio_processor.extract_dual_features(audio_file)
                    features = self.audio_processor.prepare_for_model(
                        dual_features, self.max_frames
                    )
                    
                    features_list.append(features)
                    labels_list.append(matched_label)
                    processed_count += 1
                except Exception as e:
                    print(f"Feature extraction failed for {audio_file}: {e}")
                    continue
                
                # Limit samples to 1000 for faster demo training
                if processed_count >= 1000: 
                    print("Reached sample limit (1000). Stopping load.")
                    break
                    
            except Exception as e:
                print(f"Error processing {audio_file}: {e}")
                continue
        
        if not features_list:
            print("\n⚠️ No matching audio samples found in OpenSLR dataset.")
            print("   The dataset sentences might not overlap with your vocabulary.")
            print("   Using SYNTHETIC DATA for demonstration of training pipeline.")
            return self.create_synthetic_dataset(samples_per_class=20)
        
        X = np.array(features_list)
        y = np.array(labels_list)
        
        print(f"Final Real Dataset: {len(X)} samples")
        return X, y
    
    def create_synthetic_dataset(
        self, 
        samples_per_class: int = 50
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create synthetic dataset for testing/demonstration
        
        This generates random features with consistent patterns per class.
        Use this for testing the pipeline before real data is available.
        
        Args:
            samples_per_class: Number of samples per class
            
        Returns:
            Tuple of (features array, labels array)
        """
        print(f"Creating synthetic dataset: {samples_per_class} samples/class")
        
        X = []
        y = []
        
        for class_idx in range(self.num_classes):
            # Create class-specific pattern
            class_pattern = np.random.randn(1, self.n_features) * 0.1 + class_idx * 0.1
            
            for _ in range(samples_per_class):
                # Generate sample with class pattern + noise
                sample = np.random.randn(self.max_frames, self.n_features) * 0.3
                sample += class_pattern  # Add class-specific bias
                
                X.append(sample)
                y.append(class_idx)
        
        # Shuffle
        indices = np.random.permutation(len(X))
        X = np.array(X)[indices]
        y = np.array(y)[indices]
        
        print(f"Created dataset: X={X.shape}, y={y.shape}")
        
        return X, y


def train_model(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    config: dict = None
) -> tf.keras.Model:
    """
    Train the Res-BiLSTM-AM model
    
    Args:
        X_train: Training features
        y_train: Training labels
        X_val: Validation features
        y_val: Validation labels
        config: Model configuration
        
    Returns:
        Trained model
    """
    config = config or MODEL_CONFIG
    
    print("\n" + "=" * 60)
    print("Training Res-BiLSTM-AM Model")
    print("=" * 60)
    
    print(f"\nDataset Info:")
    print(f"  Training samples: {len(X_train)}")
    print(f"  Validation samples: {len(X_val)}")
    print(f"  Feature shape: {X_train.shape[1:]}")
    print(f"  Number of classes: {config['num_classes']}")
    
    # Create model
    print("\nCreating model...")
    model = create_model(config)
    
    # Get callbacks
    callbacks = get_callbacks('res_bilstm_am')
    
    # Train
    print("\nStarting training...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=config['epochs'],
        batch_size=config['batch_size'],
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final model
    final_path = TRAINED_DIR / 'res_bilstm_am_final.keras'
    model.save(str(final_path))
    print(f"\n✅ Model saved to: {final_path}")
    
    # Save training history
    history_path = TRAINED_DIR / 'training_history.json'
    history_data = {k: [float(v) for v in vals] for k, vals in history.history.items()}
    with open(history_path, 'w') as f:
        json.dump(history_data, f, indent=2)
    print(f"✅ Training history saved to: {history_path}")
    
    return model


def evaluate_model(model: tf.keras.Model, X_test: np.ndarray, y_test: np.ndarray):
    """
    Evaluate the trained model
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
    """
    print("\n" + "=" * 60)
    print("Model Evaluation")
    print("=" * 60)
    
    # Evaluate
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    
    print(f"\nTest Results:")
    print(f"  Loss: {loss:.4f}")
    print(f"  Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Per-class predictions
    predictions = model.predict(X_test, verbose=0)
    predicted_classes = np.argmax(predictions, axis=1)
    
    correct = np.sum(predicted_classes == y_test)
    print(f"  Correct predictions: {correct}/{len(y_test)}")
    
    return {"loss": loss, "accuracy": accuracy}


def main():
    """Main training pipeline"""
    print("\n" + "=" * 60)
    print("Telugu Speech-to-Sign Language Model Training")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize dataset handler
    dataset = TeluguSignDataset()
    
    # Check for real audio data
    audio_files = list(DATASET_PATHS["audio"].glob("**/*.wav"))
    audio_files.extend(list(DATASET_PATHS["audio"].glob("**/*.mp3")))
    
    if len(audio_files) > 10:
        print("\n📂 Loading real audio dataset...")
        X, y = dataset.load_audio_samples()
    else:
        print("\n⚠️ No audio dataset found. Using synthetic data for demonstration.")
        print("   To train with real data, add Telugu audio files to:")
        print(f"   {DATASET_PATHS['audio']}")
        X, y = dataset.create_synthetic_dataset(samples_per_class=30)
    
    if len(X) == 0:
        print("\n❌ No data available for training!")
        return
    
    # Update config with actual number of classes and input shape
    config = MODEL_CONFIG.copy()
    config['num_classes'] = dataset.num_classes
    config['input_shape'] = (dataset.max_frames, dataset.n_features)
    
    # Filter classes with < 5 samples to allow stratified split
    # We need enough samples for Train (70%), Val (15%), Test (15%)
    unique, counts = np.unique(y, return_counts=True)
    valid_classes = unique[counts >= 5]
    
    if len(valid_classes) < len(unique):
        print(f"\n⚠️ Filtering {len(unique) - len(valid_classes)} classes with < 5 samples")
        mask = np.isin(y, valid_classes)
        X = X[mask]
        y = y[mask]
        print(f"Dataset size after filtering: {len(X)}")
    
    if len(X) == 0:
        print("No valid data after filtering!")
        return

    # Split data: Paper specifies 75% training and 25% testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    # Train model (using testing set as validation for tracking)
    model = train_model(X_train, y_train, X_test, y_test, config)
    
    # Evaluate
    results = evaluate_model(model, X_test, y_test)
    
    # Save class names mapping
    class_mapping_path = TRAINED_DIR / 'class_mapping.json'
    with open(class_mapping_path, 'w', encoding='utf-8') as f:
        json.dump({
            "class_names": dataset.class_names,
            "telugu_to_class": dataset.telugu_to_class,
            "num_classes": dataset.num_classes
        }, f, ensure_ascii=False, indent=2)
    print(f"✅ Class mapping saved to: {class_mapping_path}")
    
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print(f"Final Accuracy: {results['accuracy']*100:.2f}%")
    print(f"Model saved to: {TRAINED_DIR}")


if __name__ == "__main__":
    main()
