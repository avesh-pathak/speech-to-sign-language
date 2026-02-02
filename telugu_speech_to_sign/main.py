"""
Telugu Speech-to-Sign Language Translation System
Main Entry Point
"""
import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def should_prepare_data() -> bool:
    """
    Check if data preparation is needed
    Returns True if mappings or index files are missing or outdated
    """
    from config.config import DATASET_PATHS
    
    required_files = [
        DATASET_PATHS["mappings"] / "isl_corpus_signs.json",
        DATASET_PATHS["mappings"] / "isl_corpus_index.json",
        DATASET_PATHS["mappings"] / "telugu_to_isl_corpus.json",
    ]
    
    for file in required_files:
        if not file.exists():
            print(f"  ℹ Missing: {file.name}")
            return True
    
    return False


def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(
        description="Telugu Speech-to-Sign Language Translation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Launch GUI application
  python main.py --mode gui               # Launch GUI application
  python main.py --mode prepare           # Prepare ISL_CORPUS data
  python main.py --mode train             # Train the model
  python main.py --mode test              # Run tests
  python main.py --translate "నమస్కారం"  # Translate text directly
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['gui', 'prepare', 'train', 'train-corpus', 'test', 'cli'],
        default='gui',
        help='Application mode (default: gui)'
    )
    
    parser.add_argument(
        '--translate',
        type=str,
        help='Translate Telugu text directly (CLI mode)'
    )
    
    parser.add_argument(
        '--audio',
        type=str,
        help='Path to audio file to translate'
    )
    
    parser.add_argument(
        '--create-gifs',
        action='store_true',
        help='Create placeholder GIF files'
    )
    
    parser.add_argument(
        '--validate-corpus',
        action='store_true',
        help='Validate ISL Corpus structure and mappings'
    )
    
    args = parser.parse_args()
    
    # Prepare ISL Corpus data if requested or before GUI
    if args.mode == 'prepare' or (args.mode == 'gui' and should_prepare_data()):
        print("\n🎬 Preparing ISL Corpus data...")
        try:
            from prepare_data import prepare_isl_corpus, test_animation_loading
            if prepare_isl_corpus():
                test_animation_loading()
                if args.mode == 'prepare':
                    print("\n✅ Data preparation complete!")
                    return
            else:
                print("\n❌ Data preparation failed!")
                return
        except Exception as e:
            print(f"❌ Error during preparation: {e}")
            import traceback
            traceback.print_exc()
            return
    
    # Validate corpus if requested
    if args.validate_corpus:
        print("Validating ISL Corpus...")
        # from train_isl_corpus import ISLCorpusTrainer 
        # Feature moved to archive/train_isl_corpus.py
        print("Feature archived. Please run: python archive/train_isl_corpus.py --validate")
        return
    
    # Create placeholder GIFs if requested
    if args.create_gifs:
        from modules.sign_animator import create_placeholder_gifs
        print("Creating placeholder GIFs...")
        create_placeholder_gifs()
        print("Done!")
        return
    
    # Direct translation mode
    if args.translate:
        from modules.nlp_translator import TeluguNLPTranslator
        
        translator = TeluguNLPTranslator()
        result = translator.translate(args.translate)
        
        print("\n" + "=" * 50)
        print("Telugu → ISL Translation")
        print("=" * 50)
        print(f"\nInput: {args.translate}")
        print("\nTranslation:")
        for item in result:
            match = "✓" if item['direct_match'] else "✗"
            sign = item['sign'] if isinstance(item['sign'], str) else ' '.join(item['sign'])
            print(f"  {item['telugu']} → {sign} [{match}]")
        
        signs = translator.get_sign_sequence(args.translate)
        print(f"\nSign Sequence: {' → '.join(signs)}")
        return
    
    # Audio file translation
    if args.audio:
        from modules.asr_module import TeluguASR
        from modules.nlp_translator import TeluguNLPTranslator
        
        print(f"\nProcessing audio: {args.audio}")
        
        asr = TeluguASR()
        text = asr.recognize_from_file(args.audio)
        
        print(f"Recognized: {text}")
        
        translator = TeluguNLPTranslator()
        result = translator.translate(text)
        
        print("\nTranslation:")
        for item in result:
            match = "✓" if item['direct_match'] else "✗"
            sign = item['sign'] if isinstance(item['sign'], str) else ' '.join(item['sign'])
            print(f"  {item['telugu']} → {sign} [{match}]")
        return
    
    # Mode-based execution
    if args.mode == 'gui':
        print("\n" + "=" * 60)
        print("Telugu Speech-to-Sign Language Translator")
        print("తెలుగు సంకేత భాష అనువాదకుడు")
        print("=" * 60)
        print("\nLaunching GUI application...")
        
        from gui.app import main as gui_main
        gui_main()
    
    elif args.mode == 'train':
        print("\nStarting model training...")
        from train import main as train_main
        train_main()
    
    elif args.mode == 'train-corpus':
        print("\nTraining ISL Corpus...")
        from train_isl_corpus import ISLCorpusTrainer
        trainer = ISLCorpusTrainer()
        trainer.validate_corpus()
        trainer.validate_mappings()
        trainer.get_corpus_stats()
        trainer.generate_recommendations()
    
    elif args.mode == 'test':
        print("\nRunning tests...")
        import subprocess
        subprocess.run([sys.executable, '-m', 'pytest', 'tests/', '-v'])
    
    elif args.mode == 'cli':
        print("\n" + "=" * 60)
        print("Telugu Speech-to-Sign CLI Mode")
        print("=" * 60)
        print("Type Telugu text and press Enter to translate.")
        print("Type 'exit' or 'quit' to exit.\n")
        
        from modules.nlp_translator import TeluguNLPTranslator
        translator = TeluguNLPTranslator()
        
        while True:
            try:
                text = input("తెలుగు> ").strip()
                
                if text.lower() in ['exit', 'quit', 'q']:
                    print("Goodbye! వీడ్కోలు!")
                    break
                
                if not text:
                    continue
                
                result = translator.translate(text)
                signs = translator.get_sign_sequence(text)
                
                print(f"ISL: {' → '.join(signs)}\n")
                
            except KeyboardInterrupt:
                print("\nGoodbye! వీడ్కోలు!")
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
