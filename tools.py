# tools.py
"""
Tool definitions for the Ski Trip Airfare Concierge Agent.

For the purposes of this project, get_sample_fares() returns
a small hard-coded list of sample fares for major ski airports.
This keeps the project simple and API-free.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class FlightOption:
    destination: str        # Airport code (e.g., SLC)
    price_usd: int          # Estimated roundtrip fare
    notes: str              # Quick context about the airport or region


def get_sample_fares(origin: str, start_date: str, end_date: str) -> List[FlightOption]:
    """
    Returns a sample list of roundtrip fares from the given origin
    to a handful of popular ski destination airports.

    All prices are intentionally made-up but realistic enough for
    demonstration purposes.
    """

    # You can add or change airports anytime.
    sample_destinations = {
    "SLC": ("Utah resorts: Snowbird, Alta, Park City, Deer Valley", 220),
    "RNO": ("Lake Tahoe resorts: Northstar, Heavenly, Palisades Tahoe", 260),
    "JAC": ("Jackson Hole Mountain Resort", 420),
    "EGE": ("Vail & Beaver Creek", 380),
    "YVR": ("Whistler/Blackcomb (drive from Vancouver)", 310),
    "BZN": ("Big Sky, Montana", 360),
    "MMH": ("Mammoth Mountain, CA", 340),
    "MTJ": ("Telluride Ski Resort (Telluride access via Montrose)", 410),
    "BTV": ("Killington & Stowe, Vermont", 290),
    "PWM": ("Sunday River & Sugarloaf, Maine", 280)
}


    results = []

    for airport, (notes, price) in sample_destinations.items():
        # You could add simple date logic here (weekends more expensive, etc.)
        results.append(
            FlightOption(
                destination=airport,
                price_usd=price,
                notes=notes,
            )
        )

    return results
