import os
import tempfile
import wave
from pathlib import Path

import sounddevice as sd


class MicrophoneRecorder:
    """Record microphone audio and save it as a WAV file."""

    def __init__(self, sample_rate=None, channels=1, device=None):
        self.channels = channels
        self.device = device

        device_info = sd.query_devices(device, kind="input")

        self.device_name = device_info["name"]
        self.sample_rate = (
            int(sample_rate)
            if sample_rate is not None
            else int(device_info["default_samplerate"])
        )

    def record(self, duration_seconds=5, output_path=None):
        """Record audio and return the WAV file path."""

        if duration_seconds <= 0:
            raise ValueError("Recording duration must be positive.")

        frames = int(duration_seconds * self.sample_rate)

        # Use a context-managed stream so the microphone
        # is released before the next wake-word listening cycle.
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
            device=self.device,
            blocksize=0
        ) as stream:
            audio, overflowed = stream.read(frames)

        temporary_file = output_path is None

        if temporary_file:
            fd, file_name = tempfile.mkstemp(
                suffix=".wav",
                prefix="jarvis_"
            )
            os.close(fd)
            audio_path = Path(file_name)
        else:
            audio_path = Path(output_path)
            audio_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with wave.open(str(audio_path), "wb") as wav:
                wav.setnchannels(self.channels)
                wav.setsampwidth(2)
                wav.setframerate(self.sample_rate)
                wav.writeframes(audio.tobytes())

        except Exception:
            if temporary_file:
                audio_path.unlink(missing_ok=True)
            raise

        return str(audio_path)
