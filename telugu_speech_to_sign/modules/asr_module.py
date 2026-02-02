"""
ASR (Automatic Speech Recognition) Module
Converts Telugu speech to text using Google Speech Recognition API
"""
import speech_recognition as sr
from pathlib import Path
from typing import Optional, Union
import sys
import io
import wave
import numpy as np

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import ASR_CONFIG, AUDIO_CONFIG


class TeluguASR:
    """
    Telugu Automatic Speech Recognition class
    Uses Google Speech Recognition API for Telugu language
    """
    
    def __init__(self, config: dict = None):
        """Initialize ASR with configuration"""
        self.config = config or ASR_CONFIG
        self.recognizer = sr.Recognizer()
        self.language = self.config["language"]
        self.timeout = self.config["timeout"]
        self.phrase_time_limit = self.config["phrase_time_limit"]
        self.recognizer.energy_threshold = self.config["energy_threshold"]
    
    def recognize_from_file(self, audio_path: Union[str, Path]) -> str:
        """
        Recognize Telugu speech from audio file
        
        Args:
            audio_path: Path to audio file (WAV, MP3, FLAC, etc.)
            
        Returns:
            Recognized Telugu text
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        try:
            with sr.AudioFile(str(audio_path)) as source:
                # Listen for ambient noise and adjust
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Record the audio
                audio_data = self.recognizer.record(source)
                
            # Recognize using Google Speech Recognition
            text = self.recognizer.recognize_google(
                audio_data, 
                language=self.language
            )
            return text
            
        except sr.UnknownValueError:
            return "[గుర్తించలేదు - Speech not recognized]"
        except sr.RequestError as e:
            return f"[API లోపం - API Error: {e}]"
        except Exception as e:
            return f"[లోపం - Error: {e}]"
    
    def recognize_from_microphone(
        self, 
        timeout: int = None,
        phrase_time_limit: int = None,
        on_listen_complete: callable = None
    ) -> str:
        """
        Recognize Telugu speech from microphone input
        
        Args:
            timeout: Maximum seconds to wait for phrase start
            phrase_time_limit: Maximum seconds for phrase duration
            on_listen_complete: Optional callback when listening ends and processing starts
            
        Returns:
            Recognized Telugu text
        """
        timeout = timeout or self.timeout
        phrase_time_limit = phrase_time_limit or self.phrase_time_limit
        
        try:
            with sr.Microphone() as source:
                print("🎤 మాట్లాడండి... (Speak now...)")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Listen for speech
                audio_data = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                print("📝 గుర్తిస్తోంది... (Recognizing...)")
                
                if on_listen_complete:
                    on_listen_complete()
            
            # Recognize using Google Speech Recognition
            text = self.recognizer.recognize_google(
                audio_data, 
                language=self.language
            )
            return text
            
        except sr.WaitTimeoutError:
            return "[సమయం ముగిసింది - Timeout: No speech detected]"
        except sr.UnknownValueError:
            return "[గుర్తించలేదు - Speech not recognized]"
        except sr.RequestError as e:
            return f"[API లోపం - API Error: {e}]"
        except AttributeError as e:
            if "'NoneType' object has no attribute 'close'" in str(e):
                return "[మైక్రోఫోన్ లోపం - Mic Error: Device not accessible or busy]"
            return f"[లోపం - Error: {e}]"
        except Exception as e:
            return f"[లోపం - Error: {e}]"
    
    def recognize_from_audio_data(
        self, 
        audio_data: np.ndarray, 
        sample_rate: int = None
    ) -> str:
        """
        Recognize Telugu speech from numpy audio array
        
        Args:
            audio_data: Audio signal as numpy array
            sample_rate: Sample rate of audio
            
        Returns:
            Recognized Telugu text
        """
        sample_rate = sample_rate or AUDIO_CONFIG["sample_rate"]
        
        try:
            # Convert numpy array to WAV bytes
            wav_buffer = io.BytesIO()
            
            # Normalize to int16
            audio_int16 = (audio_data * 32767).astype(np.int16)
            
            with wave.open(wav_buffer, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)  # 2 bytes for int16
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_int16.tobytes())
            
            wav_buffer.seek(0)
            
            # Create AudioData from WAV
            with sr.AudioFile(wav_buffer) as source:
                audio = self.recognizer.record(source)
            
            # Recognize
            text = self.recognizer.recognize_google(
                audio, 
                language=self.language
            )
            return text
            
        except sr.UnknownValueError:
            return "[గుర్తించలేదు - Speech not recognized]"
        except sr.RequestError as e:
            return f"[API లోపం - API Error: {e}]"
        except Exception as e:
            return f"[లోపం - Error: {e}]"
    
    def get_available_microphones(self) -> list:
        """Get list of available microphone devices"""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            return mic_list
        except Exception as e:
            print(f"Error listing microphones: {e}")
            return []


def recognize_telugu(audio_path: str) -> str:
    """
    Convenience function to recognize Telugu speech from file
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Recognized Telugu text
    """
    asr = TeluguASR()
    return asr.recognize_from_file(audio_path)


if __name__ == "__main__":
    print("=" * 60)
    print("Telugu ASR Module Test")
    print("=" * 60)
    
    asr = TeluguASR()
    
    print(f"\nConfiguration:")
    print(f"  Language: {asr.language}")
    print(f"  Timeout: {asr.timeout}s")
    print(f"  Phrase Limit: {asr.phrase_time_limit}s")
    
    # List available microphones
    mics = asr.get_available_microphones()
    if mics:
        print(f"\nAvailable Microphones:")
        for i, mic in enumerate(mics[:5]):  # Show first 5
            print(f"  [{i}] {mic}")
    
    print("\n✅ Telugu ASR Module Loaded Successfully!")
    print("\nTo test with microphone, call:")
    print("  asr = TeluguASR()")
    print("  text = asr.recognize_from_microphone()")
