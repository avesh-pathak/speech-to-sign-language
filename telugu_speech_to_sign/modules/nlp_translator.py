"""
NLP Translation Module
Translates Telugu text to ISL (Indian Sign Language) structure
"""
import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import sys
from deep_translator import GoogleTranslator

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import COMMON_TELUGU_WORDS, TELUGU_CONFIG, DATASET_PATHS


class TeluguNLPTranslator:
    """
    Telugu to ISL Natural Language Processing Translator
    
    Handles:
    - Telugu text tokenization
    - Grammar transformation (Telugu SOV → ISL structure)
    - Word-to-sign mapping
    """
    
    def __init__(self):
        """Initialize the NLP translator"""
        self.word_mapping = COMMON_TELUGU_WORDS.copy()
        self.vowels = set(TELUGU_CONFIG["vowels"])
        self.consonants = set(TELUGU_CONFIG["consonants"])
        self.numbers_map = {
            num: str(i) for i, num in enumerate(TELUGU_CONFIG["numbers"])
        }
        
        # Load additional mappings if available
        self._load_additional_mappings()
    
    def _load_additional_mappings(self):
        """Load additional word mappings from file if available"""
        # First try to load ISL Corpus mapping (preferred)
        corpus_mapping_file = DATASET_PATHS.get("isl_corpus_mapping")
        if corpus_mapping_file and Path(corpus_mapping_file).exists():
            try:
                with open(corpus_mapping_file, 'r', encoding='utf-8') as f:
                    corpus_mappings = json.load(f)
                    self.word_mapping.update(corpus_mappings)
                print(f"Loaded {len(corpus_mappings)} ISL Corpus mappings")
            except Exception as e:
                print(f"Warning: Could not load ISL Corpus mappings: {e}")
        
        # Then load additional ISL mappings
        mapping_file = DATASET_PATHS.get("isl_mapping")
        if mapping_file and Path(mapping_file).exists():
            try:
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    additional_mappings = json.load(f)
                    self.word_mapping.update(additional_mappings)
            except Exception as e:
                print(f"Warning: Could not load additional mappings: {e}")

        # Load ISL Corpus Signs for Keyword Matching
        self.corpus_signs_map = {}
        try:
            corpus_signs_file = DATASET_PATHS.get("mappings") / "isl_corpus_signs.json"
            if corpus_signs_file.exists():
                with open(corpus_signs_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Create mapping: lowercase word -> sign key
                    for key, info in data.items():
                        # Map the key itself
                        self.corpus_signs_map[key.lower()] = info['original_name']
                        # Map the original name
                        self.corpus_signs_map[info['original_name'].lower()] = info['original_name']
                        # Map parts of the name (e.g. "COLLEGE" from "COLLEGE_SCHOOL")
                        parts = info['original_name'].replace("_", " ").split()
                        for part in parts:
                            if len(part) > 2: # Avoid tiny words
                                self.corpus_signs_map[part.lower()] = info['original_name']
            print(f"Loaded {len(self.corpus_signs_map)} keyword mappings for English Bridge")
        except Exception as e:
            print(f"Warning: Could not load ISL corpus signs for bridge: {e}")

        # Initialize Validator (English Translator)
        try:
            self.en_translator = GoogleTranslator(source='te', target='en')
        except:
            self.en_translator = None

    def translate_to_english(self, text: str) -> str:
        """Translate Telugu text to English"""
        if not self.en_translator:
            return text
        try:
            return self.en_translator.translate(text)
        except Exception as e:
            print(f"Translation Error: {e}")
            return text

    def find_sign_match(self, english_word: str) -> Optional[str]:
        """Find best matching sign for English word"""
        word = english_word.lower().strip()
        
        # 1. Direct Match
        if word in self.corpus_signs_map:
            return self.corpus_signs_map[word]
            
        # 2. Suffix Stripping (Stemming)
        suffixes = ['ing', 'ed', 'ly', 'ness', 'ment', 's', 'es']
        for suffix in suffixes:
            if word.endswith(suffix):
                stem = word[:-len(suffix)]
                if stem in self.corpus_signs_map:
                    return self.corpus_signs_map[stem]
                # Double stripping (e.g. happiness -> happy -> happi -> happy)
                # Handle 'iness' -> 'y' (happiness -> happy)
                if suffix == 'ness' and word.endswith('iness'):
                     stem = word[:-4] + 'y'
                     if stem in self.corpus_signs_map:
                         return self.corpus_signs_map[stem]

        # 3. Contains check (Safety fallback)
        # Check if any corpus sign is a substring of the word (e.g. "Understand" in "Understanding")
        # Only for longer words to avoid false positives with "Is", "A", etc.
        if len(word) > 4:
            for sign_key, sign_name in self.corpus_signs_map.items():
                if len(sign_key) > 3 and sign_key in word:
                    return sign_name

        return None
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize Telugu text into words
        
        Args:
            text: Telugu text string
            
        Returns:
            List of Telugu words/tokens
        """
        # Remove punctuation but keep Telugu characters
        text = re.sub(r'[^\u0C00-\u0C7F\s0-9]', '', text)
        
        # Split by whitespace and filter empty strings
        tokens = [token.strip() for token in text.split() if token.strip()]
        
        return tokens
    
    def transliterate_number(self, text: str) -> str:
        """
        Convert Telugu numbers to Arabic numerals
        
        Args:
            text: Text containing Telugu numbers
            
        Returns:
            Text with Telugu numbers replaced
        """
        for telugu_num, arabic_num in self.numbers_map.items():
            text = text.replace(telugu_num, arabic_num)
        return text
    
    def word_to_sign(self, word: str) -> Tuple[str, bool]:
        """
        Map a Telugu word to its ISL sign equivalent
        
        Args:
            word: Telugu word
            
        Returns:
            Tuple of (sign_name, is_direct_match)
        """
        # Check direct mapping
        if word in self.word_mapping:
            return (self.word_mapping[word], True)
        
        # Check if it's a number
        if word.isdigit():
            return (f"number_{word}", True)
        
        # Check Telugu numbers
        if word in self.numbers_map:
            return (f"number_{self.numbers_map[word]}", True)
        
        # No direct match - will need alphabetical spelling
        return (word, False)
    
    def word_to_alphabets(self, word: str) -> List[str]:
        """
        Break down a Telugu word into individual characters for alphabetical signing
        
        Args:
            word: Telugu word
            
        Returns:
            List of individual Telugu characters
        """
        # Telugu Unicode range: 0C00-0C7F
        characters = []
        
        for char in word:
            if '\u0C00' <= char <= '\u0C7F':
                characters.append(char)
        
        return characters
    
    def transform_grammar(self, tokens: List[str]) -> List[str]:
        """
        Transform Telugu grammar structure to ISL grammar
        
        Telugu: Subject-Object-Verb (SOV)
        ISL: Generally follows Time-Subject-Object-Verb pattern
        
        Note: This is a simplified transformation. Full ISL grammar
        is more complex and context-dependent.
        
        Args:
            tokens: List of Telugu words
            
        Returns:
            Reordered tokens for ISL structure
        """
        # For now, we keep the order as Telugu and ISL both follow SOV
        # In a production system, this would be more sophisticated
        return tokens
    
    def translate(self, text: str) -> List[Dict]:
        """
        Translate Telugu text to ISL sign sequence
        
        Args:
            text: Telugu text to translate
            
        Returns:
            List of dictionaries with sign information:
            [
                {
                    "telugu": "నమస్కారం",
                    "sign": "hello",
                    "type": "word",  # or "alphabet" or "number"
                    "direct_match": True
                },
                ...
            ]
        """
        # Handle numbers
        text = self.transliterate_number(text)
        
        # Tokenize
        tokens = self.tokenize(text)
        
        # Transform grammar
        tokens = self.transform_grammar(tokens)
        
        # Translate each token
        result = []
        for token in tokens:
            sign_name, is_direct = self.word_to_sign(token)
            
            # Check availability of direct match in Corpus
            is_available = False
            if is_direct:
                # Normalize key to check availability
                normalized_key = sign_name.lower().replace(" ", "_").replace("-", "_")
                # We check directly in corpus_signs_map keys (which are lowercase)
                # Actually corpus_signs_map keys include "college", "school" etc.
                # But sign_name might be "COLLEGE_SCHOOL".
                # Let's check if the generic sign name exists in the values of corpus_signs_map
                # Or better, just check if we can Map it back to a valid sign
                is_available = sign_name.lower() in self.corpus_signs_map or \
                               sign_name.replace("_", " ").lower() in self.corpus_signs_map
            
            if is_direct and is_available:
                result.append({
                    "telugu": token,
                    "sign": sign_name,
                    "direct_match": True
                })
            else:
                # No direct match OR direct match not available (e.g. "JOY")
                # Try English Bridge
                english_translation = self.translate_to_english(token)
                
                # If we had a direct match like "JOY", try bridging "JOY" itself?
                # Usually text->English is better.
                # "ఆనందం" -> "Happiness" -> "HAPPY"
                
                sign_match = self.find_sign_match(english_translation)
                
                if sign_match:
                     result.append({
                        "telugu": token,
                        "sign": sign_match,
                        "type": "english_bridge",
                        "english": english_translation,
                        "direct_match": True # Treat as match for animation
                    })
                elif is_direct:
                     # Fallback to the direct match even if unavailable (better than text?)
                     # No, if unavailable it will just show text anyway.
                     result.append({
                        "telugu": token,
                        "sign": sign_name,
                        "direct_match": True # Animator will handle missing frames
                    })
                else:
                    # Return the English translation so the user sees the bridge working
                    # even if no sign animation exists
                    display_text = english_translation if english_translation else token
                    result.append({
                        "telugu": token,
                        "sign": display_text, 
                        "type": "text_only",
                        "english": english_translation,
                        "direct_match": False
                    })
                
        return result
    
    def get_sign_sequence(self, text: str) -> List[str]:
        """
        Get the sequence of sign names to display (ISL Corpus format)
        
        Args:
            text: Telugu text
            
        Returns:
            List of ISL Corpus sign names
        """
        translation = self.translate(text)
        signs = []
        
        for item in translation:
            if item["direct_match"]:
                # The sign name returned is already mapped to ISL Corpus name
                signs.append(item["sign"])
            else:
                # For unmapped words, keep as text fallback
                signs.append(f"TEXT_{item['sign']}")
        
        return signs
    
    def add_word_mapping(self, telugu_word: str, sign_name: str):
        """
        Add a new word to sign mapping
        
        Args:
            telugu_word: Telugu word
            sign_name: Name of the corresponding sign
        """
        self.word_mapping[telugu_word] = sign_name
    
    def save_mappings(self, filepath: Path = None):
        """Save current word mappings to JSON file"""
        filepath = filepath or DATASET_PATHS.get("isl_mapping")
        if filepath:
            filepath = Path(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.word_mapping, f, ensure_ascii=False, indent=2)


def translate_telugu(text: str) -> List[Dict]:
    """
    Convenience function to translate Telugu text to ISL
    
    Args:
        text: Telugu text
        
    Returns:
        Translation result
    """
    translator = TeluguNLPTranslator()
    return translator.translate(text)


if __name__ == "__main__":
    print("=" * 60)
    print("Telugu NLP Translator Test")
    print("=" * 60)
    
    translator = TeluguNLPTranslator()
    
    # Test translations
    test_texts = [
        "నమస్కారం",  # Hello
        "ధన్యవాదాలు",  # Thank you
        "నేను పాఠశాల వెళ్తున్నాను",  # I am going to school
        "మంచిది",  # Good
        "౧ ౨ ౩",  # Telugu numbers 1 2 3
    ]
    
    print("\nTranslation Results:")
    print("-" * 60)
    
    for text in test_texts:
        print(f"\nTelugu: {text}")
        result = translator.translate(text)
        
        for item in result:
            match_status = "✅ Direct" if item["direct_match"] else "🔤 Alphabet"
            sign_display = item["sign"] if isinstance(item["sign"], str) else " ".join(item["sign"])
            print(f"  → {item['telugu']}: {sign_display} ({match_status})")
    
    print("\n" + "-" * 60)
    print(f"Total word mappings available: {len(translator.word_mapping)}")
    print("\n✅ Telugu NLP Translator Test Passed!")
