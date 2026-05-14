"""Optional large-language-model client for Jarvis.

Gemini is used when GEMINI_API_KEY is present. Without a key, Jarvis still works
with a local rule-based fallback so the project remains free to run.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from memory import MemoryStore


class AIClient:
    """Context-aware AI response provider with an offline fallback."""

    def __init__(self, memory: MemoryStore) -> None:
        self.memory = memory
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    def ask(self, user_text: str) -> str:
        """Return a short Turkish response using Gemini or a local fallback."""
        self.memory.remember_conversation("user", user_text)
        if self.enabled:
            response = self._ask_gemini(user_text)
        else:
            response = self._local_response(user_text)
        self.memory.remember_conversation("assistant", response)
        return response

    def _ask_gemini(self, user_text: str) -> str:
        system_prompt = (
            "Sen Jarvis adında Türkçe konuşan kısa, net ve yardımcı bir masaüstü asistansın. "
            "Kullanıcının yerel hafızasından gelen bağlamı dikkate al. "
            "Yanıtları 1-3 cümle tut."
        )
        recent = self.memory.data.get("conversation", [])[-8:]
        history_text = "\n".join(f"{item['role']}: {item['content']}" for item in recent)
        prompt = (
            f"Sistem: {system_prompt}\n"
            f"Yerel hafıza özeti: {self.memory.get_context_summary()}\n"
            f"Son konuşmalar:\n{history_text}\n"
            f"Kullanıcı: {user_text}\nJarvis:"
        )
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                data = json.loads(response.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (urllib.error.URLError, KeyError, IndexError, TimeoutError):
            return self._local_response(user_text)

    def _local_response(self, user_text: str) -> str:
        text = user_text.lower()
        if "beni hatırla" in text or "benim adım" in text:
            name = text.replace("beni hatırla", "").replace("benim adım", "").strip().title()
            if name:
                self.memory.set_fact("user_name", name)
                return f"Memnun oldum {name}. Bunu yerel hafızama kaydettim."
        if "ne biliyorsun" in text or "hafıza" in text:
            return self.memory.get_context_summary()
        if "öner" in text:
            return "Sık kullandığınız uygulamaları ve komutları takip ediyorum. Birkaç kullanım sonrası size daha iyi öneriler sunacağım."
        return "Bu konuda yerel modda kısa bir yanıt verebilirim. Gemini API anahtarı eklerseniz daha gelişmiş cevaplar üretirim."
