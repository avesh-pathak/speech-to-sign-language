"""
ISL Corpus Data Preparation and Indexing
Prepares and indexes ISL_CORPUS frames for animation playback
"""
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))

from config.config import DATASET_PATHS, COMMON_TELUGU_WORDS
from modules.isl_corpus_animator import ISLCorpusAnimator


def prepare_isl_corpus():
    """
    Prepare ISL_CORPUS by:
    1. Indexing all available signs and their frames
    2. Validating frame files
    3. Creating a comprehensive sign database
    4. Generating enhanced mappings
    """
    print("=" * 60)
    print("ISL Corpus Data Preparation")
    print("=" * 60)
    
    corpus_frames_dir = DATASET_PATHS.get("isl_corpus_frames")
    if not corpus_frames_dir or not corpus_frames_dir.exists():
        print(f"❌ ISL_CORPUS directory not found: {corpus_frames_dir}")
        return False
    
    print(f"\n📁 ISL_CORPUS location: {corpus_frames_dir}")
    
    # Initialize animator to use its indexing
    animator = ISLCorpusAnimator()
    
    # Validate corpus
    print("\n🔍 Validating ISL_CORPUS...")
    validation = animator.validate_corpus()
    
    print(f"   Total signs found: {validation['total_signs']}")
    print(f"   Signs with frames: {validation['signs_with_frames']}")
    print(f"   Total frame images: {validation['total_images']}")
    print(f"   Avg frames per sign: {validation['average_frames_per_sign']:.1f}")
    
    # Build comprehensive sign database
    print("\n📋 Building sign database...")
    sign_database = build_sign_database(animator, corpus_frames_dir)
    
    # Save database
    db_path = DATASET_PATHS["mappings"] / "isl_corpus_signs.json"
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(sign_database, f, indent=2, ensure_ascii=False)
    print(f"   ✓ Saved sign database: {db_path}")
    
    # Create Telugu to ISL Corpus mappings
    print("\n🔗 Creating Telugu-to-ISL mappings...")
    isl_mappings = create_telugu_isl_mappings(animator, sign_database)
    
    mapping_path = DATASET_PATHS["mappings"] / "telugu_to_isl_corpus.json"
    with open(mapping_path, 'w', encoding='utf-8') as f:
        json.dump(isl_mappings, f, indent=2, ensure_ascii=False)
    print(f"   ✓ Saved mappings: {mapping_path}")
    print(f"   ✓ Mapped {len(isl_mappings)} Telugu words to ISL signs")
    
    # Create training index for quick lookups
    print("\n⚡ Creating fast lookup index...")
    lookup_index = create_lookup_index(animator, sign_database)
    
    index_path = DATASET_PATHS["mappings"] / "isl_corpus_index.json"
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(lookup_index, f, indent=2, ensure_ascii=False)
    print(f"   ✓ Saved lookup index: {index_path}")
    
    # Print sample signs and their mappings
    print("\n📺 Sample Signs and Mappings:")
    print("-" * 60)
    
    samples = list(sign_database.items())[:10]
    for sign_name, sign_info in samples:
        frames = sign_info.get('frame_count', 0)
        # Find any Telugu words mapped to this sign
        mapped_words = [w for w, s in isl_mappings.items() if s == sign_name]
        if mapped_words:
            words_str = ", ".join(mapped_words[:3])
            if len(mapped_words) > 3:
                words_str += f", +{len(mapped_words)-3} more"
            print(f"   {sign_name:30s} | {frames:2d} frames | ⟵ {words_str}")
        else:
            print(f"   {sign_name:30s} | {frames:2d} frames | ⟵ (not mapped)")
    
    # Print statistics
    print("\n" + "=" * 60)
    print("📊 Preparation Summary")
    print("=" * 60)
    print(f"✓ Total signs indexed: {len(sign_database)}")
    print(f"✓ Total frame images: {validation['total_images']}")
    print(f"✓ Telugu words mapped: {len(isl_mappings)}")
    print(f"✓ Ready for animation playback!")
    print("=" * 60 + "\n")
    
    return True


def build_sign_database(animator: ISLCorpusAnimator, corpus_dir: Path) -> Dict:
    """
    Build a comprehensive database of all signs with metadata
    
    Args:
        animator: ISLCorpusAnimator instance with indexed signs
        corpus_dir: Path to ISL_CORPUS Frames_Word_Level directory
        
    Returns:
        Dictionary of sign metadata
    """
    sign_database = {}
    
    for sign_key, sign_path in animator.available_signs.items():
        # Get all image files
        image_files = sorted(
            list(sign_path.glob("*.[jJ][pP][gG]")) + 
            list(sign_path.glob("*.[pP][nN][gG]"))
        )
        
        frame_count = len(image_files)
        
        # Get original directory name (proper casing)
        original_name = sign_path.name
        
        sign_database[sign_key] = {
            "original_name": original_name,
            "directory": str(sign_path.relative_to(corpus_dir)),
            "frame_count": frame_count,
            "frames": [f.name for f in image_files],
            "status": "ready" if frame_count > 0 else "empty"
        }
    
    return sign_database


def create_telugu_isl_mappings(animator: ISLCorpusAnimator, 
                              sign_database: Dict) -> Dict:
    """
    Create Telugu to ISL Corpus sign mappings
    Combines manual mappings with animator's loaded mappings
    
    Args:
        animator: ISLCorpusAnimator with loaded mappings
        sign_database: Database of all signs
        
    Returns:
        Dictionary mapping Telugu words to ISL sign names
    """
    mappings = {}
    
    # Start with animator's loaded mappings
    if animator.telugu_isl_mapping:
        mappings.update(animator.telugu_isl_mapping)
    
    # Add from COMMON_TELUGU_WORDS if the sign exists
    for telugu_word, sign_name in COMMON_TELUGU_WORDS.items():
        sign_key = sign_name.lower().replace(" ", "_")
        if sign_key in sign_database:
            mappings[telugu_word] = sign_key
    
    return mappings


def create_lookup_index(animator: ISLCorpusAnimator, 
                       sign_database: Dict) -> Dict:
    """
    Create a fast lookup index for animation playback
    
    Args:
        animator: ISLCorpusAnimator instance
        sign_database: Database of all signs
        
    Returns:
        Fast lookup index dictionary
    """
    index = {
        "version": "1.0",
        "total_signs": len(sign_database),
        "corpus_dir": str(DATASET_PATHS.get("isl_corpus_frames")),
        "signs": {}
    }
    
    for sign_key, sign_info in sign_database.items():
        index["signs"][sign_key] = {
            "frames": sign_info["frame_count"],
            "path": sign_info["directory"],
            "ready": sign_info["status"] == "ready"
        }
    
    return index


def test_animation_loading():
    """
    Test that animations can be loaded successfully
    """
    print("\n" + "=" * 60)
    print("🧪 Testing Animation Loading")
    print("=" * 60)
    
    animator = ISLCorpusAnimator()
    
    # Test a few signs
    test_signs = ["HAPPY", "HELLO_HI", "THANK", "PLEASE", "GOOD"]
    
    for sign in test_signs:
        sign_key = sign.lower().replace(" ", "_")
        if animator.has_sign(sign_key):
            frames = animator.load_sign_frames(sign_key)
            if frames:
                print(f"✓ {sign:20s} - Loaded {len(frames):2d} frames")
            else:
                print(f"✗ {sign:20s} - Failed to load frames")
        else:
            print(f"✗ {sign:20s} - Sign not found")
    
    print("=" * 60 + "\n")


def create_training_dataset():
    """
    Create a training-ready dataset with frame sequences
    This can be used for model training later
    """
    print("\n" + "=" * 60)
    print("🏋️ Creating Training Dataset Structure")
    print("=" * 60)
    
    animator = ISLCorpusAnimator()
    corpus_dir = DATASET_PATHS.get("isl_corpus_frames")
    
    # Create training data directory
    training_dir = DATASET_PATHS["mappings"].parent / "training_data"
    training_dir.mkdir(parents=True, exist_ok=True)
    
    # Create metadata file for training
    training_metadata = {
        "dataset_name": "ISL_Corpus_Training",
        "source": str(corpus_dir),
        "total_signs": len(animator.available_signs),
        "signs": {}
    }
    
    for sign_key, sign_path in animator.available_signs.items():
        image_files = sorted(
            list(sign_path.glob("*.[jJ][pP][gG]")) + 
            list(sign_path.glob("*.[pP][nN][gG]"))
        )
        
        if len(image_files) > 0:
            training_metadata["signs"][sign_key] = {
                "source_dir": str(sign_path),
                "frame_count": len(image_files),
                "frame_files": [f.name for f in image_files]
            }
    
    # Save metadata
    metadata_path = training_dir / "metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(training_metadata, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Created training dataset metadata: {metadata_path}")
    print(f"✓ Total signs in dataset: {len(training_metadata['signs'])}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    print("\n")
    try:
        # Prepare ISL Corpus
        if prepare_isl_corpus():
            # Test loading
            test_animation_loading()
            
            # Create training dataset
            create_training_dataset()
            
            print("✅ Data preparation complete!")
            print("   You can now run: python main.py --mode gui")
        else:
            print("❌ Data preparation failed!")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error during preparation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
