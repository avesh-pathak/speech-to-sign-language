"""
ISL Corpus Sign Language Animator
Handles real frame-based animations from ISL_CORPUS
"""
import json
from pathlib import Path
from typing import List, Dict, Optional, Union
import sys
from PIL import Image
from dataclasses import dataclass

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import DATASET_PATHS, TELUGU_CONFIG, COMMON_TELUGU_WORDS


@dataclass
class SignFrame:
    """Represents a single frame from a sign sequence"""
    image: Image.Image
    frame_number: int
    total_frames: int
    sign_name: str


class ISLCorpusAnimator:
    """
    ISL Corpus-based Sign Language Animation Handler
    Uses real frame sequences from ISL_Corpus dataset
    """
    
    def __init__(self):
        """Initialize the ISL Corpus animator"""
        self.corpus_frames_dir = DATASET_PATHS.get("isl_corpus_frames")
        
        # Cache for loaded frame sequences
        self.frame_cache: Dict[str, List[Image.Image]] = {}
        
        # Mapping from Telugu to ISL Corpus signs
        self.telugu_isl_mapping = self._load_telugu_isl_mapping()
        
        # Available signs (sign name -> Path)
        self.available_signs: Dict[str, Path] = {}
        
        # Scan for available frame sequences
        self._scan_available_signs()
    
    def _load_telugu_isl_mapping(self) -> Dict[str, str]:
        """Load the Telugu to ISL Corpus mapping"""
        mapping_file = DATASET_PATHS.get("isl_corpus_mapping")
        if mapping_file and Path(mapping_file).exists():
            try:
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load ISL Corpus mapping: {e}")
        return {}
    
    def _scan_available_signs(self):
        """Scan ISL_Corpus directory for available sign sequences"""
        if self.corpus_frames_dir and self.corpus_frames_dir.exists():
            try:
                for item in self.corpus_frames_dir.iterdir():
                    if item.is_dir() and item.name != "New folder":  # Skip empty folders
                        # Folder name is the sign name (e.g. "HELLO_HI")
                        sign_name = item.name
                        sign_key = sign_name.lower().replace(" ", "_").replace("_-_", "_")
                        self.available_signs[sign_key] = item
            except Exception as e:
                pass  # Silent fail for encoding issues
    
    def get_available_signs(self) -> List[str]:
        """Get list of available sign names"""
        return list(self.available_signs.keys())
    
    def has_sign(self, sign_name: str) -> bool:
        """Check if a sign sequence exists"""
        return sign_name.lower().replace(" ", "_") in self.available_signs
    
    def load_sign_frames(self, sign_name: str) -> Optional[List[Image.Image]]:
        """
        Load all frames for a sign
        
        Args:
            sign_name: Name of the sign (e.g., "HELLO_HI", "THANK")
            
        Returns:
            List of PIL Image frames or None if not found
        """
        sign_key = sign_name.lower().replace(" ", "_")
        
        # Check cache
        if sign_key in self.frame_cache:
            return self.frame_cache[sign_key]
        
        # Check if sign exists
        if sign_key not in self.available_signs:
            return None
        
        # Load frames
        sign_dir = self.available_signs[sign_key]
        frames = []
        
        try:
            # Get all image files - handle various naming patterns
            image_files = []
            for pattern in ["*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG"]:
                image_files.extend(sign_dir.glob(pattern))
            
            # Sort by name - try numeric sort first
            def sort_key(path):
                # Extract numbers from filename
                import re
                numbers = re.findall(r'\d+', path.name)
                if numbers:
                    return (0, int(numbers[0]))  # 0 for numeric, then the number
                return (1, path.name)  # 1 for alphabetic fallback
            
            image_files = sorted(set(image_files), key=sort_key)
            
            if not image_files:
                return None
            
            for idx, img_path in enumerate(image_files):
                try:
                    img = Image.open(img_path)
                    # Ensure RGB for consistency
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    frames.append(img)
                except Exception as e:
                    pass
            
            if frames:
                self.frame_cache[sign_key] = frames
                return frames
            
        except Exception as e:
            pass
        
        return None
    
    def get_sign_for_telugu_word(self, telugu_word: str) -> Optional[str]:
        """
        Get the ISL Corpus sign name for a Telugu word
        
        Args:
            telugu_word: Telugu word
            
        Returns:
            Sign name if available, None otherwise
        """
        # Check direct mapping
        if telugu_word in self.telugu_isl_mapping:
            sign_name = self.telugu_isl_mapping[telugu_word]
            if self.has_sign(sign_name):
                return sign_name
        
        # Try case-insensitive lookup
        telugu_lower = telugu_word.lower()
        for mapped_word, sign_name in self.telugu_isl_mapping.items():
            if mapped_word.lower() == telugu_lower:
                if self.has_sign(sign_name):
                    return sign_name
        
        return None
    
    def create_animation_sequence(
        self, 
        telugu_words: List[str]
    ) -> List[Dict]:
        """
        Create animation sequence from Telugu words
        
        Args:
            telugu_words: List of Telugu words to translate
            
        Returns:
            List of animation frames with metadata
        """
        sequence = []
        
        for word in telugu_words:
            sign_name = self.get_sign_for_telugu_word(word)
            
            if sign_name:
                frames = self.load_sign_frames(sign_name)
                if frames:
                    sequence.append({
                        "type": "sign",
                        "telugu": word,
                        "isl_sign": sign_name,
                        "frames": frames,
                        "frame_count": len(frames),
                        "available": True
                    })
                else:
                    sequence.append({
                        "type": "text",
                        "telugu": word,
                        "isl_sign": sign_name,
                        "available": False,
                        "message": f"Sign '{sign_name}' frames could not be loaded"
                    })
            else:
                # No sign mapping found
                sequence.append({
                    "type": "text",
                    "telugu": word,
                    "isl_sign": None,
                    "available": False,
                    "message": f"No ISL mapping found for '{word}'"
                })
        
        return sequence
    
    def get_animation_timing(
        self,
        frame_count: int,
        fps: int = 10,
        transition_delay_ms: int = 200
    ) -> Dict:
        """
        Calculate timing information for animation
        
        Args:
            frame_count: Number of frames in the animation
            fps: Frames per second
            transition_delay_ms: Delay between signs in milliseconds
            
        Returns:
            Dictionary with timing information
        """
        frame_duration_ms = int(1000 / fps)
        total_duration_ms = (frame_count * frame_duration_ms) + transition_delay_ms
        
        return {
            "fps": fps,
            "frame_duration_ms": frame_duration_ms,
            "transition_delay_ms": transition_delay_ms,
            "frame_count": frame_count,
            "total_duration_ms": total_duration_ms,
            "total_duration_seconds": total_duration_ms / 1000
        }
    
    def clear_cache(self):
        """Clear the frame cache"""
        self.frame_cache.clear()
    
    def get_cache_info(self) -> Dict:
        """Get cache statistics"""
        total_frames = sum(len(frames) for frames in self.frame_cache.values())
        return {
            "cached_signs": len(self.frame_cache),
            "available_signs": len(self.available_signs),
            "total_cached_frames": total_frames,
            "cache_keys": list(self.frame_cache.keys())
        }
    
    def get_sign_path(self, sign_name: str) -> Optional[Path]:
        """Get the directory path for a sign"""
        sign_key = sign_name.lower().replace(" ", "_")
        return self.available_signs.get(sign_key)
    
    def validate_corpus(self) -> Dict:
        """
        Validate the corpus and return statistics
        
        Returns:
            Dictionary with corpus validation info
        """
        total_signs = len(self.available_signs)
        signs_with_frames = 0
        total_images = 0
        signs_info = []
        
        for sign_key, sign_path in self.available_signs.items():
            image_files = list(sign_path.glob("*.[jJ][pP][gG]")) + list(sign_path.glob("*.[pP][nN][gG]"))
            frame_count = len(image_files)
            
            if frame_count > 0:
                signs_with_frames += 1
                total_images += frame_count
                signs_info.append({
                    "sign": sign_key,
                    "frames": frame_count
                })
        
        return {
            "total_signs": total_signs,
            "signs_with_frames": signs_with_frames,
            "total_images": total_images,
            "average_frames_per_sign": total_images / max(signs_with_frames, 1),
            "mapped_telugu_words": len(self.telugu_isl_mapping),
            "signs_info": signs_info[:10]  # Return first 10 for overview
        }
