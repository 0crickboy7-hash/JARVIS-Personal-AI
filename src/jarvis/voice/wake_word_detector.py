import time
from math import gcd
from pathlib import Path

import numpy as np
import sounddevice as sd
from scipy.signal import resample_poly
from openwakeword.model import Model


class WakeWordDetector:
    """Offline Hey Jarvis wake-word detector."""

    def __init__(self, threshold=0.5, device=None):
        project_root = Path(__file__).resolve().parents[3]
        model_dir = project_root / "models" / "openwakeword"

        self.model_path = model_dir / "hey_jarvis_v0.1.onnx"
        self.melspec_path = model_dir / "melspectrogram.onnx"
        self.embedding_path = model_dir / "embedding_model.onnx"

        for path in (
            self.model_path,
            self.melspec_path,
            self.embedding_path
        ):
            if not path.is_file():
                raise FileNotFoundError(f"Model file not found: {path}")

        self.threshold = threshold
        self.device = device

        print("Loading Hey Jarvis model...")

        self.model = Model(
            wakeword_models=[str(self.model_path)],
            inference_framework="onnx",
            melspec_model_path=str(self.melspec_path),
            embedding_model_path=str(self.embedding_path)
        )

        device_info = sd.query_devices(device, kind="input")
        self.sample_rate = 16000
        self.device_name = device_info["name"]
        self.block_size = 1280

        print("Wake word:", "Hey Jarvis")
        print("Microphone:", self.device_name)
        print("Wake Word Detector: READY")

    def listen(self, timeout_seconds=None):
        """Listen until Hey Jarvis is detected or timeout occurs."""

        start_time = time.monotonic()
        best_score = 0.0

        print("Listening for Hey Jarvis...")

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            blocksize=self.block_size,
            device=self.device
        ) as stream:

            while True:
                if (
                    timeout_seconds is not None
                    and time.monotonic() - start_time >= timeout_seconds
                ):
                    print("Wake word not detected.")
                    print("Highest score:", round(best_score, 3))
                    return None

                audio, overflowed = stream.read(self.block_size)
                chunk = audio[:, 0].copy()

                prediction = self.model.predict(chunk)
                score = float(
                    prediction.get("hey_jarvis_v0.1", 0.0)
                )

                best_score = max(best_score, score)

                if score >= self.threshold:
                    self.model.reset()

                    print("\nHEY JARVIS DETECTED!")
                    print("Detection score:", round(score, 3))

                    return score


if __name__ == "__main__":
    detector = WakeWordDetector()

    try:
        detector.listen(timeout_seconds=20)

    except KeyboardInterrupt:
        print("\nWake word detector stopped.")
