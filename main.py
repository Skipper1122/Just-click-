"""Jarvis AI Assistant - futuristic Turkish desktop assistant.

Run this file from the VS Code terminal with:
    python main.py
"""

from __future__ import annotations

import queue
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import scrolledtext
from typing import Callable

from ai_client import AIClient
from assistant import AssistantResult, JarvisAssistant
from launcher import ApplicationLauncher
from memory import MemoryStore
from speech import TurkishSpeaker, TurkishSpeechRecognizer
from weather import WeatherReport, WeatherService


WAKE_WORD = "jarvis"


class JarvisUI:
    """Dark green futuristic Tkinter interface and application controller."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Jarvis AI Desktop Assistant")
        self.root.geometry("1020x680")
        self.root.minsize(900, 600)
        self.root.configure(bg="#020805")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.messages: queue.Queue[tuple[str, str]] = queue.Queue()
        self.ui_tasks: queue.Queue[Callable[[], None]] = queue.Queue()
        self.running = True
        self.active_mode = False
        self.glow_on = False
        self.weather_text = "Hava: yükleniyor..."

        self.memory = MemoryStore()
        self.ai_client = AIClient(self.memory)
        self.launcher = ApplicationLauncher()
        self.assistant = JarvisAssistant(self.memory, self.ai_client, self.launcher)
        self.speaker: TurkishSpeaker | None = None
        self.recognizer: TurkishSpeechRecognizer | None = None
        self.weather_service = WeatherService()

        self._build_widgets()
        self._start_workers()
        self._tick_clock()
        self._pulse_glow()
        self._process_queues()

    def _build_widgets(self) -> None:
        """Create a modern hacker/Jarvis-style layout."""
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.top_bar = tk.Frame(self.root, bg="#03120b", highlightbackground="#00ff88", highlightthickness=1)
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 10))
        self.top_bar.grid_columnconfigure(1, weight=1)

        self.clock_label = tk.Label(
            self.top_bar,
            text="--:--:--",
            font=("Consolas", 24, "bold"),
            fg="#8dffbf",
            bg="#03120b",
        )
        self.clock_label.grid(row=0, column=0, padx=18, pady=14, sticky="w")

        self.title_label = tk.Label(
            self.top_bar,
            text="JARVIS // DESKTOP AI CORE",
            font=("Segoe UI", 18, "bold"),
            fg="#00ff88",
            bg="#03120b",
        )
        self.title_label.grid(row=0, column=1, padx=18)

        self.weather_label = tk.Label(
            self.top_bar,
            text=self.weather_text,
            font=("Segoe UI", 12, "bold"),
            fg="#d7ffe8",
            bg="#03120b",
            justify="right",
        )
        self.weather_label.grid(row=0, column=2, padx=18, pady=14, sticky="e")

        self.main_panel = tk.Frame(self.root, bg="#020805")
        self.main_panel.grid(row=1, column=0, sticky="nsew", padx=18, pady=8)
        self.main_panel.grid_columnconfigure(0, weight=2)
        self.main_panel.grid_columnconfigure(1, weight=1)
        self.main_panel.grid_rowconfigure(0, weight=1)

        self.center_panel = tk.Frame(self.main_panel, bg="#06150d", highlightbackground="#00aa5b", highlightthickness=1)
        self.center_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.center_panel.grid_rowconfigure(2, weight=1)
        self.center_panel.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.center_panel, width=360, height=260, bg="#06150d", highlightthickness=0)
        self.canvas.grid(row=0, column=0, pady=(28, 8))
        self._draw_core()

        self.status_label = tk.Label(
            self.center_panel,
            text="Durum: Jarvis uyandırma kelimesi bekleniyor",
            font=("Segoe UI", 14, "bold"),
            fg="#d7ffe8",
            bg="#06150d",
        )
        self.status_label.grid(row=1, column=0, pady=(0, 12))

        self.log_box = scrolledtext.ScrolledText(
            self.center_panel,
            height=12,
            font=("Consolas", 10),
            fg="#c8ffe1",
            bg="#010503",
            insertbackground="#00ff88",
            relief="flat",
            wrap=tk.WORD,
        )
        self.log_box.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 18))
        self.log_box.insert(tk.END, "[BOOT] Jarvis arayüzü başlatıldı.\n")
        self.log_box.configure(state="disabled")

        self.side_panel = tk.Frame(self.main_panel, bg="#041009", highlightbackground="#007a44", highlightthickness=1)
        self.side_panel.grid(row=0, column=1, sticky="nsew")
        self.side_panel.grid_columnconfigure(0, weight=1)

        self.memory_label = tk.Label(
            self.side_panel,
            text="LOCAL MEMORY",
            font=("Segoe UI", 13, "bold"),
            fg="#00ff88",
            bg="#041009",
        )
        self.memory_label.grid(row=0, column=0, pady=(22, 8))

        self.memory_box = tk.Text(
            self.side_panel,
            height=12,
            font=("Consolas", 9),
            fg="#b9ffd8",
            bg="#010503",
            relief="flat",
            wrap=tk.WORD,
        )
        self.memory_box.grid(row=1, column=0, sticky="ew", padx=14)
        self.memory_box.configure(state="disabled")

        self.commands_label = tk.Label(
            self.side_panel,
            text="QUICK COMMANDS",
            font=("Segoe UI", 13, "bold"),
            fg="#00ff88",
            bg="#041009",
        )
        self.commands_label.grid(row=2, column=0, pady=(22, 8))

        quick_commands = [
            "Jarvis, saat kaç?",
            "Hava durumu nedir?",
            "Tarayıcı aç",
            "Spotify aç",
            "Hesap makinesi aç",
            "Dosya gezgini aç",
            "Beni hatırla, benim adım ...",
            "Uyku moduna geç",
        ]
        self.quick_box = tk.Text(
            self.side_panel,
            height=12,
            font=("Consolas", 9),
            fg="#b9ffd8",
            bg="#010503",
            relief="flat",
            wrap=tk.WORD,
        )
        self.quick_box.grid(row=3, column=0, sticky="nsew", padx=14, pady=(0, 16))
        self.quick_box.insert(tk.END, "\n".join(f"› {command}" for command in quick_commands))
        self.quick_box.configure(state="disabled")

        self._refresh_memory_panel()

    def _draw_core(self) -> None:
        """Draw the central microphone / reactor animation."""
        self.canvas.delete("all")
        self.outer = self.canvas.create_oval(70, 20, 290, 240, outline="#006b3c", width=3)
        self.middle = self.canvas.create_oval(105, 55, 255, 205, outline="#00ff88", width=2)
        self.inner = self.canvas.create_oval(145, 95, 215, 165, fill="#003d22", outline="#8dffbf", width=2)
        self.mic_stem = self.canvas.create_line(180, 118, 180, 158, fill="#d7ffe8", width=5)
        self.mic_head = self.canvas.create_oval(166, 86, 194, 126, outline="#d7ffe8", width=4)
        for x in range(90, 271, 30):
            self.canvas.create_line(x, 130, x + 12, 130, fill="#00aa5b", width=2)

    def _start_workers(self) -> None:
        threading.Thread(target=self._voice_loop, daemon=True).start()
        threading.Thread(target=self._weather_loop, daemon=True).start()

    def log(self, message: str, level: str = "INFO") -> None:
        self.messages.put((level, message))

    def _process_queues(self) -> None:
        while not self.messages.empty():
            level, message = self.messages.get()
            self.log_box.configure(state="normal")
            self.log_box.insert(tk.END, f"[{level}] {message}\n")
            self.log_box.see(tk.END)
            self.log_box.configure(state="disabled")

        while not self.ui_tasks.empty():
            self.ui_tasks.get()()

        if self.running:
            self.root.after(100, self._process_queues)

    def _tick_clock(self) -> None:
        now = datetime.now()
        self.clock_label.configure(text=now.strftime("%H:%M:%S"))
        if self.running:
            self.root.after(1000, self._tick_clock)

    def _pulse_glow(self) -> None:
        self.glow_on = not self.glow_on
        if self.active_mode:
            outer = "#00ff88" if self.glow_on else "#8dffbf"
            fill = "#00aa5b" if self.glow_on else "#006b3c"
        else:
            outer = "#006b3c" if self.glow_on else "#004427"
            fill = "#003d22" if self.glow_on else "#001d11"
        self.canvas.itemconfigure(self.outer, outline=outer)
        self.canvas.itemconfigure(self.inner, fill=fill)
        if self.running:
            self.root.after(550, self._pulse_glow)

    def _set_status(self, text: str, active: bool) -> None:
        self.active_mode = active
        self.ui_tasks.put(lambda: self.status_label.configure(text=text))

    def _set_weather(self, report: WeatherReport) -> None:
        self.assistant.update_weather(report)
        self.weather_text = f"Hava: {report.display_text()} • {report.updated_at}"
        self.ui_tasks.put(lambda: self.weather_label.configure(text=self.weather_text))

    def _refresh_memory_panel(self) -> None:
        summary = self.memory.get_context_summary()
        recent = self.memory.data.get("commands", [])[-5:]
        recent_text = "\n".join(f"{item['action']}: {item['command']}" for item in recent) or "Henüz komut yok."
        text = f"{summary}\n\nSon komutlar:\n{recent_text}"
        self.memory_box.configure(state="normal")
        self.memory_box.delete("1.0", tk.END)
        self.memory_box.insert(tk.END, text)
        self.memory_box.configure(state="disabled")

    def _weather_loop(self) -> None:
        while self.running:
            try:
                report = self.weather_service.fetch()
                self._set_weather(report)
                self.log(f"Hava durumu güncellendi: {report.display_text()}")
            except Exception as error:
                self.ui_tasks.put(lambda error=error: self.weather_label.configure(text=f"Hava: alınamadı ({error})"))
                self.log(f"Hava durumu alınamadı: {error}", "WARN")
            for _ in range(900):
                if not self.running:
                    return
                time.sleep(1)

    def _voice_loop(self) -> None:
        try:
            self.speaker = TurkishSpeaker(self.log)
            self.recognizer = TurkishSpeechRecognizer(self.log)
            self.recognizer.calibrate_microphone()
            self.speaker.say("Jarvis hazır. Beni çağırmak için Jarvis deyin.")
        except Exception as error:
            self.log(f"Mikrofon veya ses sistemi başlatılamadı: {error}", "ERROR")
            self._set_status("Durum: Mikrofon veya ses sistemi hatası", False)
            return

        if self.speaker is None or self.recognizer is None:
            return

        while self.running:
            self._set_status("Durum: Jarvis uyandırma kelimesi bekleniyor", False)
            heard = self.recognizer.listen_for_text(timeout=5, phrase_time_limit=4).lower()
            if not heard:
                continue
            self.log(f"Duyulan: {heard}")
            if WAKE_WORD not in heard:
                continue

            self._set_status("Durum: Aktif konuşma modu", True)
            self.speaker.say("Evet efendim. Sürekli konuşma modu aktif.")

            keep_active = True
            while self.running and keep_active:
                command = self.recognizer.listen_for_text(timeout=9, phrase_time_limit=10)
                if not command:
                    self.speaker.say("Dinliyorum efendim.")
                    continue
                self.log(f"Komut: {command}")
                result = self.assistant.handle_command(command)
                self._handle_result(result)
                keep_active = result.keep_active
                if result.should_exit:
                    self.close()
                    return

    def _handle_result(self, result: AssistantResult) -> None:
        self.log(f"Jarvis: {result.response}")
        self.ui_tasks.put(self._refresh_memory_panel)
        self.speaker.say(result.response)

    def close(self) -> None:
        self.running = False
        self.memory.save()
        self.root.after(0, self.root.destroy)

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    JarvisUI().run()
