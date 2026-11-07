"""
JARVIS AI Brain
FreeLLMAPI + SQLite Permanent Memory
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Import permanent memory
from jarvis.memory.memory_store import MemoryStore

# Load private configuration
load_dotenv(PROJECT_ROOT / ".env")


class JarvisBrain:

    def __init__(self):

        api_key = os.getenv("JARVIS_LLM_API_KEY")
        base_url = os.getenv("JARVIS_LLM_BASE_URL")

        if not api_key or not base_url:
            raise RuntimeError(
                "API configuration missing. Check .env file."
            )

        self.model = os.getenv(
            "JARVIS_LLM_MODEL"
        ) or "auto"

        self.conversation_id = os.getenv(
            "JARVIS_CONVERSATION_ID",
            "main"
        )

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=60.0,
            max_retries=1,
        )

        # Connect permanent memory
        self.memory = MemoryStore()

        self.history = [
            {
                "role": "system",
                "content": (
                    "You are JARVIS, a helpful personal AI assistant. "
                    "Speak naturally and intelligently. "
                    "Understand Hindi, English and Hinglish. "
                    "Reply in the language used by the user. "
                    "Remember relevant information from the "
                    "conversation context provided to you."
                ),
            }
        ]

        # Restore previous conversation
        saved_messages = self.memory.load_messages(
            self.conversation_id,
            limit=20
        )

        for item in saved_messages:
            self.history.append({
                "role": item["role"],
                "content": item["content"],
            })

        self.loaded_message_count = len(saved_messages)

    def ask(self, message: str) -> str:

        if not message or not message.strip():
            raise ValueError("Message cannot be empty.")

        user_message = message.strip()

        request_history = self.history + [
            {
                "role": "user",
                "content": user_message,
            }
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=request_history,
        )

        answer = response.choices[0].message.content

        if not answer:
            raise RuntimeError("AI returned an empty response.")

        # Save successful conversation permanently
        self.memory.save_message(
            self.conversation_id,
            "user",
            user_message
        )

        self.memory.save_message(
            self.conversation_id,
            "assistant",
            answer
        )

        self.history.extend([
            {
                "role": "user",
                "content": user_message,
            },
            {
                "role": "assistant",
                "content": answer,
            },
        ])

        # Keep recent context within limits
        if len(self.history) > 21:
            self.history = [
                self.history[0]
            ] + self.history[-20:]

        return answer


def main():

    print("\n================================")
    print("       JARVIS AI BRAIN")
    print("================================")

    try:
        jarvis = JarvisBrain()

        print("Status: Online")
        print(f"Model: {jarvis.model}")
        print(
            "Previous messages restored:",
            jarvis.loaded_message_count
        )

        print("Type 'exit' to stop.\n")

    except Exception as error:
        print(f"Startup Error: {error}")
        return

    while True:

        try:
            user_message = input("YOU: ").strip()

            if user_message.lower() in (
                "exit",
                "quit",
                "stop"
            ):
                print("JARVIS: Goodbye!")
                break

            if not user_message:
                continue

            answer = jarvis.ask(user_message)

            print(f"\nJARVIS: {answer}\n")

        except KeyboardInterrupt:
            print("\nJARVIS: Session stopped.")
            break

        except Exception as error:
            print(f"\nJARVIS Error: {error}\n")


if __name__ == "__main__":
    main()