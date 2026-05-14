"""Command handling for the Jarvis AI Voice Assistant.

This file keeps the assistant's "brain" separate from the microphone,
speaker, and user interface code.  The responses are intentionally simple so
beginners can add new Turkish commands easily.
"""

from __future__ import annotations

import datetime as _dt
import webbrowser


class JarvisAssistant:
    """Small Turkish command assistant.

    The `handle_command` method returns the text Jarvis should say.  It also
    returns a boolean that tells the main loop whether Jarvis should keep
    listening for commands (`True`) or go back to wake-word mode (`False`).
    """

    def __init__(self) -> None:
        self.name = "Jarvis"

    def handle_command(self, command: str) -> tuple[str, bool]:
        """Understand one Turkish command and create a spoken response.

        Args:
            command: Text recognized from the user's microphone.

        Returns:
            A tuple of `(response_text, keep_active)`.
        """
        text = command.lower().strip()

        if not text:
            return "Sizi duyamadım efendim. Lütfen tekrar eder misiniz?", True

        # Words that stop command mode but keep the program open.
        if any(word in text for word in ["uyku", "bekle", "dinlen", "sus"]):
            return "Tamam efendim. Uyku moduna geçiyorum. Beni Jarvis diyerek çağırabilirsiniz.", False

        # Words that close the whole application.
        if any(word in text for word in ["kapat", "çıkış", "görüşürüz", "programı kapat"]):
            return "Görüşürüz efendim. Sistemi kapatıyorum.", False

        if "saat" in text:
            now = _dt.datetime.now().strftime("%H:%M")
            return f"Saat şu anda {now}.", True

        if "tarih" in text or "bugün" in text:
            today = _dt.datetime.now().strftime("%d.%m.%Y")
            return f"Bugünün tarihi {today}.", True

        if "merhaba" in text or "selam" in text:
            return "Merhaba efendim. Size nasıl yardımcı olabilirim?", True

        if "nasılsın" in text:
            return "Sistemlerim çalışıyor efendim. Yardıma hazırım.", True

        if "adın ne" in text or "kimsin" in text:
            return "Ben Jarvis. Türkçe konuşabilen basit bir yapay zekâ ses asistanıyım.", True

        if "arama yap" in text or "google" in text:
            query = text.replace("arama yap", "").replace("google", "").strip()
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                return f"Google üzerinde {query} için arama yapıyorum.", True
            return "Ne aramamı istersiniz efendim?", True

        if "youtube" in text:
            webbrowser.open("https://www.youtube.com")
            return "YouTube'u açıyorum efendim.", True

        if "yardım" in text or "neler yapabilirsin" in text:
            return (
                "Saat söyleyebilirim, tarihi söyleyebilirim, Google araması yapabilirim, "
                "YouTube'u açabilirim ve uyku moduna geçebilirim."
            ), True

        return "Bu komutu henüz bilmiyorum efendim. Yardım derseniz örnek komutları söyleyebilirim.", True
