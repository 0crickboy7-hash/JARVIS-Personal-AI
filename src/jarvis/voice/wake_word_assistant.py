import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from jarvis.voice.wake_word_detector import WakeWordDetector
from jarvis.voice.voice_assistant import VoiceAssistant


def main():
    print("Initializing Wake-Controlled JARVIS...")

    detector = WakeWordDetector(threshold=0.4)

    assistant = VoiceAssistant(
        recording_duration=7,
        language=None
    )

    print("\n================================")
    print("JARVIS WAKE SYSTEM: ONLINE")
    print("Say: HEY JARVIS")
    print("Press CTRL+C to stop.")
    print("================================\n")

    try:
        while True:
            score = detector.listen()

            if score is not None:
                print("\nJARVIS ACTIVATED!")

                try:
                    assistant.run_once(countdown_seconds=0)

                except Exception as error:
                    print("\nConversation error:")
                    print(type(error).__name__, error)

                    print("Returning to wake-word listening...")

    except KeyboardInterrupt:
        print("\nJARVIS shutting down...")
        print("Wake-Controlled Assistant stopped.")


if __name__ == "__main__":
    main()
