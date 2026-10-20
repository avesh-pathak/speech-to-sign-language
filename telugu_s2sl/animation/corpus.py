"""ISL frame-corpus animator.

A sign is one directory of ordered frames::

    data/ISL_Corpus/Frames_Word_Level/HELLO_HI/001.jpg
    data/ISL_Corpus/Frames_Word_Level/HELLO_HI/002.jpg
    ...

The animator indexes directories once, loads frames lazily, and caches them as
Pillow images.  Missing signs degrade to a text card rather than raising.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from PIL import Image

from ..config import GUI_CONFIG, PATHS

_IMAGE_PATTERNS = ("*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG")


class ISLCorpusAnimator:
    """Frame-based ISL playback backed by the on-disk corpus."""

    def __init__(
        self,
        frames_dir: Path | None = None,
        mapping_files: Sequence[Path] | None = None,
        frame_size: tuple[int, int] | None = None,
    ) -> None:
        self.frames_dir = Path(frames_dir or PATHS.isl_frames)
        self.frame_size = frame_size or GUI_CONFIG["display_size"]
        self.mapping_files = list(
            mapping_files or (PATHS.telugu_to_isl, PATHS.isl_corpus_mapping)
        )

        self.telugu_isl_mapping: Dict[str, str] = self._load_mapping()
        self.available_signs: Dict[str, Path] = {}
        self.sign_frame_counts: Dict[str, int] = {}
        self.frame_cache: Dict[str, List[Image.Image]] = {}

        self._scan_available_signs()

    # ------------------------------------------------------------------ load
    def _load_mapping(self) -> Dict[str, str]:
        merged: Dict[str, str] = {}
        for path in self.mapping_files:
            path = Path(path)
            if not path.exists():
                continue
            try:
                with open(path, "r", encoding="utf-8") as handle:
                    data = json.load(handle)
                if isinstance(data, dict):
                    merged.update(data)
            except Exception as exc:
                print(f"Warning: could not load mapping {path.name}: {exc}")
        return merged

    def _scan_available_signs(self) -> None:
        if not self.frames_dir.exists():
            print(f"Note: ISL frame corpus not found at {self.frames_dir}")
            return

        for item in sorted(self.frames_dir.iterdir()):
            if not item.is_dir():
                continue
            files = set()
            for pattern in _IMAGE_PATTERNS:
                files.update(item.glob(pattern))
            count = len(files)
            if count:
                key = self._normalize(item.name)
                self.available_signs[key] = item
                self.sign_frame_counts[key] = count

        if self.available_signs:
            total = sum(self.sign_frame_counts.values())
            print(
                f"Indexed {len(self.available_signs)} ISL signs "
                f"({total:,} frames) from {self.frames_dir}"
            )

    @staticmethod
    def _normalize(name: str) -> str:
        return name.lower().replace(" ", "_").replace("-", "_")

    @staticmethod
    def _frame_number(filename: str) -> tuple:
        numbers = re.findall(r"\d+", filename)
        return (0, int(numbers[0])) if numbers else (1, filename)

    # ------------------------------------------------------------------ query
    def has_sign(self, sign_name: str) -> bool:
        return self._normalize(sign_name) in self.available_signs

    def get_available_signs(self) -> List[str]:
        return sorted(self.available_signs)

    def get_sign_frame_count(self, sign_name: str) -> int:
        return self.sign_frame_counts.get(self._normalize(sign_name), 0)

    def get_sign_for_telugu_word(self, telugu_word: str) -> Optional[str]:
        if telugu_word in self.telugu_isl_mapping:
            sign_name = self.telugu_isl_mapping[telugu_word]
            if self.has_sign(sign_name):
                return sign_name

        lower = telugu_word.lower()
        for word, sign_name in self.telugu_isl_mapping.items():
            if word.lower() == lower and self.has_sign(sign_name):
                return sign_name
        return None

    # ------------------------------------------------------------------ frames
    def load_sign_frames(self, sign_name: str) -> Optional[List[Image.Image]]:
        key = self._normalize(sign_name)
        if key in self.frame_cache:
            return self.frame_cache[key]
        if key not in self.available_signs:
            return None

        sign_dir = self.available_signs[key]
        files = []
        for pattern in _IMAGE_PATTERNS:
            files.extend(sign_dir.glob(pattern))
        files = sorted(set(files), key=lambda path: self._frame_number(path.name))

        frames: List[Image.Image] = []
        for frame_path in files:
            try:
                with Image.open(frame_path) as opened:
                    image = opened.convert("RGB")
                    if image.size != self.frame_size:
                        image = image.resize(self.frame_size, Image.Resampling.LANCZOS)
                    frames.append(image.copy())
            except Exception:
                continue

        if frames:
            self.frame_cache[key] = frames
            return frames
        return None

    def clear_cache(self) -> None:
        self.frame_cache.clear()

    # --------------------------------------------------------------- sequence
    def create_animation_sequence(self, items: List[str]) -> List[Dict]:
        """Turn gloss names (or ``TEXT_`` markers) into playback records."""
        sequence: List[Dict] = []

        for item in items:
            if isinstance(item, str) and item.startswith("TEXT_"):
                text = item[5:]
                sequence.append(
                    {"type": "text", "telugu": text, "available": False, "message": text}
                )
                continue

            if self.has_sign(item):
                frames = self.load_sign_frames(item)
                if frames:
                    sequence.append(
                        {
                            "type": "sign",
                            "telugu": item,
                            "isl_sign": item,
                            "sign_key": self._normalize(item),
                            "frames": frames,
                            "frame_count": len(frames),
                            "available": True,
                        }
                    )
                    continue

            sign_name = self.get_sign_for_telugu_word(item)
            if sign_name:
                frames = self.load_sign_frames(sign_name)
                if frames:
                    sequence.append(
                        {
                            "type": "sign",
                            "telugu": item,
                            "isl_sign": sign_name,
                            "sign_key": self._normalize(sign_name),
                            "frames": frames,
                            "frame_count": len(frames),
                            "available": True,
                        }
                    )
                    continue
                sequence.append(
                    {
                        "type": "text",
                        "telugu": item,
                        "isl_sign": sign_name,
                        "available": False,
                        "message": f"No frames for {sign_name}",
                    }
                )
                continue

            sequence.append(
                {
                    "type": "text",
                    "telugu": item,
                    "available": False,
                    "message": item,
                }
            )

        return sequence

    # ------------------------------------------------------------------- stats
    def validate_corpus(self) -> Dict:
        signs_with_frames = sum(1 for count in self.sign_frame_counts.values() if count)
        total_images = sum(self.sign_frame_counts.values())
        return {
            "total_signs": len(self.available_signs),
            "signs_with_frames": signs_with_frames,
            "total_images": total_images,
            "average_frames_per_sign": total_images / max(signs_with_frames, 1),
            "mapped_telugu_words": len(self.telugu_isl_mapping),
        }

    def get_stats(self) -> Dict:
        stats = self.validate_corpus()
        stats.update(
            {
                "cached_signs": len(self.frame_cache),
                "cached_frames": sum(len(frames) for frames in self.frame_cache.values()),
            }
        )
        return stats

    def list_all_signs_with_frames(self) -> List[Dict]:
        return [
            {
                "sign": key,
                "frames": self.sign_frame_counts[key],
                "path": str(self.available_signs[key]),
            }
            for key in sorted(self.available_signs)
        ]
