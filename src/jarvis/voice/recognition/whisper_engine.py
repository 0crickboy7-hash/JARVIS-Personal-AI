from pathlib import Path
from faster_whisper import WhisperModel


class WhisperEngine:
    """JARVIS multilingual speech-to-text engine."""

    def __init__(
        self,
        model_size="small",
        device="cpu",
        compute_type="int8",
        beam_size=5
    ):
        self.beam_size = beam_size

        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )

    def transcribe(self, audio_path, language=None):
        """Convert an audio file into text."""

        audio_file = Path(audio_path)

        if not audio_file.is_file():
            raise FileNotFoundError(
                f"Audio file not found: {audio_file}"
            )

        segments, info = self.model.transcribe(
            str(audio_file),
            language=language,
            beam_size=self.beam_size
        )

        recognized_text = " ".join(
            segment.text.strip() for segment in segments
        ).strip()

        return {
            "text": recognized_text,
            "language": info.language,
            "language_probability": info.language_probability
        }
