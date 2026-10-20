"""Optional GIF-based sign renderer and placeholder generator.

The primary runtime path uses the frame corpus in
``telugu_s2sl.animation.corpus``.  GIF animation is kept as a drop-in fallback
because the paper describes a pre-built GIF library.  Any ``.gif`` placed in
``data/gifs`` is discovered automatically.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import imageio.v2 as imageio
from PIL import Image

from ..config import COMMON_TELUGU_WORDS, PATHS, TELUGU_CONFIG


class SignAnimator:
    """Load GIF animations (or image directories) by sign name."""

    def __init__(self, gifs_dir: Path | None = None, frames_dir: Path | None = None) -> None:
        self.gifs_dir = Path(gifs_dir or PATHS.gifs)
        self.frames_dir = Path(frames_dir or PATHS.isl_frames)
        self.gif_cache: Dict[str, List[Image.Image]] = {}
        self.available_signs: Dict[str, Path] = {}
        self._scan()

    def _scan(self) -> None:
        if self.gifs_dir.exists():
            for gif_file in self.gifs_dir.rglob("*.gif"):
                self.available_signs[gif_file.stem.lower()] = gif_file
        if self.frames_dir.exists():
            for item in self.frames_dir.iterdir():
                if item.is_dir():
                    self.available_signs[item.name.lower()] = item

    def has_sign(self, sign_name: str) -> bool:
        return sign_name.lower() in self.available_signs

    def get_available_signs(self) -> List[str]:
        return sorted(self.available_signs)

    def load_gif(self, sign_name: str) -> Optional[List[Image.Image]]:
        key = sign_name.lower()
        if key in self.gif_cache:
            return self.gif_cache[key]
        if key not in self.available_signs:
            return None

        path = self.available_signs[key]
        frames: List[Image.Image] = []
        try:
            if path.is_dir():
                images = sorted(
                    list(path.glob("*.jpg"))
                    + list(path.glob("*.JPG"))
                    + list(path.glob("*.png"))
                    + list(path.glob("*.PNG"))
                )
                for image_path in images:
                    with Image.open(image_path) as opened:
                        frames.append(opened.convert("RGB").copy())
            else:
                frames = [Image.fromarray(frame) for frame in imageio.mimread(str(path))]
        except Exception as exc:
            print(f"Error loading sign {path}: {exc}")
            return None

        if frames:
            self.gif_cache[key] = frames
            return frames
        return None

    def get_gif_path(self, sign_name: str) -> Optional[Path]:
        return self.available_signs.get(sign_name.lower())

    def get_sign_for_word(self, telugu_word: str) -> Optional[str]:
        sign_name = COMMON_TELUGU_WORDS.get(telugu_word)
        if sign_name and self.has_sign(sign_name):
            return sign_name
        return None

    def get_alphabet_signs(self, word: str) -> List[str]:
        signs = []
        for char in word:
            for candidate in (f"alphabet_{char}", char):
                if self.has_sign(candidate):
                    signs.append(candidate)
                    break
        return signs

    def get_number_sign(self, number: int | str) -> Optional[str]:
        sign_name = f"number_{number}"
        return sign_name if self.has_sign(sign_name) else None

    def clear_cache(self) -> None:
        self.gif_cache.clear()


def create_placeholder_gifs() -> int:
    """Create tiny placeholder GIFs so the UI can be demoed without assets."""
    created = 0
    colors = {
        "alphabets": (100, 149, 237),
        "numbers": (144, 238, 144),
        "words": (255, 182, 193),
    }

    for category, color in colors.items():
        (PATHS.gifs / category).mkdir(parents=True, exist_ok=True)

    alphabet_path = PATHS.gifs / "alphabets"
    for char in TELUGU_CONFIG["vowels"] + TELUGU_CONFIG["consonants"]:
        path = alphabet_path / f"alphabet_{char}.gif"
        if not path.exists():
            _create_simple_gif(path, color=colors["alphabets"])
            created += 1

    number_path = PATHS.gifs / "numbers"
    for number in range(10):
        path = number_path / f"number_{number}.gif"
        if not path.exists():
            _create_simple_gif(path, color=colors["numbers"])
            created += 1

    word_path = PATHS.gifs / "words"
    for sign_name in COMMON_TELUGU_WORDS.values():
        path = word_path / f"{sign_name}.gif"
        if not path.exists():
            _create_simple_gif(path, color=colors["words"])
            created += 1

    return created


def _create_simple_gif(path: Path, color: tuple[int, int, int], size: int = 200) -> None:
    try:
        frames = []
        for index in range(3):
            brightness = 0.9 + index * 0.05
            adjusted = tuple(int(channel * brightness) for channel in color)
            frames.append(Image.new("RGB", (size, size), color=adjusted))
        frames[0].save(
            path,
            save_all=True,
            append_images=frames[1:],
            duration=300,
            loop=0,
        )
    except Exception as exc:
        print(f"Error creating GIF {path}: {exc}")


# Legacy alias used by older code and notebooks.
GifSignAnimator = SignAnimator
