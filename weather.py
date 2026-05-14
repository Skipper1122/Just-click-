"""Location-aware weather service using public, no-key APIs."""

from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass
from datetime import datetime


@dataclass
class WeatherReport:
    city: str
    country: str
    temperature: float
    wind_speed: float
    condition: str
    updated_at: str

    def display_text(self) -> str:
        return f"{self.city}: {self.temperature:.0f}°C, {self.condition}, rüzgar {self.wind_speed:.0f} km/s"


class WeatherService:
    """Fetch approximate user-location weather without paid APIs."""

    WEATHER_CODES = {
        0: "açık",
        1: "çoğunlukla açık",
        2: "parçalı bulutlu",
        3: "bulutlu",
        45: "sisli",
        48: "kırağılı sis",
        51: "hafif çisenti",
        53: "çisenti",
        55: "yoğun çisenti",
        61: "hafif yağmur",
        63: "yağmur",
        65: "şiddetli yağmur",
        71: "hafif kar",
        73: "kar",
        75: "yoğun kar",
        80: "hafif sağanak",
        81: "sağanak",
        82: "şiddetli sağanak",
        95: "fırtına",
    }

    def fetch(self) -> WeatherReport:
        location = self._get_location()
        weather = self._get_weather(location["lat"], location["lon"])
        current = weather["current_weather"]
        code = int(current.get("weathercode", -1))
        return WeatherReport(
            city=location.get("city") or "Konum",
            country=location.get("country") or "",
            temperature=float(current.get("temperature", 0)),
            wind_speed=float(current.get("windspeed", 0)),
            condition=self.WEATHER_CODES.get(code, "bilinmeyen hava"),
            updated_at=datetime.now().strftime("%H:%M"),
        )

    def _get_location(self) -> dict[str, float | str]:
        with urllib.request.urlopen("http://ip-api.com/json/", timeout=8) as response:
            data = json.loads(response.read().decode("utf-8"))
        if data.get("status") != "success":
            raise RuntimeError("Konum bilgisi alınamadı")
        return {
            "lat": float(data["lat"]),
            "lon": float(data["lon"]),
            "city": data.get("city", "Konum"),
            "country": data.get("country", ""),
        }

    def _get_weather(self, lat: float, lon: float) -> dict[str, object]:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto"
        )
        with urllib.request.urlopen(url, timeout=8) as response:
            return json.loads(response.read().decode("utf-8"))
