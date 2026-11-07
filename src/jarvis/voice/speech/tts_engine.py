import pyttsx3


class TextToSpeechEngine:
    """JARVIS text-to-speech engine for Windows."""

    def __init__(self, voice_index=0, rate=175, volume=1.0):
        self.engine = pyttsx3.init(driverName="sapi5")

        voices = self.engine.getProperty("voices")

        if not voices:
            raise RuntimeError("No Windows TTS voices available.")

        if not 0 <= voice_index < len(voices):
            raise ValueError("Invalid voice index.")

        self.engine.setProperty(
            "voice",
            voices[voice_index].id
        )

        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)

        self.voice_name = voices[voice_index].name

    def speak(self, text):
        """Speak the supplied text."""

        if not isinstance(text, str):
            raise TypeError("Speech text must be a string.")

        text = text.strip()

        if not text:
            return

        self.engine.say(text)
        self.engine.runAndWait()

    def stop(self):
        """Stop current speech."""
        self.engine.stop()
