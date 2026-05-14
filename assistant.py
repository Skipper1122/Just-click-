"""Command understanding and action routing for Jarvis."""

from __future__ import annotations

import datetime as _dt
import webbrowser
from dataclasses import dataclass

from ai_client import AIClient
from launcher import ApplicationLauncher
from memory import MemoryStore
from weather import WeatherReport


@dataclass
class AssistantResult:
    """Result returned after Jarvis handles a command."""

    response: str
    action: str
    keep_active: bool = True
    should_exit: bool = False


class JarvisAssistant:
    """Turkish, memory-aware command assistant."""

    def __init__(self, memory: MemoryStore, ai_client: AIClient, launcher: ApplicationLauncher) -> None:
        self.memory = memory
        self.ai_client = ai_client
        self.launcher = launcher
        self.latest_weather: WeatherReport | None = None

    def update_weather(self, report: WeatherReport) -> None:
        self.latest_weather = report

    def handle_command(self, command: str) -> AssistantResult:
        """Understand one Turkish command and create a spoken response."""
        text = command.lower().strip()

        if not text:
            return self._remember(command, "empty", "Sizi duyamadım efendim. Lütfen tekrar eder misiniz?")

        if any(word in text for word in ["uyku", "bekle", "dinlen", "sus"]):
            return self._remember(
                command,
                "sleep",
                "Tamam efendim. Uyku moduna geçiyorum. Beni Jarvis diyerek çağırabilirsiniz.",
                keep_active=False,
            )

        if any(word in text for word in ["kapat", "çıkış", "görüşürüz", "programı kapat"]):
            return self._remember(
                command,
                "exit",
                "Görüşürüz efendim. Sistemi kapatıyorum.",
                keep_active=False,
                should_exit=True,
            )

        if "saat" in text:
            now = _dt.datetime.now().strftime("%H:%M")
            return self._remember(command, "time", f"Saat şu anda {now}.")

        if "tarih" in text or "bugün" in text:
            today = _dt.datetime.now().strftime("%d.%m.%Y")
            return self._remember(command, "date", f"Bugünün tarihi {today}.")

        if "hava" in text:
            if self.latest_weather:
                return self._remember(command, "weather", f"Hava durumu: {self.latest_weather.display_text()}.")
            return self._remember(command, "weather", "Hava durumu henüz yüklenmedi efendim.")

        if "merhaba" in text or "selam" in text:
            user_name = self.memory.data.get("facts", {}).get("user_name", "efendim")
            return self._remember(command, "greeting", f"Merhaba {user_name}. Sistemler hazır.")

        if "nasılsın" in text:
            return self._remember(command, "status", "Sistemlerim çalışıyor efendim. Dinleme, hafıza ve arayüz modülleri aktif.")

        if "adın ne" in text or "kimsin" in text:
            return self._remember(command, "identity", "Ben Jarvis. Türkçe konuşan, öğrenen ve uygulama açabilen masaüstü asistanınızım.")

        if "aç" in text or "çalıştır" in text or "başlat" in text:
            success, response, action = self.launcher.open_app(text)
            if success:
                self.memory.remember_app_launch(action.replace("open_", ""))
            return self._remember(command, action, response)

        if "arama yap" in text or "google" in text or "internette ara" in text:
            query = text.replace("arama yap", "").replace("google", "").replace("internette ara", "").strip()
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                return self._remember(command, "web_search", f"Google üzerinde {query} için arama yapıyorum.")
            return self._remember(command, "web_search_empty", "Ne aramamı istersiniz efendim?")

        if "youtube" in text:
            webbrowser.open("https://www.youtube.com")
            self.memory.remember_app_launch("youtube")
            return self._remember(command, "open_youtube", "YouTube'u açıyorum efendim.")

        if "yardım" in text or "neler yapabilirsin" in text:
            return self._remember(
                command,
                "help",
                "Saat, tarih ve hava durumunu söyleyebilirim; tarayıcı, Spotify, hesap makinesi ve dosya gezginini açabilirim; hafızama tercihlerinizi kaydedebilirim.",
            )

        response = self.ai_client.ask(command)
        return self._remember(command, "ai_chat", response)

    def _remember(
        self,
        command: str,
        action: str,
        response: str,
        keep_active: bool = True,
        should_exit: bool = False,
    ) -> AssistantResult:
        self.memory.remember_command(command, action, response)
        return AssistantResult(response=response, action=action, keep_active=keep_active, should_exit=should_exit)
