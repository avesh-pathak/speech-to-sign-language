"""
Launch the Telugu Sign Language GUI Application
With enhanced ISL Corpus animator (114 signs, 2072+ frames)
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from pathlib import Path
import sys

sys.path.insert(0, r"c:\Users\iamav\Desktop\Claude Capstone\telugu_speech_to_sign")

from gui.app import main

print("=" * 80)
print("LAUNCHING TELUGU SIGN LANGUAGE GUI")
print("=" * 80)
print("Features:")
print("  • 114 ISL Corpus signs")
print("  • 2,072+ animation frames")
print("  • 214 Telugu word mappings")
print("  • Real-time speech recognition")
print("  • Continuous animation playback")
print("=" * 80)

if __name__ == "__main__":
    main()
