"""
Sign Language Animation Module
Handles ISL GIF loading, matching, and playback
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Union
import sys
from PIL import Image
import imageio

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import DATASET_PATHS, TELUGU_CONFIG, COMMON_TELUGU_WORDS


class SignAnimator:
    """
    ISL (Indian Sign Language) Animation Handler
    
    Loads and manages GIF animations for sign language display
    """
    
    def __init__(self):
        """Initialize the sign animator"""
        self.gifs_dir = {
            "alphabets": DATASET_PATHS["gifs_alphabets"],
            "numbers": DATASET_PATHS["gifs_numbers"],
            "words": DATASET_PATHS["gifs_words"],
        }
        
        # New frame-based animations
        self.frames_dir = DATASET_PATHS.get("isl_real_frames")
        
        # Cache for loaded GIFs
        self.gif_cache: Dict[str, List[Image.Image]] = {}
        
        # Available signs (name -> Path)
        self.available_signs: Dict[str, Path] = {}
        
        # Scan for available GIFs and Frames
        self._scan_available_gifs()
    
    def _scan_available_gifs(self):
        """Scan directories for available GIF files and Frame directories"""
        # 1. Scan GIFs
        for category, dir_path in self.gifs_dir.items():
            if dir_path.exists():
                for gif_file in dir_path.glob("*.gif"):
                    sign_name = gif_file.stem.lower()
                    self.available_signs[sign_name] = gif_file
        
        # 2. Scan Frame directories
        if self.frames_dir and self.frames_dir.exists():
            for item in self.frames_dir.iterdir():
                if item.is_dir():
                    # Folder name is the sign name (e.g. "HAPPY")
                    sign_name = item.name.lower()
                    # If duplicate, real frames take precedence over GIFs
                    self.available_signs[sign_name] = item

    def get_available_signs(self) -> List[str]:
        """Get list of available sign names"""
        return list(self.available_signs.keys())
    
    def has_sign(self, sign_name: str) -> bool:
        """Check if a GIF/Sequence exists for the given sign"""
        return sign_name.lower() in self.available_signs
    
    def load_gif(self, sign_name: str) -> Optional[List[Image.Image]]:
        """
        Load GIF frames or Image Sequence for a sign
        
        Args:
            sign_name: Name of the sign
            
        Returns:
            List of PIL Image frames or None if not found
        """
        sign_name = sign_name.lower()
        
        # Check cache
        if sign_name in self.gif_cache:
            return self.gif_cache[sign_name]
        
        # Check if sign exists
        if sign_name not in self.available_signs:
            return None
        
        # Get path
        path = self.available_signs[sign_name]
        frames = []
        
        try:
            if path.is_dir():
                # Load sequence of images
                images = sorted(list(path.glob("*.[jJ][pP][gG]")) + list(path.glob("*.[pP][nN][gG]")))
                # Simple sort might fail on "1.jpg", "10.jpg" if not zero-padded, but usually acceptable
                if not images:
                    print(f"Warning: No images found in {path}")
                    return None
                    
                for img_path in images:
                    img = Image.open(img_path)
                    frames.append(img)
            else:
                # Load GIF
                gif = imageio.mimread(str(path))
                frames = [Image.fromarray(frame) for frame in gif]
            
            # Cache the frames
            if frames:
                self.gif_cache[sign_name] = frames
                return frames
            
        except Exception as e:
            print(f"Error loading sign {path}: {e}")
            
        return None
    
    def get_gif_path(self, sign_name: str) -> Optional[Path]:
        """Get the file path for a sign GIF"""
        sign_name = sign_name.lower()
        return self.available_signs.get(sign_name)
    
    def get_sign_for_word(self, telugu_word: str) -> Optional[str]:
        """
        Get the sign name for a Telugu word
        
        Args:
            telugu_word: Telugu word
            
        Returns:
            Sign name if available, None otherwise
        """
        # Check direct mapping
        if telugu_word in COMMON_TELUGU_WORDS:
            sign_name = COMMON_TELUGU_WORDS[telugu_word]
            if self.has_sign(sign_name):
                return sign_name
        
        return None
    
    def get_alphabet_signs(self, word: str) -> List[str]:
        """
        Get alphabet signs for spelling a word
        
        Args:
            word: Word to spell
            
        Returns:
            List of available alphabet sign names
        """
        signs = []
        for char in word:
            sign_name = f"alphabet_{char}"
            if self.has_sign(sign_name):
                signs.append(sign_name)
            else:
                # Try without prefix
                if self.has_sign(char):
                    signs.append(char)
        return signs
    
    def get_number_sign(self, number: Union[int, str]) -> Optional[str]:
        """Get sign name for a number"""
        sign_name = f"number_{number}"
        if self.has_sign(sign_name):
            return sign_name
        return None
    
    def create_animation_sequence(
        self, 
        translation_result: List[Dict]
    ) -> List[Dict]:
        """
        Create animation sequence from translation result
        
        Args:
            translation_result: Output from NLP translator
            
        Returns:
            List of animation items with GIF info
        """
        sequence = []
        
        for item in translation_result:
            if item["direct_match"]:
                sign_name = item["sign"]
                if self.has_sign(sign_name):
                    sequence.append({
                        "type": "gif",
                        "sign": sign_name,
                        "path": str(self.get_gif_path(sign_name)),
                        "telugu": item["telugu"]
                    })
                else:
                    # Sign not available, use text display
                    sequence.append({
                        "type": "text",
                        "sign": sign_name,
                        "path": None,
                        "telugu": item["telugu"]
                    })
            else:
                # Alphabetical spelling
                for char in item["sign"]:
                    alpha_sign = f"alphabet_{char}"
                    if self.has_sign(alpha_sign):
                        sequence.append({
                            "type": "gif",
                            "sign": alpha_sign,
                            "path": str(self.get_gif_path(alpha_sign)),
                            "telugu": char
                        })
                    else:
                        sequence.append({
                            "type": "text",
                            "sign": char,
                            "path": None,
                            "telugu": char
                        })
        
        return sequence
    
    def clear_cache(self):
        """Clear the GIF cache"""
        self.gif_cache.clear()
    
    def get_cache_info(self) -> Dict:
        """Get cache statistics"""
        return {
            "cached_signs": len(self.gif_cache),
            "available_signs": len(self.available_signs),
            "cache_keys": list(self.gif_cache.keys())
        }


def create_placeholder_gifs():
    """
    Create placeholder GIF files for testing
    This creates simple colored frames as placeholders
    """
    import numpy as np
    
    animator = SignAnimator()
    
    # Create directories
    for dir_path in animator.gifs_dir.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Colors for different categories
    colors = {
        "alphabets": (100, 149, 237),  # Cornflower blue
        "numbers": (144, 238, 144),     # Light green
        "words": (255, 182, 193),       # Light pink
    }
    
    # Create alphabet GIFs for Telugu consonants and vowels
    alphabets = TELUGU_CONFIG["vowels"] + TELUGU_CONFIG["consonants"]
    for char in alphabets:
        gif_path = animator.gifs_dir["alphabets"] / f"alphabet_{char}.gif"
        if not gif_path.exists():
            _create_simple_gif(gif_path, char, colors["alphabets"])
    
    # Create number GIFs
    for i in range(10):
        gif_path = animator.gifs_dir["numbers"] / f"number_{i}.gif"
        if not gif_path.exists():
            _create_simple_gif(gif_path, str(i), colors["numbers"])
    
    # Create word GIFs
    for telugu_word, sign_name in COMMON_TELUGU_WORDS.items():
        gif_path = animator.gifs_dir["words"] / f"{sign_name}.gif"
        if not gif_path.exists():
            _create_simple_gif(gif_path, telugu_word[:4], colors["words"])
    
    print(f"Created placeholder GIFs in {DATASET_PATHS['gifs_alphabets'].parent}")


def _create_simple_gif(path: Path, text: str, color: tuple, size: int = 200):
    """Create a simple placeholder GIF with text"""
    try:
        frames = []
        
        for i in range(3):  # 3 frames
            # Create colored background
            img = Image.new('RGB', (size, size), color=color)
            
            # Add subtle variation for animation effect
            brightness = 0.9 + (i * 0.05)
            adjusted_color = tuple(int(c * brightness) for c in color)
            img = Image.new('RGB', (size, size), color=adjusted_color)
            
            frames.append(img)
        
        # Save as GIF
        frames[0].save(
            path,
            save_all=True,
            append_images=frames[1:],
            duration=300,
            loop=0
        )
        
    except Exception as e:
        print(f"Error creating GIF {path}: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("Sign Animator Test")
    print("=" * 60)
    
    animator = SignAnimator()
    
    print(f"\nGIF Directories:")
    for category, path in animator.gifs_dir.items():
        exists = "✅" if path.exists() else "❌"
        print(f"  {category}: {path} {exists}")
    
    print(f"\nAvailable Signs: {len(animator.available_signs)}")
    if animator.available_signs:
        print(f"  Sample signs: {list(animator.available_signs.keys())[:5]}")
    
    # Create placeholders if no GIFs exist
    if len(animator.available_signs) == 0:
        print("\n📁 No GIFs found. Creating placeholder GIFs...")
        create_placeholder_gifs()
        
        # Rescan
        animator._scan_available_gifs()
        print(f"✅ Created {len(animator.available_signs)} placeholder GIFs")
    
    print("\n✅ Sign Animator Module Loaded Successfully!")
