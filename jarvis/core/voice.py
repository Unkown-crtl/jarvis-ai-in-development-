"""
Voice Control Module — speech recognition (mic → text) + TTS (text → speech)

Backends:
  STT: SpeechRecognition (Google free API) — fallback: vosk (offline)
  TTS: pyttsx3 (offline, fast) — fallback: gTTS (online, better quality)

Install:
    pip install SpeechRecognition pyttsx3 pyaudio
    (optional online TTS): pip install gTTS playsound
"""
import threading
import queue
import os


# ─── TTS ────────────────────────────────────────────────────────────────────

class TTSEngine:
    def __init__(self):
        self._engine = None
        self._lock = threading.Lock()
        self._queue: queue.Queue = queue.Queue()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()
        self._init_engine()

    def _init_engine(self):
        try:
            import pyttsx3
            self._engine = pyttsx3.init()
            # Make voice deeper/clearer — Jarvis feel
            voices = self._engine.getProperty("voices")
            # Prefer a male voice if available
            for v in voices:
                if "male" in v.name.lower() or "david" in v.name.lower() or "alex" in v.name.lower():
                    self._engine.setProperty("voice", v.id)
                    break
            self._engine.setProperty("rate", 165)    # slightly slower = clearer
            self._engine.setProperty("volume", 1.0)
            self._backend = "pyttsx3"
        except Exception as e:
            self._backend = "none"
            print(f"[TTS] pyttsx3 unavailable: {e}")

    def speak(self, text: str):
        """Queue text for speaking (non-blocking)."""
        # Strip markdown / action blocks
        import re
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        text = re.sub(r"[*_`#>]", "", text)
        text = text.strip()
        if text:
            self._queue.put(text)

    def _worker(self):
        while True:
            text = self._queue.get()
            if text is None:
                break
            self._say(text)
            self._queue.task_done()

    def _say(self, text: str):
        if self._backend == "pyttsx3" and self._engine:
            with self._lock:
                try:
                    self._engine.say(text)
                    self._engine.runAndWait()
                except Exception as e:
                    print(f"[TTS] Error: {e}")
        elif self._backend == "gtts":
            self._gtts_say(text)

    def _gtts_say(self, text: str):
        try:
            from gtts import gTTS
            import tempfile, subprocess
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                path = f.name
            gTTS(text=text, lang="en").save(path)
            # Play cross-platform
            import platform
            sys = platform.system()
            if sys == "Darwin":
                subprocess.call(["afplay", path])
            elif sys == "Linux":
                subprocess.call(["mpg123", "-q", path])
            else:
                from playsound import playsound
                playsound(path)
            os.unlink(path)
        except Exception as e:
            print(f"[TTS/gTTS] {e}")

    def stop(self):
        self._queue.put(None)

    @property
    def available(self):
        return self._backend != "none"


# ─── STT ────────────────────────────────────────────────────────────────────

class STTEngine:
    def __init__(self):
        self._backend = "none"
        self._recognizer = None
        self._init()

    def _init(self):
        try:
            import speech_recognition as sr
            self._recognizer = sr.Recognizer()
            self._recognizer.energy_threshold = 300
            self._recognizer.dynamic_energy_threshold = True
            self._recognizer.pause_threshold = 0.8
            self._backend = "google"
        except ImportError:
            print("[STT] SpeechRecognition not installed: pip install SpeechRecognition pyaudio")

    def listen(self, timeout: float = 5.0, phrase_limit: float = 12.0) -> str | None:
        """Block until speech captured; return transcribed text or None."""
        if self._backend == "none":
            return None
        try:
            import speech_recognition as sr
            with sr.Microphone() as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = self._recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
            # Try Google first (online)
            try:
                return self._recognizer.recognize_google(audio)
            except Exception:
                pass
            # Fallback: Sphinx (offline, less accurate)
            try:
                return self._recognizer.recognize_sphinx(audio)
            except Exception:
                return None
        except Exception as e:
            print(f"[STT] {e}")
            return None

    @property
    def available(self):
        return self._backend != "none"


# ─── Combined VoiceController ────────────────────────────────────────────────

class VoiceController:
    def __init__(self):
        self.tts = TTSEngine()
        self.stt = STTEngine()
        self.active = False
        self._listen_thread: threading.Thread | None = None
        self._callback = None        # fn(text: str) called on each utterance
        self._status_cb = None       # fn(status: str)

    def start_listening(self, on_speech=None, on_status=None):
        """Start continuous listen loop in background."""
        self._callback = on_speech
        self._status_cb = on_status
        self.active = True
        self._listen_thread = threading.Thread(target=self._loop, daemon=True)
        self._listen_thread.start()

    def stop_listening(self):
        self.active = False

    def _loop(self):
        while self.active:
            if self._status_cb:
                self._status_cb("listening")
            text = self.stt.listen(timeout=4.0)
            if text:
                if self._status_cb:
                    self._status_cb("processing")
                if self._callback:
                    self._callback(text)
            else:
                if self._status_cb:
                    self._status_cb("idle")

    def say(self, text: str):
        self.tts.speak(text)

    @property
    def stt_available(self):
        return self.stt.available

    @property
    def tts_available(self):
        return self.tts.available
