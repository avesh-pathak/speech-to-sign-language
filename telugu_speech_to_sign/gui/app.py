"""
Telugu Speech-to-Sign Language Translation GUI Application
Main graphical interface using Tkinter
"""
import os
import sys
import threading
import queue
from pathlib import Path
from datetime import datetime
from typing import Optional, List
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import imageio.v2 as imageio

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set environment variable before importing TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from config.config import (
    GUI_CONFIG, DATASET_PATHS, TRAINED_DIR, COMMON_TELUGU_WORDS
)
from modules.audio_processor import AudioProcessor
from modules.asr_module import TeluguASR
from modules.nlp_translator import TeluguNLPTranslator
from modules.sign_animator import SignAnimator, create_placeholder_gifs
from modules.isl_corpus_animator_enhanced import EnhancedISLCorpusAnimator


class TeluguSignApp:
    """
    Main GUI Application for Telugu Speech-to-Sign Language Translation
    """
    
    def __init__(self, root: tk.Tk):
        """Initialize the application"""
        self.root = root
        self.root.title(GUI_CONFIG["window_title"])
        self.root.geometry(GUI_CONFIG["window_size"])
        self.root.configure(bg='#1a1a2e')
        
        # Initialize modules
        self.audio_processor = AudioProcessor()
        self.asr = TeluguASR()
        self.translator = TeluguNLPTranslator()
        self.animator = SignAnimator()
        self.corpus_animator = EnhancedISLCorpusAnimator()  # Use Enhanced ISL Corpus animator
        
        # State variables
        self.is_recording = False
        self.current_audio_path: Optional[Path] = None
        self.animation_queue = queue.Queue()
        self.current_gif_frames: List[ImageTk.PhotoImage] = []
        self.current_frame_index = 0
        self.animation_running = False
        self.current_animation_sequence: List[Dict] = []
        self.animation_sequence_index = 0
        self.current_sign_frames: List[Image.Image] = []
        self.animation_paused = False
        
        # Ensure GIFs exist
        # self._ensure_gifs_exist()  # User requested to use only Real Corpus
        
        # Build UI
        self._create_styles()
        self._build_ui()
        
        # Start animation thread
        self._start_animation_loop()
    
    def _ensure_gifs_exist(self):
        """Ensure placeholder GIFs are created"""
        if len(self.animator.available_signs) == 0:
            print("Creating placeholder GIFs...")
            create_placeholder_gifs()
            self.animator._scan_available_gifs()
    
    def _create_styles(self):
        """Create custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom colors
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_light': '#0f3460',
            'accent': '#e94560',
            'text': '#eaeaea',
            'text_secondary': '#a0a0a0',
            'success': '#00d26a',
            'warning': '#ffc107'
        }
        
        # Configure button style
        style.configure(
            'Accent.TButton',
            font=(GUI_CONFIG["font_family"], 12, 'bold'),
            padding=10
        )
    
    def _build_ui(self):
        """Build the main user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="తెలుగు సంకేత భాష అనువాదకుడు",
            font=(GUI_CONFIG["font_family"], 24, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg_dark']
        )
        title_label.pack(pady=(0, 5))
        
        subtitle = tk.Label(
            main_frame,
            text="Telugu Sign Language Translator",
            font=(GUI_CONFIG["font_family"], 12),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_dark']
        )
        subtitle.pack(pady=(0, 20))
        
        # Content area (split into left and right panels)
        content_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left Panel - Input & Text
        left_panel = tk.Frame(content_frame, bg=self.colors['bg_medium'], width=500)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self._build_input_panel(left_panel)
        
        # Right Panel - Animation Display
        right_panel = tk.Frame(content_frame, bg=self.colors['bg_medium'], width=500)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        right_panel.pack_propagate(False)
        
        self._build_animation_panel(right_panel)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            main_frame,
            textvariable=self.status_var,
            font=(GUI_CONFIG["font_family"], 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_dark'],
            anchor='w'
        )
        status_bar.pack(fill=tk.X, pady=(20, 0))
    
    def _build_input_panel(self, parent):
        """Build the input controls panel"""
        # Panel title
        tk.Label(
            parent,
            text="Audio Input",
            font=(GUI_CONFIG["font_family"], 14, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg_medium']
        ).pack(pady=20)
        
        # Buttons frame
        buttons_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        buttons_frame.pack(pady=10)
        
        # Record button
        self.record_btn = tk.Button(
            buttons_frame,
            text="🎤 Record",
            font=(GUI_CONFIG["font_family"], 12, 'bold'),
            fg='white',
            bg=self.colors['accent'],
            activebackground='#c13550',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self._toggle_recording
        )
        self.record_btn.pack(side=tk.LEFT, padx=5)
        
        # Upload button
        upload_btn = tk.Button(
            buttons_frame,
            text="📁 Upload",
            font=(GUI_CONFIG["font_family"], 12, 'bold'),
            fg='white',
            bg=self.colors['bg_light'],
            activebackground='#1a4980',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self._upload_audio
        )
        upload_btn.pack(side=tk.LEFT, padx=5)
        
        # Direct text input
        tk.Label(
            parent,
            text="Or type text (Telugu):",
            font=(GUI_CONFIG["font_family"], 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_medium']
        ).pack(pady=(30, 10))
        
        # Text input frame
        text_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        text_frame.pack(fill=tk.X, padx=20)
        
        self.text_input = tk.Entry(
            text_frame,
            font=(GUI_CONFIG["font_family"], 14),
            bg=self.colors['bg_dark'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief=tk.FLAT,
            width=40
        )
        self.text_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=(0, 10))
        self.text_input.bind('<Return>', lambda e: self._translate_text())
        
        translate_btn = tk.Button(
            text_frame,
            text="Translate",
            font=(GUI_CONFIG["font_family"], 11, 'bold'),
            fg='white',
            bg=self.colors['success'],
            padx=15,
            pady=5,
            cursor='hand2',
            command=self._translate_text
        )
        translate_btn.pack(side=tk.RIGHT)
        
        # Recognized text display
        tk.Label(
            parent,
            text="Recognized Text:",
            font=(GUI_CONFIG["font_family"], 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_medium']
        ).pack(pady=(30, 10))
        
        self.recognized_text = tk.Text(
            parent,
            font=(GUI_CONFIG["font_family"], 16),
            bg=self.colors['bg_dark'],
            fg=self.colors['text'],
            height=3,
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        self.recognized_text.pack(fill=tk.X, padx=20)
        
        # Translation result
        tk.Label(
            parent,
            text="ISL Translation:",
            font=(GUI_CONFIG["font_family"], 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_medium']
        ).pack(pady=(20, 10))
        
        self.translation_text = tk.Text(
            parent,
            font=(GUI_CONFIG["font_family"], 14),
            bg=self.colors['bg_dark'],
            fg=self.colors['accent'],
            height=4,
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        self.translation_text.pack(fill=tk.X, padx=20)
    
    def _build_animation_panel(self, parent):
        """Build the sign language animation panel"""
        # Panel title
        tk.Label(
            parent,
            text="Sign Language Animation",
            font=(GUI_CONFIG["font_family"], 14, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg_medium']
        ).pack(pady=20)
        
        # Animation display frame
        self.animation_frame = tk.Frame(
            parent,
            bg=self.colors['bg_dark'],
            width=400,
            height=400
        )
        self.animation_frame.pack(pady=10)
        self.animation_frame.pack_propagate(False)
        
        # Animation label (will show GIFs)
        self.animation_label = tk.Label(
            self.animation_frame,
            bg=self.colors['bg_dark'],
            text="🤟",
            font=(GUI_CONFIG["font_family"], 100),
            fg=self.colors['text_secondary']
        )
        self.animation_label.pack(expand=True)
        
        # Current sign label
        self.current_sign_var = tk.StringVar(value="")
        tk.Label(
            parent,
            textvariable=self.current_sign_var,
            font=(GUI_CONFIG["font_family"], 16, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg_medium']
        ).pack(pady=10)
        
        # Animation controls
        controls_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        controls_frame.pack(pady=10)
        
        # Play/Pause button
        self.play_btn = tk.Button(
            controls_frame,
            text="▶ Play",
            font=(GUI_CONFIG["font_family"], 11),
            fg='white',
            bg=self.colors['success'],
            padx=15,
            pady=5,
            cursor='hand2',
            command=self._play_animation
        )
        self.play_btn.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        stop_btn = tk.Button(
            controls_frame,
            text="⏹ Stop",
            font=(GUI_CONFIG["font_family"], 11),
            fg='white',
            bg=self.colors['accent'],
            padx=15,
            pady=5,
            cursor='hand2',
            command=self._stop_animation
        )
        stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        reset_btn = tk.Button(
            controls_frame,
            text="🔄 Reset",
            font=(GUI_CONFIG["font_family"], 11),
            fg='white',
            bg=self.colors['bg_light'],
            padx=15,
            pady=5,
            cursor='hand2',
            command=self._reset_all
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Sign sequence display
        tk.Label(
            parent,
            text="Sign Sequence:",
            font=(GUI_CONFIG["font_family"], 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_medium']
        ).pack(pady=(20, 5))
        
        self.sequence_text = tk.Text(
            parent,
            font=(GUI_CONFIG["font_family"], 12),
            bg=self.colors['bg_dark'],
            fg=self.colors['text'],
            height=3,
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        self.sequence_text.pack(fill=tk.X, padx=20, pady=(0, 20))
    
    def _toggle_recording(self):
        """Toggle microphone recording"""
        if not self.is_recording:
            self._start_recording()
        else:
            self._stop_recording()
    
    def _start_recording(self):
        """Start microphone recording"""
        self.is_recording = True
        self.record_btn.configure(
            text="⏹ Stop",
            bg=self.colors['warning']
        )
        self.status_var.set("🎤 Recording...")
        
        # Run recognition in background thread
        thread = threading.Thread(target=self._record_and_recognize)
        thread.daemon = True
        thread.start()
    
    def _stop_recording(self):
        """Stop microphone recording"""
        self.is_recording = False
        self.record_btn.configure(
            text="🎤 Record",
            bg=self.colors['accent']
        )
    
    def _record_and_recognize(self):
        """Record audio from microphone and recognize Telugu speech"""
        try:
            # Callback to update UI when listening finishes and processing starts
            def on_processing_start():
                self.root.after(0, lambda: self.status_var.set("⏳ Processing Speech..."))
            
            # Recognize from microphone
            text = self.asr.recognize_from_microphone(
                on_listen_complete=on_processing_start
            )
            
            # Update UI in main thread
            self.root.after(0, lambda: self._handle_recognition_result(text))
            
        except Exception as e:
            self.root.after(0, lambda: self._show_error(str(e)))
        finally:
            self.root.after(0, self._stop_recording)
    
    def _upload_audio(self):
        """Upload and process an audio file"""
        filetypes = [
            ("Audio files", "*.wav *.mp3 *.flac *.ogg"),
            ("WAV files", "*.wav"),
            ("MP3 files", "*.mp3"),
            ("All files", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=filetypes
        )
        
        if filepath:
            self.current_audio_path = Path(filepath)
            self.status_var.set(f"Processing: {self.current_audio_path.name}")
            
            # Process in background
            thread = threading.Thread(target=self._process_audio_file)
            thread.daemon = True
            thread.start()
    
    def _process_audio_file(self):
        """Process uploaded audio file"""
        try:
            # Recognize speech
            text = self.asr.recognize_from_file(self.current_audio_path)
            
            # Update UI in main thread
            self.root.after(0, lambda: self._handle_recognition_result(text))
            
        except Exception as e:
            self.root.after(0, lambda: self._show_error(str(e)))
    
    def _translate_text(self):
        """Translate text input to sign language"""
        text = self.text_input.get().strip()
        
        if not text:
            return
        
        self._handle_recognition_result(text)
    
    def _handle_recognition_result(self, text: str):
        """Handle recognized text and translate to sign language"""
        # Update recognized text display
        self.recognized_text.delete(1.0, tk.END)
        self.recognized_text.insert(tk.END, text)
        
        # Translate to ISL
        translation = self.translator.translate(text)
        
        # Display translation
        self.translation_text.delete(1.0, tk.END)
        translation_str = ""
        for item in translation:
            if item['direct_match']:
                translation_str += f"[{item['sign']}] "
            else:
                chars = " ".join(item['sign']) if isinstance(item['sign'], list) else item['sign']
                translation_str += f"({chars}) "
        self.translation_text.insert(tk.END, translation_str)
        
        # Get sign sequence
        signs = self.translator.get_sign_sequence(text)
        
        # Update sequence display
        self.sequence_text.delete(1.0, tk.END)
        self.sequence_text.insert(tk.END, " → ".join(signs))
        
        # Create animation sequence from ISL Corpus
        self.current_animation_sequence = self.corpus_animator.create_animation_sequence(signs)
        self.animation_sequence_index = 0
        
        self.status_var.set(f"Translated: {len(signs)} signs - Ready to animate")
        
        # Auto-play animation
        self._play_animation()
    
    def _start_animation_loop(self):
        """Start the animation update loop"""
        self._update_animation()
    
    def _update_animation(self):
        """Update animation frame with continuous playback"""
        if self.animation_running and not self.animation_paused:
            if self.animation_sequence_index < len(self.current_animation_sequence):
                current_item = self.current_animation_sequence[self.animation_sequence_index]
                
                # If moving to a new sign, load its frames
                if not self.current_sign_frames or self.current_frame_index >= len(self.current_sign_frames):
                    if current_item["type"] == "sign" and current_item["available"]:
                        self.current_sign_frames = current_item["frames"]
                        self.current_frame_index = 0
                        self.current_sign_var.set(f"{current_item['isl_sign']} ({current_item['telugu']})")
                    else:
                        # Move to next sign
                        self.current_frame_index = 0
                        self.current_sign_frames = []
                        self.animation_sequence_index += 1
                        self.root.after(300, self._update_animation)  # Transition delay
                        return
                
                # Display current frame
                if self.current_sign_frames:
                    try:
                        img = self.current_sign_frames[self.current_frame_index]
                        # Resize to fit display
                        img_resized = img.resize((400, 400), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img_resized)
                        self.animation_label.configure(image=photo, text="")
                        self.animation_label.image = photo  # Keep a reference
                        
                        self.current_frame_index += 1
                        
                        # Move to next sign when all frames are shown
                        if self.current_frame_index >= len(self.current_sign_frames):
                            self.animation_sequence_index += 1
                            self.current_frame_index = 0
                            self.current_sign_frames = []
                    except Exception as e:
                        print(f"Error displaying frame: {e}")
                        self.animation_sequence_index += 1
                        self.current_frame_index = 0
                        self.current_sign_frames = []
            else:
                # Animation complete
                self.animation_running = False
                self.animation_paused = False
                self.current_sign_var.set("✓ Complete")
                self.status_var.set("Animation complete")
                self.play_btn.configure(text="▶ Play")
        
        # Schedule next update (frame timing based on FPS)
        self.root.after(100, self._update_animation)  # ~10 FPS for frame changes
    
    def _load_next_sign(self):
        """Load the next sign animation from sequence"""
        if self.animation_sequence_index >= len(self.current_animation_sequence):
            self.animation_running = False
            self.animation_paused = False
            self.current_sign_var.set("✓ Complete")
            return
        
        current_item = self.current_animation_sequence[self.animation_sequence_index]
        
        if current_item["type"] == "sign" and current_item["available"]:
            self.current_sign_frames = current_item["frames"]
            self.current_frame_index = 0
            self.current_sign_var.set(f"{current_item['isl_sign']} ({current_item['telugu']})")
        else:
            # Text fallback
            display_text = current_item.get("message", "N/A")
            self.current_sign_frames = []
            self.animation_label.configure(
                image='',
                text=display_text[:10],
                font=(GUI_CONFIG["font_family"], 40)
            )
    
    def _play_animation(self):
        """Start playing the sign animation sequence"""
        if self.animation_sequence_index >= len(self.current_animation_sequence):
            self.animation_sequence_index = 0
            self.status_var.set("Starting animation...")
        
        if not self.animation_running:
            self.animation_running = True
            self.animation_paused = False
            self.play_btn.configure(text="⏸ Pause")
            self.status_var.set("▶ Playing animation...")
        elif self.animation_paused:
            self.animation_paused = False
            self.play_btn.configure(text="⏸ Pause")
            self.status_var.set("▶ Resuming animation...")
        else:
            # Pause
            self.animation_paused = True
            self.play_btn.configure(text="▶ Resume")
            self.status_var.set("⏸ Animation paused")
    
    def _stop_animation(self):
        """Stop the animation"""
        self.animation_running = False
        self.animation_paused = False
        self.animation_sequence_index = 0
        self.current_frame_index = 0
        self.current_sign_frames = []
        self.current_sign_var.set("Stopped")
        self.play_btn.configure(text="▶ Play")
        self.status_var.set("Animation stopped")
    
    def _reset_all(self):
        """Reset all states"""
        self._stop_animation()
        
        # Clear displays
        self.recognized_text.delete(1.0, tk.END)
        self.translation_text.delete(1.0, tk.END)
        self.sequence_text.delete(1.0, tk.END)
        self.text_input.delete(0, tk.END)
        self.current_sign_var.set("")
        self.current_animation_sequence = []
        
        # Reset animation display
        self.current_sign_frames = []
        self.animation_label.configure(
            image='',
            text="🤟",
            font=(GUI_CONFIG["font_family"], 100)
        )
        
        self.status_var.set("Ready")
    
    def _show_error(self, message: str):
        """Show error message"""
        messagebox.showerror("Error", message)
        self.status_var.set("Error occurred")


def main():
    """Launch the application"""
    root = tk.Tk()
    
    # Set icon if available
    try:
        # You can add an icon file later
        pass
    except:
        pass
    
    app = TeluguSignApp(root)
    
    print("=" * 60)
    print("Telugu Speech-to-Sign Language Translator")
    print("=" * 60)
    print("Application started successfully!")
    print("Press Ctrl+C to exit")
    
    root.mainloop()


if __name__ == "__main__":
    main()
