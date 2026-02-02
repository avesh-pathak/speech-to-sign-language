"""
Tests for Telugu Speech-to-Sign Language Translation System
"""
import sys
import numpy as np
from pathlib import Path
import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestAudioProcessor:
    """Tests for audio processing module"""
    
    def test_audio_processor_init(self):
        """Test AudioProcessor initialization"""
        from modules.audio_processor import AudioProcessor
        
        processor = AudioProcessor()
        assert processor.sample_rate == 16000
        assert processor.n_mfcc == 40
    
    def test_mfcc_extraction(self):
        """Test MFCC feature extraction"""
        from modules.audio_processor import AudioProcessor
        
        processor = AudioProcessor()
        
        # Create dummy audio signal
        duration = 2.0
        sample_rate = 16000
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = 0.5 * np.sin(2 * np.pi * 440 * t)
        
        # Extract MFCC
        mfcc = processor.extract_mfcc_features(audio, sample_rate)
        
        # Check output shape
        assert mfcc.shape[0] == processor.n_mfcc * 3  # MFCC + delta + delta2
        assert mfcc.shape[1] > 0  # Time frames
    
    def test_spectral_extraction(self):
        """Test spectral feature extraction"""
        from modules.audio_processor import AudioProcessor
        
        processor = AudioProcessor()
        
        # Create dummy audio
        audio = np.random.randn(16000 * 2)  # 2 seconds
        
        # Extract spectral features
        spectral = processor.extract_spectral_features(audio)
        
        # Check output exists
        assert spectral.shape[0] > 0
        assert spectral.shape[1] > 0
    
    def test_dual_feature_extraction(self):
        """Test combined dual feature extraction"""
        from modules.audio_processor import AudioProcessor
        
        processor = AudioProcessor()
        
        # Create dummy audio
        audio = np.random.randn(16000 * 2)
        
        # Extract both features
        combined = processor.extract_features_from_array(audio)
        
        # Should have more features than just MFCC
        assert combined.shape[0] > processor.n_mfcc * 3
    
    def test_prepare_for_model(self):
        """Test feature preparation for model input"""
        from modules.audio_processor import AudioProcessor
        
        processor = AudioProcessor()
        
        # Create dummy features
        features = np.random.randn(140, 100)  # (features, time)
        
        # Prepare for model
        prepared = processor.prepare_for_model(features, max_frames=200)
        
        # Check output shape
        assert prepared.shape == (200, 140)  # (time, features)


class TestNLPTranslator:
    """Tests for NLP translation module"""
    
    def test_translator_init(self):
        """Test NLPTranslator initialization"""
        from modules.nlp_translator import TeluguNLPTranslator
        
        translator = TeluguNLPTranslator()
        assert len(translator.word_mapping) > 0
    
    def test_tokenize(self):
        """Test Telugu text tokenization"""
        from modules.nlp_translator import TeluguNLPTranslator
        
        translator = TeluguNLPTranslator()
        
        text = "నమస్కారం ధన్యవాదాలు"
        tokens = translator.tokenize(text)
        
        assert len(tokens) == 2
        assert tokens[0] == "నమస్కారం"
        assert tokens[1] == "ధన్యవాదాలు"
    
    def test_word_to_sign_direct(self):
        """Test direct word-to-sign mapping"""
        from modules.nlp_translator import TeluguNLPTranslator
        
        translator = TeluguNLPTranslator()
        
        sign, is_direct = translator.word_to_sign("నమస్కారం")
        
        assert is_direct is True
        assert sign == "hello"
    
    def test_word_to_sign_no_match(self):
        """Test word without direct mapping"""
        from modules.nlp_translator import TeluguNLPTranslator
        
        translator = TeluguNLPTranslator()
        
        sign, is_direct = translator.word_to_sign("అజ్ఞాతపదం")
        
        assert is_direct is False
    
    def test_translate(self):
        """Test full translation"""
        from modules.nlp_translator import TeluguNLPTranslator
        
        translator = TeluguNLPTranslator()
        
        result = translator.translate("నమస్కారం")
        
        assert len(result) == 1
        assert result[0]["telugu"] == "నమస్కారం"
        assert result[0]["sign"] == "hello"
        assert result[0]["direct_match"] is True
    
    def test_get_sign_sequence(self):
        """Test sign sequence generation"""
        from modules.nlp_translator import TeluguNLPTranslator
        
        translator = TeluguNLPTranslator()
        
        signs = translator.get_sign_sequence("అవును కాదు")
        
        assert "yes" in signs
        assert "no" in signs


class TestSignAnimator:
    """Tests for sign animation module"""
    
    def test_animator_init(self):
        """Test SignAnimator initialization"""
        from modules.sign_animator import SignAnimator
        
        animator = SignAnimator()
        assert animator.gifs_dir is not None
    
    def test_get_available_signs(self):
        """Test getting available signs"""
        from modules.sign_animator import SignAnimator, create_placeholder_gifs
        
        # Create placeholders first
        create_placeholder_gifs()
        
        animator = SignAnimator()
        animator._scan_available_gifs()
        
        signs = animator.get_available_signs()
        # Should have some signs after creating placeholders
        assert isinstance(signs, list)


class TestModel:
    """Tests for the deep learning model"""
    
    def test_model_creation(self):
        """Test model creation"""
        from models.res_bilstm_am import create_model
        
        config = {
            'lstm_units': 64,
            'attention_heads': 2,
            'dropout_rate': 0.3,
            'learning_rate': 0.001,
            'embedding_dim': 128,
            'num_classes': 10,
        }
        
        model = create_model(config)
        
        assert model is not None
        assert model.name == 'Res_BiLSTM_AM'
    
    def test_model_forward_pass(self):
        """Test model forward pass"""
        from models.res_bilstm_am import create_model
        
        config = {
            'lstm_units': 32,
            'attention_heads': 2,
            'dropout_rate': 0.3,
            'learning_rate': 0.001,
            'embedding_dim': 64,
            'num_classes': 5,
        }
        
        model = create_model(config)
        
        # Create dummy input
        dummy_input = np.random.randn(2, 200, 140).astype(np.float32)
        
        # Forward pass
        output = model.predict(dummy_input, verbose=0)
        
        assert output.shape == (2, 5)
        # Should sum to 1 (softmax)
        assert np.allclose(output.sum(axis=1), 1.0, atol=1e-5)


class TestUtilities:
    """Tests for utility functions"""
    
    def test_is_telugu_text(self):
        """Test Telugu text detection"""
        from utils.helpers import is_telugu_text
        
        assert is_telugu_text("నమస్కారం") is True
        assert is_telugu_text("Hello") is False
        assert is_telugu_text("Hello నమస్కారం") is True
    
    def test_extract_telugu_words(self):
        """Test Telugu word extraction"""
        from utils.helpers import extract_telugu_words
        
        words = extract_telugu_words("Hello నమస్కారం World ధన్యవాదాలు")
        
        assert "నమస్కారం" in words
        assert "ధన్యవాదాలు" in words
        assert "Hello" not in words


class TestIntegration:
    """Integration tests for the full pipeline"""
    
    def test_full_translation_pipeline(self):
        """Test complete translation pipeline"""
        from modules.nlp_translator import TeluguNLPTranslator
        from modules.sign_animator import SignAnimator
        
        translator = TeluguNLPTranslator()
        animator = SignAnimator()
        
        # Translate text
        text = "నమస్కారం"
        result = translator.translate(text)
        
        # Get animation sequence
        sequence = animator.create_animation_sequence(result)
        
        assert len(sequence) > 0
        assert sequence[0]["telugu"] == "నమస్కారం"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
