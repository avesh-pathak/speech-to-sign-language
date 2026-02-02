"""
Audio Processing Module
Extracts spectral and MFCC features from Telugu speech audio
"""
import numpy as np
import librosa
import warnings
from pathlib import Path
from typing import Optional, Tuple, Union
import sys

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import AUDIO_CONFIG

warnings.filterwarnings('ignore')


class AudioProcessor:
    """
    Audio processing class for extracting dual features (Spectral + MFCC)
    from Telugu speech audio files.
    """
    
    def __init__(self, config: dict = None):
        """Initialize audio processor with configuration"""
        self.config = config or AUDIO_CONFIG
        self.sample_rate = self.config["sample_rate"]
        self.n_mfcc = self.config["n_mfcc"]
        self.n_fft = self.config["n_fft"]
        self.hop_length = self.config["hop_length"]
        self.max_length = self.config["max_audio_length"]
    
    def load_audio(self, audio_path: Union[str, Path]) -> Tuple[np.ndarray, int]:
        """
        Load and preprocess audio file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Tuple of (audio signal, sample rate)
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Load audio with librosa
        audio, sr = librosa.load(
            str(audio_path), 
            sr=self.sample_rate,
            mono=True,
            duration=self.max_length
        )
        
        # Normalize audio
        audio = self._normalize_audio(audio)
        
        return audio, sr
    
    def _normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        """Normalize audio to [-1, 1] range"""
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val
        return audio
    
    def extract_mfcc_features(
        self, 
        audio: np.ndarray, 
        sr: int = None
    ) -> np.ndarray:
        """
        Extract MFCC (Mel-Frequency Cepstral Coefficients) features
        
        Args:
            audio: Audio signal as numpy array
            sr: Sample rate (uses default if None)
            
        Returns:
            MFCC features array of shape (n_mfcc, time_frames)
        """
        sr = sr or self.sample_rate
        
        # Extract MFCCs
        mfccs = librosa.feature.mfcc(
            y=audio,
            sr=sr,
            n_mfcc=self.n_mfcc,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )
        
        # Compute delta and delta-delta (velocity and acceleration)
        mfcc_delta = librosa.feature.delta(mfccs)
        mfcc_delta2 = librosa.feature.delta(mfccs, order=2)
        
        # Stack all MFCC features
        mfcc_features = np.vstack([mfccs, mfcc_delta, mfcc_delta2])
        
        return mfcc_features
    
    def extract_spectral_features(
        self, 
        audio: np.ndarray, 
        sr: int = None
    ) -> np.ndarray:
        """
        Extract spectral features from audio
        
        Features extracted:
        - Spectral Centroid
        - Spectral Bandwidth
        - Spectral Rolloff
        - Zero Crossing Rate
        - Spectral Contrast
        - Chroma Features
        
        Args:
            audio: Audio signal as numpy array
            sr: Sample rate (uses default if None)
            
        Returns:
            Spectral features array
        """
        sr = sr or self.sample_rate
        
        # Spectral Centroid - "brightness" of sound
        spectral_centroid = librosa.feature.spectral_centroid(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )
        
        # Spectral Bandwidth - width of the spectrum
        spectral_bandwidth = librosa.feature.spectral_bandwidth(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )
        
        # Spectral Rolloff - frequency below which 85% of energy is contained
        spectral_rolloff = librosa.feature.spectral_rolloff(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )
        
        # Zero Crossing Rate - rate of sign changes
        zero_crossing = librosa.feature.zero_crossing_rate(
            audio, frame_length=self.n_fft, hop_length=self.hop_length
        )
        
        # Spectral Contrast - difference in amplitude between peaks and valleys
        spectral_contrast = librosa.feature.spectral_contrast(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )
        
        # Chroma Features - pitch class representation
        chroma = librosa.feature.chroma_stft(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )
        
        # Stack all spectral features
        spectral_features = np.vstack([
            spectral_centroid,
            spectral_bandwidth,
            spectral_rolloff,
            zero_crossing,
            spectral_contrast,
            chroma
        ])
        
        return spectral_features
    
    def extract_dual_features(
        self, 
        audio_path: Union[str, Path]
    ) -> np.ndarray:
        """
        Extract combined dual features (MFCC + Spectral) from audio file
        
        This is the main feature extraction method used by the Res-BiLSTM-AM model.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Combined feature array of shape (total_features, time_frames)
        """
        # Load audio
        audio, sr = self.load_audio(audio_path)
        
        # Extract both feature types
        mfcc_features = self.extract_mfcc_features(audio, sr)
        spectral_features = self.extract_spectral_features(audio, sr)
        
        # Ensure same number of time frames
        min_frames = min(mfcc_features.shape[1], spectral_features.shape[1])
        mfcc_features = mfcc_features[:, :min_frames]
        spectral_features = spectral_features[:, :min_frames]
        
        # Combine features
        dual_features = np.vstack([mfcc_features, spectral_features])
        
        return dual_features
    
    def extract_features_from_array(
        self, 
        audio: np.ndarray, 
        sr: int = None
    ) -> np.ndarray:
        """
        Extract dual features from audio array (for real-time processing)
        
        Args:
            audio: Audio signal as numpy array
            sr: Sample rate
            
        Returns:
            Combined feature array
        """
        sr = sr or self.sample_rate
        audio = self._normalize_audio(audio)
        
        mfcc_features = self.extract_mfcc_features(audio, sr)
        spectral_features = self.extract_spectral_features(audio, sr)
        
        min_frames = min(mfcc_features.shape[1], spectral_features.shape[1])
        mfcc_features = mfcc_features[:, :min_frames]
        spectral_features = spectral_features[:, :min_frames]
        
        return np.vstack([mfcc_features, spectral_features])
    
    def prepare_for_model(
        self, 
        features: np.ndarray, 
        max_frames: int = 200
    ) -> np.ndarray:
        """
        Prepare features for model input (padding/truncating)
        
        Args:
            features: Feature array of shape (n_features, time_frames)
            max_frames: Maximum number of time frames
            
        Returns:
            Padded/truncated features of shape (max_frames, n_features)
        """
        # Transpose to (time_frames, n_features)
        features = features.T
        
        current_frames = features.shape[0]
        
        if current_frames > max_frames:
            # Truncate
            features = features[:max_frames, :]
        elif current_frames < max_frames:
            # Pad with zeros
            padding = np.zeros((max_frames - current_frames, features.shape[1]))
            features = np.vstack([features, padding])
        
        return features


def extract_features(audio_path: str) -> np.ndarray:
    """
    Convenience function to extract dual features from audio file
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Feature array ready for model input
    """
    processor = AudioProcessor()
    features = processor.extract_dual_features(audio_path)
    return processor.prepare_for_model(features)


if __name__ == "__main__":
    # Test the audio processor
    import sys
    
    print("=" * 60)
    print("Audio Processor Test")
    print("=" * 60)
    
    processor = AudioProcessor()
    print(f"\nConfiguration:")
    print(f"  Sample Rate: {processor.sample_rate} Hz")
    print(f"  MFCC Coefficients: {processor.n_mfcc}")
    print(f"  FFT Size: {processor.n_fft}")
    print(f"  Hop Length: {processor.hop_length}")
    
    # Create a test audio signal (sine wave)
    duration = 2.0  # seconds
    t = np.linspace(0, duration, int(processor.sample_rate * duration))
    test_audio = 0.5 * np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
    
    print(f"\nTest Audio: {duration}s @ 440 Hz")
    print(f"  Shape: {test_audio.shape}")
    
    # Extract features
    mfcc = processor.extract_mfcc_features(test_audio)
    spectral = processor.extract_spectral_features(test_audio)
    combined = processor.extract_features_from_array(test_audio)
    
    print(f"\nExtracted Features:")
    print(f"  MFCC Shape: {mfcc.shape} (3x{processor.n_mfcc} coefficients x time)")
    print(f"  Spectral Shape: {spectral.shape}")
    print(f"  Combined Shape: {combined.shape}")
    
    # Prepare for model
    model_input = processor.prepare_for_model(combined)
    print(f"\nModel Input Shape: {model_input.shape} (time x features)")
    
    print("\n✅ Audio Processor Test Passed!")
