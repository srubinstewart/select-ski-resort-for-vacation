# main.py
"""
Entry point for the Ski Trip Airfare Concierge Agent.

Run this file to interact with the CoordinatorAgent in a simple
command-line loop.
"""

from agents import CoordinatorAgent
from session import InMemorySessionService


def main():
    session_service = InMemorySessionService()
    coordinator = CoordinatorAgent(session_service=session_service)

    # For this simple demo we just use a fixed user id.
    user_id = "demo_user"

    print("Ski Trip Airfare Concierge")
    print("Type 'quit' to exit.")
    print("\nExamples:")
    print("  Set my home airport to DEN")
    print("  Plan a ski trip from Feb 15 to Feb 20")
    print("  Plan a ski trip from Mar 5 to Mar 12 with a $400 budget")

    while True:
        message = input("\nYou: ").strip()
        if message.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        response = coordinator.handle_message(user_id=user_id, message=message)
        print(f"\nAgent:\n{response}")


if __name__ == "__main__":
    main()
