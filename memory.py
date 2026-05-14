"""Persistent local memory for the Jarvis desktop assistant.

The memory file is intentionally simple JSON so beginners can open it, read it,
and understand exactly what Jarvis is learning between restarts.
"""

from __future__ import annotations

import json
import threading
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


class MemoryStore:
    """Fast, lightweight JSON memory with automatic persistence."""

    def __init__(self, path: str = "data/memory.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self.data: dict[str, Any] = self._load()

    def _default_data(self) -> dict[str, Any]:
        return {
            "commands": [],
            "action_counts": {},
            "app_usage": {},
            "preferences": {
                "theme": "dark_green",
                "language": "tr-TR",
                "voice_rate": 165,
                "favorite_apps": [],
                "habits": [],
                "shortcuts": {},
            },
            "conversation": [],
            "facts": {},
        }

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return self._default_data()

        try:
            loaded = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            backup = self.path.with_suffix(".broken.json")
            self.path.replace(backup)
            return self._default_data()

        defaults = self._default_data()
        for key, value in defaults.items():
            loaded.setdefault(key, value)
        loaded.setdefault("preferences", {}).update(
            {key: loaded.get("preferences", {}).get(key, value) for key, value in defaults["preferences"].items()}
        )
        return loaded

    def save(self) -> None:
        """Write the current memory to disk atomically enough for this app."""
        with self._lock:
            self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")

    def remember_command(self, command: str, action: str, response: str) -> None:
        """Store command history and update repeated-action counters."""
        entry = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "command": command,
            "action": action,
            "response": response,
        }
        self.data["commands"].append(entry)
        self.data["commands"] = self.data["commands"][-250:]
        self.data["action_counts"][action] = self.data["action_counts"].get(action, 0) + 1
        self._learn_from_repetition(action)
        self.save()

    def remember_app_launch(self, app_name: str) -> None:
        """Track application usage patterns."""
        app = app_name.lower()
        usage = self.data["app_usage"].setdefault(app, {"count": 0, "last_opened": None})
        usage["count"] += 1
        usage["last_opened"] = datetime.now().isoformat(timespec="seconds")
        self._update_favorite_apps()
        self.save()

    def remember_conversation(self, role: str, content: str) -> None:
        """Keep short-term conversation context for the current and next prompts."""
        self.data["conversation"].append(
            {"time": datetime.now().isoformat(timespec="seconds"), "role": role, "content": content}
        )
        self.data["conversation"] = self.data["conversation"][-20:]
        self.save()

    def set_preference(self, key: str, value: Any) -> None:
        self.data["preferences"][key] = value
        self.save()

    def set_fact(self, key: str, value: str) -> None:
        self.data["facts"][key] = value
        self.save()

    def get_context_summary(self) -> str:
        """Create a compact summary for AI prompts and UI debugging."""
        prefs = self.data.get("preferences", {})
        favorite_apps = ", ".join(prefs.get("favorite_apps", [])) or "henüz yok"
        top_actions = Counter(self.data.get("action_counts", {})).most_common(5)
        action_text = ", ".join(f"{name}:{count}" for name, count in top_actions) or "henüz yok"
        facts = self.data.get("facts", {})
        fact_text = ", ".join(f"{key}={value}" for key, value in facts.items()) or "henüz yok"
        return f"Favori uygulamalar: {favorite_apps}. Sık eylemler: {action_text}. Bilinen bilgiler: {fact_text}."

    def _update_favorite_apps(self) -> None:
        usage = self.data.get("app_usage", {})
        ranked = sorted(usage.items(), key=lambda item: item[1].get("count", 0), reverse=True)
        self.data["preferences"]["favorite_apps"] = [name for name, _ in ranked[:5]]

    def _learn_from_repetition(self, action: str) -> None:
        count = self.data["action_counts"].get(action, 0)
        habits = self.data["preferences"].setdefault("habits", [])
        habit = f"{action} komutu sık kullanılıyor"
        if count >= 3 and habit not in habits:
            habits.append(habit)
