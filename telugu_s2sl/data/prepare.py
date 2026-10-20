"""Build fast lookup indexes for the ISL frame corpus.

Run with::

    python app.py --mode prepare

The generated files live in ``data/mappings`` and are intentionally ignored by
git; they can always be rebuilt from the frame directory.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict

from ..config import COMMON_TELUGU_WORDS, PATHS
from ..animation.corpus import ISLCorpusAnimator

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def prepare_isl_corpus() -> bool:
    """Index frames, validate them and write the generated mapping files."""
    frames_dir = PATHS.isl_frames
    if not frames_dir.exists():
        print(f"ISL frame corpus not found: {frames_dir}")
        print("Add sign directories under data/ISL_Corpus/Frames_Word_Level/")
        return False

    animator = ISLCorpusAnimator(frames_dir=frames_dir)
    validation = animator.validate_corpus()
    if validation["total_signs"] == 0:
        print("No sign directories with images were found. Nothing to index.")
        return False

    print(
        f"Found {validation['total_signs']} signs / "
        f"{validation['total_images']:,} frames "
        f"({validation['average_frames_per_sign']:.1f} frames per sign)"
    )

    PATHS.mappings.mkdir(parents=True, exist_ok=True)

    sign_database = build_sign_database(animator, frames_dir)
    _write_json(PATHS.isl_signs, sign_database)
    print(f"Wrote {PATHS.isl_signs}")

    mappings = create_telugu_isl_mappings(animator, sign_database)
    _write_json(PATHS.isl_corpus_mapping, mappings)
    print(f"Wrote {PATHS.isl_corpus_mapping} ({len(mappings)} Telugu words)")

    index = create_lookup_index(sign_database, frames_dir)
    _write_json(PATHS.isl_index, index)
    print(f"Wrote {PATHS.isl_index}")

    return True


def build_sign_database(animator: ISLCorpusAnimator, corpus_dir: Path) -> Dict:
    database: Dict[str, Dict] = {}
    for sign_key, sign_path in animator.available_signs.items():
        image_files = set()
        for pattern in ("*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG"):
            image_files.update(sign_path.glob(pattern))
        image_files = sorted(image_files, key=lambda path: path.name)
        try:
            relative = str(sign_path.relative_to(corpus_dir))
        except ValueError:
            relative = sign_path.name

        database[sign_key] = {
            "original_name": sign_path.name,
            "directory": relative,
            "frame_count": len(image_files),
            "frames": [path.name for path in image_files],
            "status": "ready" if image_files else "empty",
        }
    return database


def create_telugu_isl_mappings(
    animator: ISLCorpusAnimator, sign_database: Dict
) -> Dict[str, str]:
    mappings = dict(animator.telugu_isl_mapping)
    for telugu_word, sign_name in COMMON_TELUGU_WORDS.items():
        normalized = sign_name.lower().replace(" ", "_")
        if normalized in sign_database:
            mappings.setdefault(telugu_word, normalized)
    return mappings


def create_lookup_index(sign_database: Dict, corpus_dir: Path) -> Dict:
    return {
        "version": "2.0",
        "total_signs": len(sign_database),
        "corpus_dir": str(corpus_dir),
        "signs": {
            key: {
                "frames": info["frame_count"],
                "path": info["directory"],
                "ready": info["status"] == "ready",
            }
            for key, info in sign_database.items()
        },
    }


def test_animation_loading() -> None:
    animator = ISLCorpusAnimator()
    for sign in ("HAPPY", "HELLO_HI", "THANK", "PLEASE", "GOOD"):
        if animator.has_sign(sign):
            frames = animator.load_sign_frames(sign)
            status = f"{len(frames)} frames" if frames else "failed to load"
        else:
            status = "not in corpus"
        print(f"  {sign:<12} {status}")


def _write_json(path: Path, data: Dict) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    if prepare_isl_corpus():
        test_animation_loading()
    else:
        raise SystemExit(1)
