# Modules package initialization
from .audio_processor import AudioProcessor, extract_features
from .asr_module import TeluguASR, recognize_telugu
from .nlp_translator import TeluguNLPTranslator, translate_telugu
from .sign_animator import SignAnimator, create_placeholder_gifs

__all__ = [
    'AudioProcessor',
    'extract_features',
    'TeluguASR',
    'recognize_telugu',
    'TeluguNLPTranslator',
    'translate_telugu',
    'SignAnimator',
    'create_placeholder_gifs',
]
