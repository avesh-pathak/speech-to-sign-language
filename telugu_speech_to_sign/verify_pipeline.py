import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, r"c:\Users\iamav\Desktop\Claude Capstone\telugu_speech_to_sign")

from modules.nlp_translator import TeluguNLPTranslator
from modules.isl_corpus_animator_enhanced import EnhancedISLCorpusAnimator

def test_pipeline():
    output_lines = []
    def log(msg):
        print(msg)
        output_lines.append(str(msg))

    log("=" * 60)
    log("TESTING TRANSLATION PIPELINE (TERMINAL VERIFICATION)")
    log("=" * 60)
    
    # 1. Initialize Modules
    log("\n1. Initializing Modules...")
    translator = TeluguNLPTranslator()
    animator = EnhancedISLCorpusAnimator()
    
    # 2. Verify Mappings Load
    log(f"  [Translator] Word Mappings: {len(translator.word_mapping)}")
    log(f"  [Animator]   Mapped Words:  {len(animator.telugu_isl_mapping)}")
    log(f"  [Animator]   Available Signs: {len(animator.available_signs)}")

    # 3. Test Cases (Trained/Mapped Words)
    test_cases = [
        "నమస్కారం",      # Hello (Direct)
        "ధన్యవాదాలు",     # Thank you (Direct)
        "ఆనందం",         # Happiness (Bridge -> HAPPY)
        "వైద్యుడు",       # Doctor (Bridge -> DOCTOR/DO?)
        "కళాశాల",        # College (Bridge -> COLLEGE)
        "నేను పాఠశాల వెళ్తున్నాను"  # Sentence
    ]

    log("\n2. Running Translations...")
    for text in test_cases:
        log(f"\n--- Input: '{text}' ---")
        
        # Step A: NLP Translation
        translation_result = translator.translate(text)
        log("  [NLP Output]:")
        for item in translation_result:
            match_type = "✓ Direct" if item.get('direct_match') else "✗ No Match"
            if item.get('type') == 'english_bridge':
                match_type = f"⚡ Bridge ({item['english']})"
            log(f"    - {item['telugu']} -> {item['sign']} [{match_type}]")

        # Step B: Animation Sequence Generation
        # Get sign names from translation
        sign_names = [item['sign'] for item in translation_result]
        
        # Create sequence
        sequence = animator.create_animation_sequence(sign_names)
        
        log("  [Animation Sequence]:")
        for step in sequence:
            status = "AVAILABLE" if step['available'] else "MISSING"
            kind = step['type']
            content = step.get('isl_sign', step.get('telugu', 'Unknown'))
            log(f"    - [{kind.upper()}] {content} -> {status}")

    # Write to file
    with open("pipeline_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    print("\nReport written to pipeline_report.txt")

if __name__ == "__main__":
    test_pipeline()
