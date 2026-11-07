import asyncio
import tempfile
from pathlib import Path

import edge_tts
import pygame


class EdgeTTSVoice:
    """Online neural TTS voice with synchronous audio playback."""

    def __init__(self, voice, rate="+0%", volume="+0%"):
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.voice_name = voice

    async def _generate(self, text, audio_path):
        communicator = edge_tts.Communicate(
            text,
            self.voice,
            rate=self.rate,
            volume=self.volume
        )
        await communicator.save(str(audio_path))

    def speak(self, text):
        if not isinstance(text, str):
            raise TypeError("Speech text must be a string.")

        text = text.strip()
        if not text:
            return

        with tempfile.NamedTemporaryFile(
            suffix=".mp3", delete=False
        ) as temp:
            audio_path = Path(temp.name)

        try:
            asyncio.run(self._generate(text, audio_path))

            if not pygame.mixer.get_init():
                pygame.mixer.init()

            pygame.mixer.music.load(str(audio_path))
            pygame.mixer.music.play()

            clock = pygame.time.Clock()
            while pygame.mixer.music.get_busy():
                clock.tick(20)

        finally:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                pygame.mixer.quit()

            audio_path.unlink(missing_ok=True)

    def stop(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
