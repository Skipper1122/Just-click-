# Jarvis AI Desktop Assistant

A Python-based futuristic desktop AI assistant with a dark green hacker/Jarvis-style interface, Turkish voice interaction, local learning memory, weather display, application launching, and optional Gemini AI integration.

## Features

- Python 3.10+ compatible
- Runs directly in the Visual Studio Code terminal
- Dark green futuristic Tkinter desktop UI
- Always-visible real-time clock
- Live weather panel based on approximate user location
- Wake word detection: **Jarvis**
- Continuous conversation mode after activation
- Turkish speech-to-text with `SpeechRecognition` (`tr-TR`)
- Optional offline speech recognition with a local Vosk Turkish model
- Turkish text-to-speech with `pyttsx3`
- Application launcher for browser, Spotify, calculator, file explorer, notes, YouTube, and web search
- Optional Gemini API integration for advanced AI responses
- Short-term conversation context for current session prompts
- Long-term local memory stored in `data/memory.json`
- Learns repeated commands, app usage patterns, favorite apps, preferences, habits, and saved facts

## Folder structure

```text
.
├── main.py              # Starts the futuristic desktop UI and voice loop
├── assistant.py         # Routes Turkish commands to actions or AI responses
├── speech.py            # Speech recognition and text-to-speech helpers
├── memory.py            # Persistent JSON memory and learning logic
├── launcher.py          # Cross-platform application launcher
├── weather.py           # Public no-key weather/location API integration
├── ai_client.py         # Optional Gemini REST client and local AI fallback
├── requirements.txt     # Python packages
├── data/memory.json     # Created automatically after first run
└── README.md            # Setup and usage guide
```

## Download this project

Choose one option:

### Option A: Download as a ZIP

1. Open the repository page for this project on GitHub.
2. Click **Code**.
3. Click **Download ZIP**.
4. Extract the ZIP file.
5. Open the extracted folder in Visual Studio Code.

### Option B: Clone with Git

If you have Git installed, open a terminal and run:

```bash
git clone <repository-url>
cd <repository-folder>
```

Replace `<repository-url>` with the URL from the GitHub **Code** button.

## Quick start in Visual Studio Code

1. Download or clone the project.
2. Open the project folder in VS Code.
3. Open the VS Code terminal with **Terminal > New Terminal**.
4. Create a virtual environment.
5. Install the packages from `requirements.txt`.
6. Run `python main.py`.
7. Say **"Jarvis"** to activate voice mode.

## Installation in Visual Studio Code

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> **PyAudio note:** if `pip install pyaudio` fails, install PortAudio first.
>
> - Windows: try `pip install pipwin` then `pipwin install pyaudio`, or install a matching PyAudio wheel.
> - macOS: `brew install portaudio` then `pip install pyaudio`.
> - Ubuntu/Debian: `sudo apt install portaudio19-dev python3-pyaudio` then `pip install pyaudio`.

## How to run

Make sure your virtual environment is active, then run:

```bash
python main.py
```

If your system uses `python3` instead of `python`, run:

```bash
python3 main.py
```

You can also press **F5** in VS Code and choose **Run Jarvis AI Voice Assistant** if the Python extension is installed.

## How to use voice mode

1. Run `python main.py`.
2. Wait for Jarvis to say it is ready.
3. Say **"Jarvis"**.
4. Jarvis enters continuous conversation mode.
5. Keep speaking commands without saying the wake word again.
6. Say **"uyku moduna geç"** to return to wake-word mode.
7. Say **"programı kapat"** to close the app.

## Example Turkish commands

- `Jarvis`
- `Saat kaç?`
- `Bugün tarih ne?`
- `Hava durumu nedir?`
- `Tarayıcı aç`
- `Spotify aç`
- `Hesap makinesi aç`
- `Dosya gezgini aç`
- `YouTube aç`
- `Google Python öğrenme araması yap`
- `Beni hatırla, benim adım Ahmet`
- `Hafızanda ne biliyorsun?`
- `Neler yapabilirsin?`
- `Uyku moduna geç`
- `Programı kapat`

## Weather support

Weather is fetched with public no-key APIs:

1. Approximate location is detected from your IP address.
2. Current weather is fetched from Open-Meteo.
3. The top bar updates automatically about every 15 minutes.

No paid weather API key is required.

## Optional Gemini AI setup

Jarvis works without Gemini by using local command rules and a simple local fallback response. For smarter AI answers, create a Gemini API key and set it as an environment variable.

### Windows PowerShell

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
python main.py
```

### macOS / Linux

```bash
export GEMINI_API_KEY="your_api_key_here"
python main.py
```

Optional model override:

```bash
export GEMINI_MODEL="gemini-2.5-flash"
```

The app calls the Gemini REST `generateContent` endpoint with only Python standard-library HTTP tools, so no extra Gemini package is required.

## Local memory system

Jarvis creates this file automatically:

```text
data/memory.json
```

It stores:

- Recent commands
- Frequently used actions
- Application usage counts and last-opened times
- Favorite apps learned from repeated launches
- Preferences such as theme, language, voice rate, habits, and shortcuts
- Short-term conversation entries
- Saved facts, such as your name when you say `Beni hatırla, benim adım ...`

The memory file persists after restart, so Jarvis can learn patterns over time.

## Optional offline Vosk support

The app automatically uses Vosk offline recognition only if both are available:

1. The `vosk` package is installed.
2. A Turkish Vosk model exists at:

```text
models/vosk-tr
```

Download a Turkish model from the official Vosk model list, unzip it, and rename the extracted folder to `models/vosk-tr`.

If the model is not present, the app falls back to SpeechRecognition's free Google recognizer with Turkish language code `tr-TR`.

## Notes

- A working microphone is required for voice commands.
- The first launch may ask your operating system for microphone permission.
- Turkish text-to-speech quality depends on installed system voices.
- System app names differ by operating system, so some launch commands may depend on what is installed.
- Shutdown/restart commands are intentionally not executed automatically for safety.
- The code is modular so you can expand commands in `assistant.py`, app shortcuts in `launcher.py`, memory behavior in `memory.py`, or AI behavior in `ai_client.py`.
