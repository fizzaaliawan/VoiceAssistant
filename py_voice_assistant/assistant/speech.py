from __future__ import annotations
import os, queue, threading, sys
from typing import Optional

import pyttsx3

try:
    import speech_recognition as sr
except Exception:
    sr = None

class Speaker:
    def __init__(self, rate: int = 180, volume: float = 1.0, voice_id: Optional[str] = None):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        if voice_id is not None:
            self.engine.setProperty('voice', voice_id)

        # run engine in a worker thread to avoid blocking
        self._q: queue.Queue[str] = queue.Queue()
        self._t = threading.Thread(target=self._loop, daemon=True)
        self._t.start()

    def _loop(self):
        while True:
            text = self._q.get()
            if text is None:
                break
            self.engine.say(text)
            self.engine.runAndWait()

    def say(self, text: str):
        self._q.put(text)

    def close(self):
        self._q.put(None)

class Listener:
    def __init__(self, engine: str = "speech_recognition", language: str = "en-US", vosk_model_path: str = ""):
        self.engine = engine
        self.language = language
        self.vosk_model_path = vosk_model_path
        self._setup()

    def _setup(self):
        if self.engine == "vosk":
            from vosk import Model, KaldiRecognizer  # type: ignore
            import pyaudio
            self._vosk_model = Model(self.vosk_model_path)
            self._rec = KaldiRecognizer(self._vosk_model, 16000)
            self._pa = pyaudio.PyAudio()
            self._stream = self._pa.open(format=pyaudio.paInt16, channels=1, rate=16000,
                                         input=True, frames_per_buffer=8000)
            self._stream.start_stream()
        elif self.engine == "speech_recognition":
            if sr is None:
                raise RuntimeError("speech_recognition not installed")
            self._recog = sr.Recognizer()
            self._mic = sr.Microphone()  # default device
        else:
            raise ValueError("Unknown ASR engine")

    def listen_once(self) -> Optional[str]:
        if self.engine == "vosk":
            import json
            while True:
                data = self._stream.read(4000, exception_on_overflow = False)
                if self._rec.AcceptWaveform(data):
                    res = json.loads(self._rec.Result())
                    text = res.get("text") or ""
                    if text.strip():
                        return text
        else:
            with self._mic as source:
                self._recog.adjust_for_ambient_noise(source, duration=0.5)
                audio = self._recog.listen(source, timeout=None, phrase_time_limit=8)
            try:
                return self._recog.recognize_google(audio, language=self.language)
            except Exception:
                return None

    def close(self):
        if self.engine == "vosk":
            self._stream.stop_stream()
            self._stream.close()
            self._pa.terminate()
