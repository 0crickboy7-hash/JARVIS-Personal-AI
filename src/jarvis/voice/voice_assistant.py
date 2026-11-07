import sys
import time
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Existing JARVIS modules
from jarvis.brain.llm_client import JarvisBrain
from jarvis.agents.agent_router import AgentRouter
from jarvis.voice.speech.microphone import MicrophoneRecorder
from jarvis.voice.recognition.whisper_engine import WhisperEngine
from jarvis.voice.speech.multilingual_tts_engine import MultilingualTTSEngine


class VoiceAssistant:
    """Connect JARVIS microphone, Whisper, AI Brain and TTS."""

    def __init__(
        self,
        recording_duration=7,
        language="en"
    ):
        print("Initializing JARVIS Voice Assistant...")

        self.recording_duration = recording_duration
        self.language = language

        self.recorder = MicrophoneRecorder()
        self.whisper = WhisperEngine()
        self.brain = JarvisBrain()
        self.agent_router = AgentRouter(self.brain)
        self.tts = MultilingualTTSEngine()

        print("Microphone:", self.recorder.device_name)
        print("TTS Voice:", self.tts.voice_name)
        print("JARVIS Voice Assistant: READY")

    def run_once(self, countdown_seconds=3):
        """Listen once, get an AI response and speak it."""

        audio_path = None

        try:
            if countdown_seconds > 0:
                print(f"\nRecording starts in {countdown_seconds} seconds...")
                time.sleep(countdown_seconds)

            print("Listening... Speak now!")

            audio_path = self.recorder.record(
                duration_seconds=self.recording_duration
            )

            print("\nProcessing your voice...")

            result = self.whisper.transcribe(
                audio_path,
                language=self.language
            )

            user_text = result["text"].strip()

            print("\n--- JARVIS VOICE INPUT ---")
            print("Detected Language:", result["language"])
            print("You said:", user_text)

            if not user_text:
                print("No speech recognized.")
                self.tts.speak("Sorry, I could not hear you.")
                return

            print("\nJARVIS AI is thinking...")

            routed_answer = self.agent_router.handle(user_text)
            answer = routed_answer if routed_answer is not None else self.brain.ask(user_text)

            print("\n--- JARVIS AI RESPONSE ---")
            print(answer)

            print("\nJARVIS is speaking...")
            self.tts.speak(answer)

            print("\nVOICE CONVERSATION: SUCCESS")

            return answer

        except Exception as error:
            print("\nVOICE ASSISTANT ERROR:")
            print(type(error).__name__, error)
            raise

        finally:
            if audio_path is not None:
                Path(audio_path).unlink(missing_ok=True)
                print("Temporary audio cleaned up.")


def main():
    assistant = VoiceAssistant(
        recording_duration=7,
        language="en"
    )

    assistant.run_once()


if __name__ == "__main__":
    main()
