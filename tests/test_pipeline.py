"""End-to-end text -> gloss -> animation bundle tests."""
import json
from pathlib import Path

from PIL import Image

from telugu_s2sl.animation.corpus import ISLCorpusAnimator
from telugu_s2sl.pipeline import SpeechToSignPipeline


def test_pipeline_bundle(tmp_path):
    sign_dir = tmp_path / "frames" / "HELLO_HI"
    sign_dir.mkdir(parents=True)
    for index in range(2):
        Image.new("RGB", (16, 16), (10, 20, 30)).save(sign_dir / f"{index}.jpg")

    mapping_path = tmp_path / "mapping.json"
    mapping_path.write_text(
        json.dumps({"నమస్కారం": "HELLO_HI"}, ensure_ascii=False), encoding="utf-8"
    )

    animator = ISLCorpusAnimator(
        frames_dir=tmp_path / "frames", mapping_files=[mapping_path]
    )
    pipeline = SpeechToSignPipeline(animator=animator)
    bundle = pipeline.translate_text("నమస్కారం")

    assert bundle.signs[0].lower() == "hello_hi"
    assert bundle.available_steps == 1
    assert bundle.animation[0]["type"] == "sign"


def test_pipeline_fallback_bundle(tmp_path):
    empty = tmp_path / "frames"
    empty.mkdir()
    pipeline = SpeechToSignPipeline(
        animator=ISLCorpusAnimator(frames_dir=empty, mapping_files=[])
    )
    bundle = pipeline.translate_text("అజ్ఞాతపదం")

    assert bundle.missing_steps == len(bundle.animation)
    assert bundle.has_frames is False
