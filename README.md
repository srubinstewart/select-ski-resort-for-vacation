# Ski Trip Airfare Concierge Agent

A small multi-agent concierge that helps travelers plan ski vacations
by starting from airfare. Given a home airport and dates, it suggests
ski destinations with reasonable flight prices and shows the estimated
roundtrip fares to each.

## 1. Problem

People plan ski trips in different ways. Some start with the resort and
then try to make the airfare work. Others care more about airfare and
want to find good ski destinations that are affordable to fly to on
specific dates.

Today, the "airfare-first" planner has to:

- Check multiple airline or OTA sites.
- Search different ski airports one by one.
- Manually compare prices across destinations.
- Keep notes somewhere about which places look reasonable.

This is slow and error-prone, and it makes it harder to be flexible
about destination when the real constraint is budget and dates.

## 2. Solution

The **Ski Trip Airfare Concierge Agent** focuses on the airfare-first
use case. It:

1. Asks for:
   - Home airport (e.g., DEN, ATL, BOS)
   - Trip dates (start and end)
   - Optional budget per person

2. Uses a **Flight Price Agent** with a `get_sample_fares` tool to get
   estimated roundtrip prices from the home airport to a small set of
   popular ski destination airports (for example: SLC, RNO, JAC, EGE,
   YVR, etc.).

3. Uses a **Filter Agent** to:
   - Filter down to "reasonable" destinations (e.g., under the budget
     or under a default threshold).
   - Sort destinations by price.
   - Tag them with simple labels like "budget-friendly" or "premium".

4. Uses a **Coordinator Agent** to orchestrate the other agents and
   return a short summary list for the user, such as:

> From DEN, for 15–20 Feb, here are ski destinations with reasonable fares:
> - SLC – \$220 roundtrip – Budget-friendly – Access to multiple Utah resorts.
> - RNO (Tahoe) – \$260 roundtrip – Mid-range – Good access to Tahoe resorts.
> - JAC – \$420 roundtrip – Premium – Home to Jackson Hole.

This keeps the scope intentionally small but useful.

## 3. Architecture

Agents:

- **CoordinatorAgent**
  - Entry point for user queries.
  - Parses home airport, dates, and budget.
  - Calls FlightPriceAgent and FilterAgent.
  - Formats the final recommendation list.

- **FlightPriceAgent**
  - Uses the `get_sample_fares` tool.
  - Returns a list of `(destination_airport, price, notes)` for the
    configured ski destinations.
  - For this project, fares are simulated/hard-coded so the agent can
    run without external APIs.

- **FilterAgent**
  - Takes the full fare list plus optional budget.
  - Filters out clearly too-expensive options.
  - Sorts by price.
  - Adds simple labels like "budget-friendly" or "premium".

Key concepts demonstrated:

1. **Multi-agent system**
   - CoordinatorAgent, FlightPriceAgent, FilterAgent.

2. **Tools**
   - `get_sample_fares(origin, start_date, end_date)` returns a list of
     sample fares.

3. **Sessions and state**
   - A simple in-memory session service can remember the user's
     preferred home airport so they do not have to repeat it every time.

## 4. Files (planned)

- `main.py`  
  Command-line entry point. Reads user input and passes it to the CoordinatorAgent.

- `agents.py`  
  Definitions of CoordinatorAgent, FlightPriceAgent, FilterAgent and a
  placeholder LLM client.

- `tools.py`  
  Implementation of `get_sample_fares` and a small `FlightOption`
  dataclass for structured fares.

- `session.py`  
  Minimal in-memory session helper to remember the home airport per user.

## 5. How to run (once implemented)

1. Install dependencies (for example):

   ```bash
   pip install -r requirements.txt
