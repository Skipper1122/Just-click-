"""Jarvis AI Voice Assistant - Turkish desktop voice assistant.

Run this file from the VS Code terminal with:
    python main.py
"""

from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import scrolledtext

from assistant import JarvisAssistant
from speech import TurkishSpeaker, TurkishSpeechRecognizer


WAKE_WORD = "jarvis"


class JarvisUI:
    """Simple Iron Man inspired Tkinter interface."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Jarvis AI Voice Assistant")
        self.root.geometry("760x520")
        self.root.configure(bg="#08090d")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.messages: queue.Queue[str] = queue.Queue()
        self.running = True
        self.active_mode = False

        self._build_widgets()

        self.assistant = JarvisAssistant()
        self.speaker = TurkishSpeaker(self.log)
        self.recognizer = TurkishSpeechRecognizer(self.log)

        self.worker = threading.Thread(target=self._voice_loop, daemon=True)
        self.worker.start()
        self.root.after(100, self._process_messages)
        self._pulse_glow()

    def _build_widgets(self) -> None:
        """Create all visible Tkinter widgets."""
        self.title_label = tk.Label(
            self.root,
            text="JARVIS",
            font=("Segoe UI", 34, "bold"),
            fg="#ff3131",
            bg="#08090d",
        )
        self.title_label.pack(pady=(22, 4))

        self.subtitle_label = tk.Label(
            self.root,
            text="Türkçe Sesli Asistan • Uyandırma kelimesi: Jarvis",
            font=("Segoe UI", 12),
            fg="#ff8a8a",
            bg="#08090d",
        )
        self.subtitle_label.pack(pady=(0, 18))

        self.canvas = tk.Canvas(self.root, width=190, height=190, bg="#08090d", highlightthickness=0)
        self.canvas.pack()
        self.outer_ring = self.canvas.create_oval(20, 20, 170, 170, outline="#7a0000", width=5)
        self.inner_ring = self.canvas.create_oval(48, 48, 142, 142, outline="#ff3131", width=3)
        self.core = self.canvas.create_oval(73, 73, 117, 117, fill="#ff3131", outline="#ffb3b3", width=2)

        self.status_label = tk.Label(
            self.root,
            text="Durum: Jarvis kelimesi bekleniyor...",
            font=("Segoe UI", 13, "bold"),
            fg="#ffffff",
            bg="#08090d",
        )
        self.status_label.pack(pady=16)

        self.log_box = scrolledtext.ScrolledText(
            self.root,
            height=10,
            font=("Consolas", 10),
            fg="#ffd1d1",
            bg="#11131a",
            insertbackground="#ff3131",
            relief="flat",
            wrap=tk.WORD,
        )
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 20))
        self.log_box.insert(tk.END, "Jarvis başlatılıyor...\n")
        self.log_box.configure(state="disabled")

    def log(self, message: str) -> None:
        """Thread-safe log helper."""
        self.messages.put(message)

    def _process_messages(self) -> None:
        """Move queued worker-thread messages into the Tkinter log box."""
        while not self.messages.empty():
            message = self.messages.get()
            self.log_box.configure(state="normal")
            self.log_box.insert(tk.END, message + "\n")
            self.log_box.see(tk.END)
            self.log_box.configure(state="disabled")
        if self.running:
            self.root.after(100, self._process_messages)

    def _set_status(self, text: str, active: bool) -> None:
        """Update status from the worker thread safely."""
        self.active_mode = active
        self.root.after(0, lambda: self.status_label.configure(text=text))

    def _pulse_glow(self) -> None:
        """Animate the red arc-reactor style circles."""
        color = "#ff3131" if self.active_mode else "#7a0000"
        fill = "#ff5a5a" if self.active_mode else "#401010"
        self.canvas.itemconfigure(self.outer_ring, outline=color)
        self.canvas.itemconfigure(self.core, fill=fill)
        if self.running:
            self.root.after(650, self._pulse_glow)

    def _voice_loop(self) -> None:
        """Main wake-word and command listening loop."""
        try:
            self.recognizer.calibrate_microphone()
            self.speaker.say("Jarvis hazır. Beni çağırmak için Jarvis deyin.")
        except Exception as error:  # Keeps UI open and shows setup problems clearly.
            self.log(f"Mikrofon veya ses sistemi başlatılamadı: {error}")
            self._set_status("Durum: Mikrofon veya ses sistemi hatası", False)
            return

        while self.running:
            self._set_status("Durum: Jarvis kelimesi bekleniyor...", False)
            heard = self.recognizer.listen_for_text(timeout=5, phrase_time_limit=4).lower()

            if not heard:
                continue

            self.log(f"Duyulan: {heard}")
            if WAKE_WORD not in heard:
                continue

            self._set_status("Durum: Aktif, komut bekleniyor...", True)
            self.speaker.say("Evet efendim, sizi dinliyorum.")

            keep_active = True
            while self.running and keep_active:
                command = self.recognizer.listen_for_text(timeout=7, phrase_time_limit=8)
                if not command:
                    self.speaker.say("Komut duyamadım efendim.")
                    continue

                self.log(f"Komut: {command}")
                response, keep_active = self.assistant.handle_command(command)
                self.speaker.say(response)

                if any(word in command.lower() for word in ["kapat", "çıkış", "görüşürüz", "programı kapat"]):
                    self.close()
                    return

    def close(self) -> None:
        """Stop the loop and close the Tkinter window."""
        self.running = False
        self.root.after(0, self.root.destroy)

    def run(self) -> None:
        """Start the Tkinter application."""
        self.root.mainloop()


if __name__ == "__main__":
    JarvisUI().run()
