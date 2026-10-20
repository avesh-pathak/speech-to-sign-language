"""Telugu Speech → Indian Sign Language.

Usage
-----
    python app.py                         # desktop GUI
    python app.py --translate "నమస్కారం"  # text -> ISL gloss
    python app.py --audio path/to.wav      # speech -> ISL gloss
    python app.py --mode prepare           # index the ISL frame corpus
    python app.py --mode train             # train Res-BiLSTM-AM
    python app.py --mode classify --audio path/to.wav
    python app.py --mode info              # corpus / mapping summary
    python app.py --mode test              # pytest
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from telugu_s2sl.config import ensure_directories


def _print_translation(text: str) -> None:
    from telugu_s2sl.pipeline import SpeechToSignPipeline

    bundle = SpeechToSignPipeline().translate_text(text)

    print("\n" + "=" * 60)
    print("Telugu → ISL")
    print("=" * 60)
    print(f"Input: {text}\n")
    for item in bundle.tokens:
        marker = "✓ direct" if item.get("direct_match") else "· fallback"
        print(f"  {item['telugu']:<20} → {item['sign']:<20} [{marker}]")
    print(f"\nGloss: {' → '.join(bundle.signs)}")
    print(
        f"Animation: {bundle.available_steps} ready, "
        f"{bundle.missing_steps} text fallback(s)\n"
    )


def _print_audio(path: str) -> None:
    from telugu_s2sl.pipeline import SpeechToSignPipeline

    pipeline = SpeechToSignPipeline()
    print(f"Transcribing {path}…")
    bundle = pipeline.translate_audio_file(path)
    print(f"Recognised: {bundle.source_text}\n")
    print(f"Gloss: {' → '.join(bundle.signs)}")
    print(
        f"Animation: {bundle.available_steps} ready, "
        f"{bundle.missing_steps} text fallback(s)\n"
    )


def _print_info() -> None:
    from telugu_s2sl.pipeline import SpeechToSignPipeline

    info = SpeechToSignPipeline().describe()
    print("\n" + "=" * 60)
    print("Telugu Speech-to-Sign — runtime summary")
    print("=" * 60)
    for key, value in info.items():
        print(f"  {key:<14} {value}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Telugu speech-to-Indian-Sign-Language framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--mode",
        choices=["gui", "translate", "audio", "prepare", "train", "classify", "info", "test"],
        default="gui",
    )
    parser.add_argument("--translate", metavar="TELUGU_TEXT")
    parser.add_argument("--audio", metavar="PATH")
    args = parser.parse_args()

    ensure_directories()

    if args.translate:
        _print_translation(args.translate)
        return

    if args.mode == "translate":
        _print_translation(args.audio or input("Telugu text: ").strip())
        return

    if args.mode == "audio" or args.audio:
        if not args.audio:
            parser.error("--mode audio requires --audio PATH")
        _print_audio(args.audio)
        return

    if args.mode == "info":
        _print_info()
        return

    if args.mode == "prepare":
        from telugu_s2sl.data.prepare import prepare_isl_corpus, test_animation_loading

        if not prepare_isl_corpus():
            raise SystemExit(1)
        test_animation_loading()
        return

    if args.mode == "train":
        from telugu_s2sl.training.train import main as train_main

        train_main()
        return

    if args.mode == "classify":
        if not args.audio:
            parser.error("--mode classify requires --audio PATH")
        from telugu_s2sl.model.inference import SignClassifier

        result = SignClassifier().predict_audio(args.audio)
        print(f"\nPredicted sign: {result['predicted_name']} ({result['confidence']:.1%})")
        for item in result["top_predictions"]:
            print(f"  {item['name']:<24} {item['confidence']:.3f}")
        return

    if args.mode == "test":
        import subprocess

        raise SystemExit(
            subprocess.call([sys.executable, "-m", "pytest", "tests", "-v"], cwd=PROJECT_ROOT)
        )

    from telugu_s2sl.gui.app import main as gui_main

    gui_main()


if __name__ == "__main__":
    main()
