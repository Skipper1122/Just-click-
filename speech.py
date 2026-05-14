"""Speech recognition and text-to-speech helpers for Jarvis.

The project uses only beginner-friendly libraries requested in the task:
`speechrecognition`, `pyttsx3`, `pyaudio`, `tkinter`, and optional `vosk`.
"""

from __future__ import annotations

import importlib
import importlib.util
import json
from pathlib import Path
from typing import Callable

import pyttsx3
import speech_recognition as sr


LogCallback = Callable[[str], None]


class TurkishSpeaker:
    """Text-to-speech wrapper using pyttsx3."""

    def __init__(self, log: LogCallback | None = None) -> None:
        self.log = log or (lambda message: None)
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 165)
        self.engine.setProperty("volume", 1.0)
        self._select_turkish_voice()

    def _select_turkish_voice(self) -> None:
        """Try to select a Turkish voice if the operating system has one."""
        voices = self.engine.getProperty("voices")
        turkish_keywords = ("tr", "turkish", "türk", "turk")

        for voice in voices:
            voice_text = f"{voice.id} {voice.name}".lower()
            languages = " ".join(str(language).lower() for language in getattr(voice, "languages", []))
            if any(keyword in voice_text or keyword in languages for keyword in turkish_keywords):
                self.engine.setProperty("voice", voice.id)
                self.log(f"Türkçe ses seçildi: {voice.name}")
                return

        self.log("Türkçe sistem sesi bulunamadı. Varsayılan pyttsx3 sesi kullanılacak.")

    def say(self, text: str) -> None:
        """Speak the given text out loud."""
        self.log(f"Jarvis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()


class TurkishSpeechRecognizer:
    """Microphone speech recognition with Turkish language support.

    If a local Vosk Turkish model exists in `models/vosk-tr`, offline speech
    recognition is used. Otherwise, SpeechRecognition's free Google recognizer
    is used with `language="tr-TR"`.
    """

    def __init__(self, log: LogCallback | None = None, model_path: str = "models/vosk-tr") -> None:
        self.log = log or (lambda message: None)
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.model_path = Path(model_path)
        self.use_vosk = self._vosk_is_ready()

    def _vosk_is_ready(self) -> bool:
        """Check optional offline Vosk support without breaking imports."""
        vosk_package_found = importlib.util.find_spec("vosk") is not None
        model_found = self.model_path.exists()

        if vosk_package_found and model_found:
            self.log(f"Offline Vosk modu hazır: {self.model_path}")
            return True

        self.log("Offline Vosk modeli bulunamadı. Çevrim içi ücretsiz Google tanıma kullanılacak.")
        return False

    def calibrate_microphone(self) -> None:
        """Measure room noise once so recognition works better."""
        with sr.Microphone() as source:
            self.log("Mikrofon ortam sesine göre ayarlanıyor...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.log("Mikrofon hazır.")

    def listen_for_text(self, timeout: int = 5, phrase_time_limit: int = 7) -> str:
        """Listen once and return recognized Turkish text.

        Common microphone/recognition errors are handled here so the main
        application loop can keep running instead of crashing.
        """
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return ""

        try:
            if self.use_vosk:
                return self._recognize_with_vosk(audio)
            return self.recognizer.recognize_google(audio, language="tr-TR")
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as error:
            self.log(f"Konuşma tanıma servisine ulaşılamadı: {error}")
            return ""

    def _recognize_with_vosk(self, audio: sr.AudioData) -> str:
        """Recognize speech with a local Vosk Turkish model."""
        # Importing here keeps Vosk optional. The package is only loaded when
        # both the library and the local model folder are available.
        vosk = importlib.import_module("vosk")
        model = vosk.Model(str(self.model_path))
        recognizer = vosk.KaldiRecognizer(model, audio.sample_rate)
        recognizer.AcceptWaveform(audio.get_raw_data(convert_rate=audio.sample_rate, convert_width=2))
        result = json.loads(recognizer.Result())
        return result.get("text", "")
