"""
Enhanced ISL Corpus Animator with complete 114-sign support
All ISL signs with proper frame loading and caching
"""
import json
from pathlib import Path
from typing import List, Dict, Optional
import sys
from PIL import Image
import os

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import DATASET_PATHS


class EnhancedISLCorpusAnimator:
    """
    Complete ISL Corpus animator supporting all 114 signs
    Robust frame loading with proper caching and image handling
    """
    
    def __init__(self):
        """Initialize the enhanced animator"""
        self.corpus_frames_dir = Path(DATASET_PATHS.get("isl_corpus_frames", 
                                      r"c:\Users\iamav\Desktop\Claude Capstone\telugu_speech_to_sign\datasets\ISL_Corpus\Frames_Word_Level"))
        
        # Comprehensive mapping with all 214 Telugu words
        self.telugu_isl_mapping = self._load_comprehensive_mapping()
        
        # All available signs from corpus
        self.available_signs: Dict[str, Path] = {}
        self.sign_frame_counts: Dict[str, int] = {}
        
        # Multi-level frame cache (more aggressive caching)
        self.frame_cache: Dict[str, List[Image.Image]] = {}
        self.frame_info_cache: Dict[str, List[Dict]] = {}
        
        # Initialize
        self._scan_available_signs()
        self._build_frame_index()
    
    def _load_comprehensive_mapping(self) -> Dict[str, str]:
        """Load the comprehensive Telugu to ISL mapping"""
        mapping_file = Path(r"c:\Users\iamav\Desktop\Claude Capstone\telugu_speech_to_sign\telugu_to_isl_corpus_complete.json")
        
        if mapping_file.exists():
            try:
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load comprehensive mapping: {e}")
        
        # Fallback to original mapping
        try:
            mapping_file = DATASET_PATHS.get("isl_corpus_mapping")
            if mapping_file and Path(mapping_file).exists():
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        
        return {}
    
    def _scan_available_signs(self):
        """Scan and index all 114 signs from ISL_Corpus"""
        if not self.corpus_frames_dir.exists():
            print(f"Warning: ISL_Corpus directory not found: {self.corpus_frames_dir}")
            return
        
        try:
            for item in sorted(self.corpus_frames_dir.iterdir()):
                if item.is_dir():
                    # Get all image files
                    images = list(item.glob("*.jpg")) + list(item.glob("*.JPG")) + \
                             list(item.glob("*.jpeg")) + list(item.glob("*.JPEG")) + \
                             list(item.glob("*.png")) + list(item.glob("*.PNG"))
                    
                    if images:  # Only add if has frames
                        sign_name = item.name
                        sign_key = self._normalize_sign_name(sign_name)
                        self.available_signs[sign_key] = item
                        self.sign_frame_counts[sign_key] = len(images)
        except Exception as e:
            print(f"Error scanning ISL_Corpus: {e}")
    
    def _normalize_sign_name(self, name: str) -> str:
        """Normalize sign folder name to lowercase with underscores"""
        return name.lower().replace(" ", "_").replace("-", "_")
    
    def _build_frame_index(self):
        """Pre-index all sign frames for faster access"""
        print(f"Indexing {len(self.available_signs)} ISL signs...")
        for sign_key in self.available_signs:
            self._preload_frame_info(sign_key)
    
    def _preload_frame_info(self, sign_key: str):
        """Pre-load frame information for a sign without loading full images"""
        if sign_key in self.frame_info_cache:
            return
        
        sign_path = self.available_signs.get(sign_key)
        if not sign_path:
            return
        
        try:
            frame_files = sorted(
                list(sign_path.glob("*.jpg")) + list(sign_path.glob("*.JPG")) +
                list(sign_path.glob("*.jpeg")) + list(sign_path.glob("*.JPEG")) +
                list(sign_path.glob("*.png")) + list(sign_path.glob("*.PNG")),
                key=lambda p: self._extract_frame_number(p.name)
            )
            
            frame_info = []
            for frame_file in frame_files:
                frame_info.append({
                    "path": str(frame_file),
                    "filename": frame_file.name,
                    "index": len(frame_info)
                })
            
            self.frame_info_cache[sign_key] = frame_info
        except Exception as e:
            print(f"Error preloading frame info for {sign_key}: {e}")
    
    def _extract_frame_number(self, filename: str) -> tuple:
        """Extract numeric frame number from filename for proper sorting"""
        import re
        numbers = re.findall(r'\d+', filename)
        if numbers:
            return (0, int(numbers[0]))  # Primary numeric sort
        return (1, filename)  # Fallback to alphabetic
    
    def load_sign_frames(self, sign_name: str) -> Optional[List[Image.Image]]:
        """
        Load all frames for a sign with robust error handling
        
        Args:
            sign_name: Name of the sign (e.g., "HELLO_HI", "YOU")
            
        Returns:
            List of PIL Image.Image objects or None if not found
        """
        sign_key = self._normalize_sign_name(sign_name)
        
        # Check cache first
        if sign_key in self.frame_cache:
            return self.frame_cache[sign_key]
        
        # Check if sign exists
        if sign_key not in self.available_signs:
            return None
        
        sign_path = self.available_signs[sign_key]
        frames = []
        
        try:
            # Get frames in correct order
            frame_files = sorted(
                list(sign_path.glob("*.jpg")) + list(sign_path.glob("*.JPG")) +
                list(sign_path.glob("*.jpeg")) + list(sign_path.glob("*.JPEG")) +
                list(sign_path.glob("*.png")) + list(sign_path.glob("*.PNG")),
                key=lambda p: self._extract_frame_number(p.name)
            )
            
            if not frame_files:
                return None
            
            # Load each frame
            for frame_file in frame_files:
                try:
                    img = Image.open(frame_file)
                    # Ensure RGB for consistency
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    # Resize to standard size for consistency
                    img = img.resize((400, 400), Image.Resampling.LANCZOS)
                    frames.append(img)
                except Exception as e:
                    pass  # Skip problematic frames
            
            if frames:
                self.frame_cache[sign_key] = frames
                return frames
        
        except Exception as e:
            print(f"Error loading frames for {sign_key}: {e}")
        
        return None
    
    def get_sign_for_telugu_word(self, telugu_word: str) -> Optional[str]:
        """
        Get ISL sign for a Telugu word
        
        Args:
            telugu_word: Telugu word text
            
        Returns:
            Sign name or None if not found
        """
        # Direct lookup
        if telugu_word in self.telugu_isl_mapping:
            sign_name = self.telugu_isl_mapping[telugu_word]
            if self._normalize_sign_name(sign_name) in self.available_signs:
                return sign_name
        
        # Case-insensitive lookup
        telugu_lower = telugu_word.lower()
        for mapped_word, sign_name in self.telugu_isl_mapping.items():
            if mapped_word.lower() == telugu_lower:
                if self._normalize_sign_name(sign_name) in self.available_signs:
                    return sign_name
        
        return None
    
    def create_animation_sequence(self, items: List[str]) -> List[Dict]:
        """
        Create animation sequence from sign names or Telugu words
        
        Args:
            items: List of sign names (from translator) or Telugu words
            
        Returns:
            List of animation frames with metadata
        """
        sequence = []
        
        for item in items:
            # Skip TEXT_* items (these are handled separately by translator)
            if isinstance(item, str) and item.startswith("TEXT_"):
                # Extract Telugu text from TEXT_ prefix
                telugu_text = item[5:]  # Remove "TEXT_" prefix
                sequence.append({
                    "type": "text",
                    "telugu": telugu_text,
                    "available": False,
                    "message": telugu_text
                })
                continue
            
            # First, check if this is already a direct sign name
            sign_key = self._normalize_sign_name(item)
            if sign_key in self.available_signs:
                # It's a direct sign name from the translator
                frames = self.load_sign_frames(item)
                if frames:
                    sequence.append({
                        "type": "sign",
                        "telugu": item,
                        "isl_sign": item,
                        "sign_key": sign_key,
                        "frames": frames,
                        "frame_count": len(frames),
                        "available": True
                    })
                else:
                    sequence.append({
                        "type": "text",
                        "telugu": item,
                        "isl_sign": item,
                        "available": False,
                        "message": f"No frames for {item}"
                    })
            else:
                # Try to find a sign for this Telugu word
                sign_name = self.get_sign_for_telugu_word(item)
                
                if sign_name:
                    frames = self.load_sign_frames(sign_name)
                    if frames:
                        sequence.append({
                            "type": "sign",
                            "telugu": item,
                            "isl_sign": sign_name,
                            "sign_key": self._normalize_sign_name(sign_name),
                            "frames": frames,
                            "frame_count": len(frames),
                            "available": True
                        })
                    else:
                        sequence.append({
                            "type": "text",
                            "telugu": item,
                            "isl_sign": sign_name,
                            "available": False,
                            "message": f"No frames for {sign_name}"
                        })
                else:
                    sequence.append({
                        "type": "text",
                        "telugu": item,
                        "available": False,
                        "message": f"No ISL sign for '{item}'"
                    })
        
        return sequence
    
    def get_available_signs(self) -> List[str]:
        """Get all available sign names"""
        return sorted(list(self.available_signs.keys()))
    
    def get_stats(self) -> Dict:
        """Get comprehensive statistics"""
        total_frames = sum(self.sign_frame_counts.values())
        return {
            "total_signs": len(self.available_signs),
            "total_frames": total_frames,
            "average_frames_per_sign": total_frames / max(len(self.available_signs), 1),
            "mapped_telugu_words": len(self.telugu_isl_mapping),
            "cached_signs": len(self.frame_cache),
            "cached_frames": sum(len(frames) for frames in self.frame_cache.values())
        }
    
    def clear_cache(self):
        """Clear frame cache to free memory"""
        self.frame_cache.clear()
    
    def get_sign_frame_count(self, sign_name: str) -> int:
        """Get number of frames for a sign"""
        sign_key = self._normalize_sign_name(sign_name)
        return self.sign_frame_counts.get(sign_key, 0)
    
    def list_all_signs_with_frames(self) -> List[Dict]:
        """Get all signs with frame counts"""
        signs_list = []
        for sign_key in sorted(self.available_signs.keys()):
            frame_count = self.sign_frame_counts.get(sign_key, 0)
            signs_list.append({
                "sign": sign_key,
                "frames": frame_count,
                "path": str(self.available_signs[sign_key])
            })
        return signs_list


# For backward compatibility
ISLCorpusAnimator = EnhancedISLCorpusAnimator
