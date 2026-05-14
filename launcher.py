"""Cross-platform application launcher for Jarvis commands."""

from __future__ import annotations

import os
import platform
import subprocess
import webbrowser


class ApplicationLauncher:
    """Open common system apps without third-party dependencies."""

    def __init__(self) -> None:
        self.system = platform.system().lower()

    def open_app(self, app_name: str) -> tuple[bool, str, str]:
        """Open a known app and return `(success, user_message, action_name)`."""
        app = app_name.lower().strip()
        try:
            if any(word in app for word in ["browser", "tarayıcı", "chrome", "web"]):
                webbrowser.open("https://www.google.com")
                return True, "Tarayıcıyı açıyorum efendim.", "open_browser"

            if "spotify" in app:
                return self._open_spotify()

            if any(word in app for word in ["hesap", "calculator", "calc", "makine"]):
                return self._open_calculator()

            if any(word in app for word in ["dosya", "file", "explorer", "klasör", "finder"]):
                return self._open_file_explorer()

            if any(word in app for word in ["not", "notepad", "editör", "editor"]):
                return self._open_text_editor()

            return False, "Bu uygulama için hazır bir kısayol bulamadım efendim.", "unknown_app"
        except OSError as error:
            return False, f"Uygulama açılamadı: {error}", "app_error"

    def _open_spotify(self) -> tuple[bool, str, str]:
        if self.system == "windows":
            os.startfile("spotify:")  # type: ignore[attr-defined]
        elif self.system == "darwin":
            subprocess.Popen(["open", "-a", "Spotify"])
        else:
            subprocess.Popen(["spotify"])
        return True, "Spotify'ı açıyorum efendim.", "open_spotify"

    def _open_calculator(self) -> tuple[bool, str, str]:
        if self.system == "windows":
            subprocess.Popen(["calc"])
        elif self.system == "darwin":
            subprocess.Popen(["open", "-a", "Calculator"])
        else:
            for command in (["gnome-calculator"], ["kcalc"], ["qalculate-gtk"], ["xcalc"]):
                try:
                    subprocess.Popen(command)
                    break
                except FileNotFoundError:
                    continue
            else:
                return False, "Linux hesap makinesi uygulaması bulunamadı.", "calculator_not_found"
        return True, "Hesap makinesini açıyorum efendim.", "open_calculator"

    def _open_file_explorer(self) -> tuple[bool, str, str]:
        if self.system == "windows":
            os.startfile(os.path.expanduser("~"))  # type: ignore[attr-defined]
        elif self.system == "darwin":
            subprocess.Popen(["open", os.path.expanduser("~")])
        else:
            subprocess.Popen(["xdg-open", os.path.expanduser("~")])
        return True, "Dosya gezginini açıyorum efendim.", "open_file_explorer"

    def _open_text_editor(self) -> tuple[bool, str, str]:
        if self.system == "windows":
            subprocess.Popen(["notepad"])
        elif self.system == "darwin":
            subprocess.Popen(["open", "-a", "TextEdit"])
        else:
            subprocess.Popen(["xdg-open", os.path.expanduser("~")])
        return True, "Not uygulamasını açıyorum efendim.", "open_notes"

    def shutdown(self, restart: bool = False) -> tuple[bool, str, str]:
        """Prepare system power commands. Disabled by default for safety."""
        action = "restart" if restart else "shutdown"
        return False, f"Güvenlik için {action} komutu otomatik çalıştırılmadı.", action
