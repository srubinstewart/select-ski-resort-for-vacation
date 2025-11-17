# agents.py
"""
Agent definitions for the Ski Trip Airfare Concierge.

This file contains:
- LLMClient (placeholder)
- FlightPriceAgent
- FilterAgent
- CoordinatorAgent
"""

from typing import List, Optional
from tools import get_sample_fares, FlightOption
from session import InMemorySessionService


# -----------------------------------------------------------
# Placeholder LLM Client (can be swapped for Gemini later)
# -----------------------------------------------------------
class LLMClient:
    def generate(self, prompt: str) -> str:
        """
        Placeholder text generation.

        In a real implementation, this would call Gemini to generate
        nicer descriptions or travel tips. For now, we keep it simple.
        """
        return "Placeholder LLM output. Replace with Gemini if desired."


# -----------------------------------------------------------
# FlightPriceAgent
# -----------------------------------------------------------
class FlightPriceAgent:
    """Agent responsible for retrieving or simulating flight prices."""

    def get_fares(self, origin: str, start_date: str, end_date: str) -> List[FlightOption]:
        return get_sample_fares(origin, start_date, end_date)


# -----------------------------------------------------------
# FilterAgent
# -----------------------------------------------------------
class FilterAgent:
    """
    Agent that filters and ranks flight options based on a budget and
    simple heuristics.
    """

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def label_price_band(self, price: int, budget: Optional[int]) -> str:
        """
        Assign a basic label like 'budget-friendly', 'mid-range', 'premium'.
        """
        if budget is not None:
            if price <= budget * 0.8:
                return "budget-friendly"
            elif price <= budget * 1.2:
                return "within budget"
            else:
                return "above budget"
        else:
            # No budget given: use fixed thresholds
            if price <= 250:
                return "budget-friendly"
            elif price <= 400:
                return "mid-range"
            else:
                return "premium"

    def filter_and_sort(
        self,
        flights: List[FlightOption],
        budget: Optional[int] = None,
    ) -> List[dict]:
        """
        Filter and sort flight options, returning a list of simple dicts for display.
        """
        # Basic filtering: if budget given, drop options that are far above budget.
        if budget is not None:
            filtered = [f for f in flights if f.price_usd <= budget * 1.5]
        else:
            filtered = flights

        # Sort by price ascending
        filtered.sort(key=lambda f: f.price_usd)

        results = []
        for f in filtered:
            band = self.label_price_band(f.price_usd, budget)
            results.append(
                {
                    "destination": f.destination,
                    "price_usd": f.price_usd,
                    "label": band,
                    "notes": f.notes,
                }
            )
        return results


# -----------------------------------------------------------
# CoordinatorAgent
# -----------------------------------------------------------
class CoordinatorAgent:
    """
    Top-level agent that interacts with the user, coordinates the
    FlightPriceAgent and FilterAgent, and formats the final answer.
    """

    def __init__(self, session_service: InMemorySessionService):
        self.session = session_service
        self.flight_agent = FlightPriceAgent()
        self.filter_agent = FilterAgent(llm=LLMClient())

    def _parse_budget(self, message_lower: str) -> Optional[int]:
        """
        Very simple budget extractor that looks for a dollar sign and a number.
        Example: 'with a $400 budget' -> 400
        """
        import re

        match = re.search(r"\$?(\d{2,5})", message_lower)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return None
        return None

    def handle_message(self, user_id: str, message: str) -> str:
        message_lower = message.lower()

        # ---- Handle setting the home airport -----------------------------------
        if "set my home airport to" in message_lower:
            parts = message_lower.split("set my home airport to")
            airport = parts[1].strip().upper()
            self.session.set_home_airport(user_id, airport)
            return f"Got it. I will remember your home airport as {airport}."

        # ---- Determine home airport --------------------------------------------
        home_airport = self.session.get_home_airport(user_id)
        if not home_airport:
            # Try to guess a 3-letter airport code in the message
            import re

            code_match = re.search(r"\b([A-Z]{3})\b", message.upper())
            if code_match:
                home_airport = code_match.group(1)
            else:
                return (
                    "I don't know your home airport yet. "
                    "Please say something like: 'Set my home airport to DEN'."
                )

        # ---- Extract very simple dates ------------------------------------------
        # For this demo we will not parse real dates. We'll just echo back
        # what the user wrote. In a more advanced version, we would parse
        # dates explicitly or ask follow-up questions.
        start_date = "your start date"
        end_date = "your end date"

        # ---- Extract optional budget -------------------------------------------
        budget = self._parse_budget(message_lower)

        # ---- Get flight options -------------------------------------------------
        flight_options = self.flight_agent.get_fares(
            origin=home_airport,
            start_date=start_date,
            end_date=end_date,
        )

        # ---- Filter and sort ----------------------------------------------------
        ranked = self.filter_agent.filter_and_sort(flight_options, budget=budget)

        if not ranked:
            return "I couldn't find any ski d
