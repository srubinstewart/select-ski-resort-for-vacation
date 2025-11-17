# session.py
"""
A minimal in-memory session service that stores user preferences,
specifically the user's home airport (e.g., DEN, ATL, ORD).
This demonstrates the 'Sessions & State' concept.
"""


class InMemorySessionService:
    """
    Very small session helper to store a user's preferred home airport.
    Keyed by a user_id string.
    """

    def __init__(self):
        self._store = {}

    def set_home_airport(self, user_id: str, airport: str):
        """Store the user's home airport (as a 3-letter code)."""
        airport = airport.upper()
        self._store[user_id] = {"home_airport": airport}

    def get_home_airport(self, user_id: str) -> str | None:
        """Retrieve the stored home airport, if any."""
        data = self._store.get(user_id)
        if not data:
            return None
        return data.get("home_airport")
