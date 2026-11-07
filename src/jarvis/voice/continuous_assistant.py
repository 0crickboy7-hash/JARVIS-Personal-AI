import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from jarvis.voice.voice_assistant import VoiceAssistant


def main():
    assistant = VoiceAssistant(
        recording_duration=7,
        language=None
    )

    assistant.tts.speak(
        "JARVIS is online. You can start speaking. "
        "Press Control C to stop."
    )

    try:
        while True:
            try:
                assistant.run_once()

            except KeyboardInterrupt:
                raise

            except Exception as error:
                print("\nConversation error:", error)
                assistant.tts.speak(
                    "Sorry, something went wrong. Please try again."
                )
                time.sleep(2)

    except KeyboardInterrupt:
        print("\nJARVIS shutting down...")
        assistant.tts.speak("Goodbye. JARVIS is shutting down.")


if __name__ == "__main__":
    main()
