"""Tests for the ISL frame animator using a temporary corpus."""
import json
from pathlib import Path

from PIL import Image

from telugu_s2sl.animation.corpus import ISLCorpusAnimator


def _make_corpus(tmp_path: Path, sign: str = "HELLO_HI", frames: int = 3) -> tuple[Path, Path]:
    frames_dir = tmp_path / "frames"
    sign_dir = frames_dir / sign
    sign_dir.mkdir(parents=True)
    for index in range(frames):
        Image.new("RGB", (32, 32), (20 + index * 10, 30, 40)).save(sign_dir / f"{index:03d}.jpg")

    mapping_path = tmp_path / "mapping.json"
    mapping_path.write_text(
        json.dumps({"నమస్కారం": sign}, ensure_ascii=False), encoding="utf-8"
    )
    return frames_dir, mapping_path


def test_indexes_and_loads_frames(tmp_path):
    frames_dir, mapping_path = _make_corpus(tmp_path)
    animator = ISLCorpusAnimator(frames_dir=frames_dir, mapping_files=[mapping_path])

    assert animator.has_sign("HELLO_HI")
    assert animator.get_sign_frame_count("hello_hi") == 3

    frames = animator.load_sign_frames("HELLO_HI")
    assert frames is not None and len(frames) == 3
    assert animator.frame_cache


def test_sequence_for_available_sign(tmp_path):
    frames_dir, mapping_path = _make_corpus(tmp_path)
    animator = ISLCorpusAnimator(frames_dir=frames_dir, mapping_files=[mapping_path])

    sequence = animator.create_animation_sequence(["HELLO_HI"])
    assert sequence[0]["type"] == "sign"
    assert sequence[0]["available"] is True
    assert sequence[0]["frame_count"] == 3


def test_text_fallback(tmp_path):
    frames_dir, mapping_path = _make_corpus(tmp_path)
    animator = ISLCorpusAnimator(frames_dir=frames_dir, mapping_files=[mapping_path])

    sequence = animator.create_animation_sequence(["TEXT_నమస్కారం", "UNKNOWN"])
    assert [step["type"] for step in sequence] == ["text", "text"]
    assert all(step["available"] is False for step in sequence)


def test_validate_corpus(tmp_path):
    frames_dir, mapping_path = _make_corpus(tmp_path)
    animator = ISLCorpusAnimator(frames_dir=frames_dir, mapping_files=[mapping_path])
    stats = animator.validate_corpus()
    assert stats["total_signs"] == 1
    assert stats["total_images"] == 3
    assert stats["mapped_telugu_words"] == 1
