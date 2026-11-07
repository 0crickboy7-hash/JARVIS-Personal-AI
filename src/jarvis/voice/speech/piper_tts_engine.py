import os
import tempfile
import wave
from pathlib import Path

import winsound
from piper import PiperVoice


class PiperTextToSpeechEngine:
    """Offline Hindi neural voice engine for JARVIS."""

    def __init__(self, model_path=None):
        project_root = Path(__file__).resolve().parents[4]

        if model_path is None:
            model_path = (
                project_root
                / "models"
                / "piper"
                / "hi_IN-pratham-medium.onnx"
            )

        self.model_path = Path(model_path)

        if not self.model_path.is_file():
            raise FileNotFoundError(
                f"Piper Hindi model not found: {self.model_path}"
            )

        print("Loading Piper Hindi voice...")
        self.voice = PiperVoice.load(str(self.model_path))

        self.voice_name = "Piper Hindi Pratham"
        print("Piper Hindi voice: READY")

    def speak(self, text):
        """Generate and play Hindi speech offline."""

        if not isinstance(text, str):
            raise TypeError("Speech text must be a string.")

        text = text.strip()

        if not text:
            return

        fd, audio_path = tempfile.mkstemp(
            suffix=".wav",
            prefix="jarvis_piper_"
        )
        os.close(fd)

        try:
            with wave.open(audio_path, "wb") as wav_file:
                self.voice.synthesize_wav(text, wav_file)

            with wave.open(audio_path, "rb") as wav_file:
                if wav_file.getnframes() == 0:
                    raise RuntimeError("Piper generated empty audio.")

            winsound.PlaySound(
                audio_path,
                winsound.SND_FILENAME
            )

        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)
