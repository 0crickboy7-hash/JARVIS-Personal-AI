import re
from pathlib import Path

from jarvis.voice.speech.edge_tts_engine import EdgeTTSVoice


class MultilingualTTSEngine:
    """Select Hindi or English TTS based on the supplied text."""

    DEVANAGARI_PATTERN = re.compile(r"[\u0900-\u097F]")

    def __init__(self):
        print("Initializing Multilingual TTS Engine...")

        self.hindi = EdgeTTSVoice("hi-IN-SwaraNeural")
        self.english = EdgeTTSVoice("en-IN-NeerjaNeural")

        self.voice_name = "Hindi: Swara Female; Indian English: Neerja Female"

        print("English voice:", self.english.voice_name)
        print("Hindi voice:", self.hindi.voice_name)
        print("Multilingual TTS: READY")

    def detect_language(self, text):
        """Detect Hindi script or default to English."""

        if self.DEVANAGARI_PATTERN.search(text):
            return "hi"

        return "en"

    def speak(self, text, language=None):
        """Speak text using the selected voice."""

        if not isinstance(text, str):
            raise TypeError("Speech text must be a string.")

        text = text.strip()
        # MARKDOWN SPEECH CLEANING
        text = re.sub(r"(?m)^[ \t]*#{1,6}[ \t]*", "", text)
        text = re.sub(r"(?<!\w)#(?=\w)", "", text)
        text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        text = re.sub(r"https?://\S+", "", text)
        text = re.sub(r"\*+|_{1,2}|~~|`+", "", text)
        text = re.sub(r"(?m)^[ \t]*[-+][ \t]+", "", text)
        text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
        text = re.sub(r"</?[^>]+>", " ", text)
        text = text.replace("|", " ")
        text = re.sub(r"\s+", " ", text).strip()

        if not text:
            return

        selected_language = (
            language.lower().strip()
            if language
            else self.detect_language(text)
        )

        if selected_language in ("hi", "hindi"):
            print("Selected voice: Hindi - Swara Female")
            self.hindi.speak(text)

        elif selected_language in ("en", "english", "hinglish"):
            print("Selected voice: Indian English - Neerja Female")
            self.english.speak(text)

        else:
            raise ValueError(
                f"Unsupported language: {selected_language}"
            )
