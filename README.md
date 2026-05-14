# Jarvis AI Voice Assistant

A beginner-friendly Turkish voice assistant project for Visual Studio Code.  It listens for the wake word **"Jarvis"**, speaks Turkish responses with `pyttsx3`, and shows a simple Iron Man inspired Tkinter interface.

## Features

- Python 3.10+ compatible
- Runs directly in the VS Code terminal
- Wake word detection: **Jarvis**
- Turkish speech recognition (`tr-TR`) and Turkish responses
- Turkish text-to-speech where your operating system has a Turkish voice installed
- Continuous command listening after activation
- Tkinter dark red glowing UI
- No paid APIs required
- Optional offline recognition with a local Vosk Turkish model

## Folder structure

```text
.
├── main.py           # Starts the Tkinter UI and voice loop
├── speech.py         # Microphone recognition and text-to-speech helpers
├── assistant.py      # Turkish command responses
├── requirements.txt  # Python packages
└── README.md         # Setup and usage guide
```

## Installation in Visual Studio Code

1. Open this folder in VS Code.
2. Open the VS Code terminal with **Terminal > New Terminal**.
3. Create and activate a virtual environment:

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

## How to run in VS Code terminal

```bash
python main.py
```

If your system uses `python3` instead of `python`, run:

```bash
python3 main.py
```

## How to use

1. Run `python main.py`.
2. Wait for Jarvis to say it is ready.
3. Say **"Jarvis"**.
4. After Jarvis answers, say a Turkish command.

Example commands:

- `Jarvis`
- `Merhaba`
- `Saat kaç?`
- `Bugün tarih ne?`
- `Google Python öğrenme araması yap`
- `YouTube aç`
- `Yardım`
- `Uyku moduna geç`
- `Programı kapat`

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

- A working microphone is required.
- The first launch may ask your operating system for microphone permission.
- Turkish text-to-speech quality depends on the voices installed on your computer. If no Turkish voice is installed, `pyttsx3` uses the default system voice.
- The code is split into small files and heavily commented so you can add your own commands in `assistant.py`.
