# fleet_utils.py
# Catch-all helpers since 2013.
# Dead functions removed 2024; only what is actually called remains.

KM_TO_MILES = 0.621371          # 1 km in miles


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles."""
    return km * KM_TO_MILES


def format_number(value: float) -> str:
    """Format a number to one decimal place."""
    return f"{value:.1f}"
