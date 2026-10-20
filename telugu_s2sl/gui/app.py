"""Tkinter desktop interface for the Telugu -> ISL translator."""
from __future__ import annotations

import os
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import List

from PIL import Image, ImageTk

if __package__ in (None, ""):  # Allow ``python telugu_s2sl/gui/app.py``.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

from telugu_s2sl.config import GUI_CONFIG, ensure_directories
from telugu_s2sl.pipeline import SpeechToSignPipeline, TranslationBundle


class TeluguSignApp:
    """Main window: input on the left, sign playback on the right."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(GUI_CONFIG["window_title"])
        self.root.geometry(GUI_CONFIG["window_size"])
        self.root.configure(bg="#1a1a2e")
        self.root.minsize(1040, 700)

        self.pipeline = SpeechToSignPipeline()

        self.is_recording = False
        self.animation_sequence: List[dict] = []
        self.sequence_index = 0
        self.current_frames: List[Image.Image] = []
        self.frame_index = 0
        self.animation_running = False
        self.animation_paused = False
        self.hold_ticks = 0
        self.frame_interval = max(30, int(1000 / GUI_CONFIG["fps"]))
        self._photo = None  # keep a reference to the current Tk image

        self.colors = {
            "bg_dark": "#1a1a2e",
            "bg_medium": "#16213e",
            "bg_light": "#0f3460",
            "accent": "#e94560",
            "text": "#eaeaea",
            "text_secondary": "#a0a0a0",
            "success": "#00d26a",
            "warning": "#ffc107",
        }

        self._create_styles()
        self._build_ui()
        self._tick()

    # ------------------------------------------------------------------ build
    def _create_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Accent.TButton",
            font=(GUI_CONFIG["font_family"], 12, "bold"),
            padding=10,
        )

    def _build_ui(self) -> None:
        main = tk.Frame(self.root, bg=self.colors["bg_dark"])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=18)

        tk.Label(
            main,
            text="తెలుగు సంకేత భాష అనువాదకుడు",
            font=(GUI_CONFIG["font_family"], 24, "bold"),
            fg=self.colors["accent"],
            bg=self.colors["bg_dark"],
        ).pack(pady=(0, 2))

        tk.Label(
            main,
            text="Telugu Speech → Indian Sign Language",
            font=(GUI_CONFIG["font_family"], 12),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_dark"],
        ).pack(pady=(0, 16))

        content = tk.Frame(main, bg=self.colors["bg_dark"])
        content.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(content, bg=self.colors["bg_medium"])
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        self._build_input_panel(left)

        right = tk.Frame(content, bg=self.colors["bg_medium"])
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))
        self._build_animation_panel(right)

        self.status_var = tk.StringVar(value="Ready")
        tk.Label(
            main,
            textvariable=self.status_var,
            font=(GUI_CONFIG["font_family"], 10),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_dark"],
            anchor="w",
        ).pack(fill=tk.X, pady=(14, 0))

    def _build_input_panel(self, parent: tk.Frame) -> None:
        tk.Label(
            parent,
            text="Audio input",
            font=(GUI_CONFIG["font_family"], 14, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg_medium"],
        ).pack(pady=(18, 10))

        buttons = tk.Frame(parent, bg=self.colors["bg_medium"])
        buttons.pack(pady=6)

        self.record_btn = tk.Button(
            buttons,
            text="🎤  Record",
            font=(GUI_CONFIG["font_family"], 12, "bold"),
            fg="white",
            bg=self.colors["accent"],
            activebackground="#c13550",
            padx=18,
            pady=9,
            cursor="hand2",
            command=self._toggle_recording,
        )
        self.record_btn.pack(side=tk.LEFT, padx=4)

        tk.Button(
            buttons,
            text="📁  Upload",
            font=(GUI_CONFIG["font_family"], 12, "bold"),
            fg="white",
            bg=self.colors["bg_light"],
            activebackground="#1a4980",
            padx=18,
            pady=9,
            cursor="hand2",
            command=self._upload_audio,
        ).pack(side=tk.LEFT, padx=4)

        tk.Label(
            parent,
            text="Or type Telugu text",
            font=(GUI_CONFIG["font_family"], 11),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_medium"],
        ).pack(pady=(24, 8))

        text_row = tk.Frame(parent, bg=self.colors["bg_medium"])
        text_row.pack(fill=tk.X, padx=18)

        self.text_input = tk.Entry(
            text_row,
            font=(GUI_CONFIG["font_family"], 14),
            bg=self.colors["bg_dark"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief=tk.FLAT,
        )
        self.text_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=9, padx=(0, 8))
        self.text_input.bind("<Return>", lambda _event: self._translate_text())

        tk.Button(
            text_row,
            text="Translate",
            font=(GUI_CONFIG["font_family"], 11, "bold"),
            fg="white",
            bg=self.colors["success"],
            padx=14,
            pady=6,
            cursor="hand2",
            command=self._translate_text,
        ).pack(side=tk.RIGHT)

        self._display_block(parent, "Recognized text", height=3, color=self.colors["text"])
        self.recognized_text = self._last_text_widget

        self._display_block(parent, "ISL translation", height=4, color=self.colors["accent"])
        self.translation_text = self._last_text_widget

    def _display_block(self, parent: tk.Frame, label: str, height: int, color: str) -> None:
        tk.Label(
            parent,
            text=label,
            font=(GUI_CONFIG["font_family"], 11),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_medium"],
        ).pack(pady=(22, 8))

        widget = tk.Text(
            parent,
            font=(GUI_CONFIG["font_family"], 15),
            bg=self.colors["bg_dark"],
            fg=color,
            height=height,
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=10,
            pady=8,
        )
        widget.pack(fill=tk.X, padx=18)
        self._last_text_widget = widget

    def _build_animation_panel(self, parent: tk.Frame) -> None:
        tk.Label(
            parent,
            text="Sign language animation",
            font=(GUI_CONFIG["font_family"], 14, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg_medium"],
        ).pack(pady=(18, 10))

        self.animation_frame = tk.Frame(
            parent, bg=self.colors["bg_dark"], width=400, height=400
        )
        self.animation_frame.pack(pady=8)
        self.animation_frame.pack_propagate(False)

        self.animation_label = tk.Label(
            self.animation_frame,
            bg=self.colors["bg_dark"],
            text="🤟",
            font=(GUI_CONFIG["font_family"], 96),
            fg=self.colors["text_secondary"],
        )
        self.animation_label.pack(expand=True)

        self.current_sign_var = tk.StringVar(value="")
        tk.Label(
            parent,
            textvariable=self.current_sign_var,
            font=(GUI_CONFIG["font_family"], 16, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg_medium"],
        ).pack(pady=8)

        controls = tk.Frame(parent, bg=self.colors["bg_medium"])
        controls.pack(pady=6)

        self.play_btn = tk.Button(
            controls,
            text="▶  Play",
            font=(GUI_CONFIG["font_family"], 11),
            fg="white",
            bg=self.colors["success"],
            padx=14,
            pady=5,
            cursor="hand2",
            command=self._play_animation,
        )
        self.play_btn.pack(side=tk.LEFT, padx=4)

        tk.Button(
            controls,
            text="⏹  Stop",
            font=(GUI_CONFIG["font_family"], 11),
            fg="white",
            bg=self.colors["accent"],
            padx=14,
            pady=5,
            cursor="hand2",
            command=self._stop_animation,
        ).pack(side=tk.LEFT, padx=4)

        tk.Button(
            controls,
            text="🔄  Reset",
            font=(GUI_CONFIG["font_family"], 11),
            fg="white",
            bg=self.colors["bg_light"],
            padx=14,
            pady=5,
            cursor="hand2",
            command=self._reset_all,
        ).pack(side=tk.LEFT, padx=4)

        tk.Label(
            parent,
            text="Sign sequence",
            font=(GUI_CONFIG["font_family"], 11),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_medium"],
        ).pack(pady=(18, 5))

        self.sequence_text = tk.Text(
            parent,
            font=(GUI_CONFIG["font_family"], 12),
            bg=self.colors["bg_dark"],
            fg=self.colors["text"],
            height=3,
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=10,
            pady=8,
        )
        self.sequence_text.pack(fill=tk.X, padx=18, pady=(0, 16))

    # ---------------------------------------------------------------- recording
    def _toggle_recording(self) -> None:
        if self.is_recording:
            self.is_recording = False
            self.record_btn.configure(text="🎤  Record", bg=self.colors["accent"])
            self.status_var.set("Recording cancelled")
        else:
            self._start_recording()

    def _start_recording(self) -> None:
        self.is_recording = True
        self.record_btn.configure(text="⏹  Stop", bg=self.colors["warning"])
        self.status_var.set("🎤 Listening…")

        thread = threading.Thread(target=self._record_and_recognize, daemon=True)
        thread.start()

    def _record_and_recognize(self) -> None:
        def on_status(message: str) -> None:
            self.root.after(0, lambda: self.status_var.set(message))

        def on_processing() -> None:
            self.root.after(0, lambda: self.status_var.set("⏳ Processing speech…"))

        try:
            text = self.pipeline.asr.recognize_from_microphone(
                on_listen_complete=on_processing,
                on_status=on_status,
            )
            self.root.after(0, lambda: self._handle_result(text))
        except Exception as exc:
            self.root.after(0, lambda: self._show_error(str(exc)))
        finally:
            self.root.after(0, self._stop_recording)

    def _stop_recording(self) -> None:
        self.is_recording = False
        self.record_btn.configure(text="🎤  Record", bg=self.colors["accent"])

    # ------------------------------------------------------------------ files
    def _upload_audio(self) -> None:
        path = filedialog.askopenfilename(
            title="Select audio",
            filetypes=[
                ("Audio", "*.wav *.mp3 *.flac *.ogg"),
                ("WAV", "*.wav"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return

        self.status_var.set(f"Processing {Path(path).name}…")
        thread = threading.Thread(target=self._process_audio_file, args=(path,), daemon=True)
        thread.start()

    def _process_audio_file(self, path: str) -> None:
        try:
            text = self.pipeline.transcribe_file(path)
            self.root.after(0, lambda: self._handle_result(text))
        except Exception as exc:
            self.root.after(0, lambda: self._show_error(str(exc)))

    # -------------------------------------------------------------- translation
    def _translate_text(self) -> None:
        text = self.text_input.get().strip()
        if text:
            self._handle_result(text)

    def _handle_result(self, text: str) -> None:
        self.recognized_text.delete("1.0", tk.END)
        self.recognized_text.insert(tk.END, text)

        bundle: TranslationBundle = self.pipeline.translate_text(text)
        self._render_bundle(bundle)

    def _render_bundle(self, bundle: TranslationBundle) -> None:
        self.translation_text.delete("1.0", tk.END)
        parts = []
        for item in bundle.tokens:
            if item.get("direct_match"):
                parts.append(f"[{item['sign']}]")
            else:
                parts.append(f"({item['sign']})")
        self.translation_text.insert(tk.END, " ".join(parts))

        self.sequence_text.delete("1.0", tk.END)
        self.sequence_text.insert(tk.END, " → ".join(bundle.signs))

        self.animation_sequence = bundle.animation
        self.sequence_index = 0
        self.current_frames = []
        self.frame_index = 0
        self.hold_ticks = 0

        missing = bundle.missing_steps
        suffix = f" · {missing} fallback" if missing else ""
        self.status_var.set(f"Translated {len(bundle.signs)} sign(s){suffix}")

        # A new sentence restarts playback instead of toggling Pause.
        self.animation_running = False
        self.animation_paused = False
        self.play_btn.configure(text="▶  Play")
        self._play_animation()

    # --------------------------------------------------------------- animation
    def _play_animation(self) -> None:
        if not self.animation_sequence:
            self.status_var.set("Nothing to play yet")
            return

        if self.sequence_index >= len(self.animation_sequence):
            self.sequence_index = 0
            self.current_frames = []
            self.frame_index = 0

        if not self.animation_running:
            self.animation_running = True
            self.animation_paused = False
            self.play_btn.configure(text="⏸  Pause")
            self.status_var.set("▶ Playing animation…")
        elif self.animation_paused:
            self.animation_paused = False
            self.play_btn.configure(text="⏸  Pause")
            self.status_var.set("▶ Resuming…")
        else:
            self.animation_paused = True
            self.play_btn.configure(text="▶  Resume")
            self.status_var.set("⏸ Paused")

    def _stop_animation(self) -> None:
        self.animation_running = False
        self.animation_paused = False
        self.sequence_index = 0
        self.frame_index = 0
        self.current_frames = []
        self.current_sign_var.set("Stopped")
        self.play_btn.configure(text="▶  Play")
        self.status_var.set("Animation stopped")

    def _tick(self) -> None:
        if self.animation_running and not self.animation_paused:
            if self.hold_ticks > 0:
                self.hold_ticks -= 1
            elif self.sequence_index >= len(self.animation_sequence):
                self.animation_running = False
                self.current_sign_var.set("✓ Complete")
                self.status_var.set("Animation complete")
                self.play_btn.configure(text="▶  Play")
            else:
                self._step()

        self.root.after(self.frame_interval, self._tick)

    def _step(self) -> None:
        item = self.animation_sequence[self.sequence_index]

        if item.get("type") != "sign" or not item.get("available"):
            self._show_text(item.get("message", item.get("telugu", "")), item.get("telugu", ""))
            self.sequence_index += 1
            self.current_frames = []
            self.frame_index = 0
            self.hold_ticks = max(1, int(900 / self.frame_interval))
            return

        if not self.current_frames:
            self.current_frames = item["frames"]
            self.frame_index = 0
            self.current_sign_var.set(f"{item['isl_sign']}  ({item['telugu']})")

        if self.frame_index >= len(self.current_frames):
            self.sequence_index += 1
            self.current_frames = []
            self.frame_index = 0
            return

        frame = self.current_frames[self.frame_index]
        self.frame_index += 1
        self._show_image(frame)

    def _show_image(self, image: Image.Image) -> None:
        try:
            size = GUI_CONFIG["display_size"]
            if image.size != size:
                image = image.resize(size, Image.Resampling.LANCZOS)
            self._photo = ImageTk.PhotoImage(image)
            self.animation_label.configure(image=self._photo, text="")
        except Exception as exc:
            print(f"Could not render frame: {exc}")

    def _show_text(self, text: str, telugu: str = "") -> None:
        display = (text or "?")[:18]
        self._photo = None
        self.animation_label.configure(
            image="",
            text=display,
            font=(GUI_CONFIG["font_family"], 34),
            fg=self.colors["text_secondary"],
        )
        self.current_sign_var.set(f"Fallback: {telugu or text}")

    # ------------------------------------------------------------------ reset
    def _reset_all(self) -> None:
        self._stop_animation()
        for widget in (self.recognized_text, self.translation_text, self.sequence_text):
            widget.delete("1.0", tk.END)
        self.text_input.delete(0, tk.END)
        self.current_sign_var.set("")
        self.animation_sequence = []
        self.current_frames = []
        self.frame_index = 0
        self.animation_label.configure(
            image="",
            text="🤟",
            font=(GUI_CONFIG["font_family"], 96),
            fg=self.colors["text_secondary"],
        )
        self.status_var.set("Ready")

    def _show_error(self, message: str) -> None:
        messagebox.showerror("Error", message)
        self.status_var.set("Error")


def main() -> None:
    ensure_directories()
    root = tk.Tk()
    TeluguSignApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
