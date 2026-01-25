#!/usr/bin/env python3
"""
Process Microsoft Form submissions and update academics_data.json

This script handles both:
1. repository_dispatch events (from Power Automate webhook)
2. workflow_dispatch events (manual testing)
"""

import json
import os
import requests
from typing import Optional

# Nominatim API for geocoding (free, no API key required)
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

def geocode_location(city: str, country: str) -> tuple[Optional[float], Optional[float]]:
    """
    Convert city/country to latitude/longitude using OpenStreetMap Nominatim.
    Returns (lat, lon) or (None, None) if geocoding fails.
    """
    query = f"{city}, {country}"

    try:
        response = requests.get(
            NOMINATIM_URL,
            params={
                "q": query,
                "format": "json",
                "limit": 1
            },
            headers={
                "User-Agent": "BusinessHistoryMap/1.0 (academic-directory)"
            },
            timeout=10
        )
        response.raise_for_status()

        results = response.json()
        if results:
            lat = float(results[0]["lat"])
            lon = float(results[0]["lon"])
            print(f"Geocoded '{query}' to ({lat}, {lon})")
            return lat, lon
        else:
            print(f"No geocoding results for '{query}'")
            return None, None

    except Exception as e:
        print(f"Geocoding error for '{query}': {e}")
        return None, None


def load_data(filepath: str) -> list[dict]:
    """Load existing academics data from JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(filepath: str, data: list[dict]) -> None:
    """Save academics data to JSON file with proper formatting."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} entries to {filepath}")


def find_individual_by_name(data: list[dict], name: str) -> Optional[int]:
    """Find index of an individual entry by name (case-insensitive)."""
    name_lower = name.lower().strip()
    for i, entry in enumerate(data):
        if entry.get("type") == "individual":
            if entry.get("name", "").lower().strip() == name_lower:
                return i
    return None


def add_individual(data: list[dict], name: str, affiliation: str,
                   city: str, country: str, interests: str) -> list[dict]:
    """
    Add a new individual to the dataset.

    - If the person already exists, update their information
    - Geocode the location to get coordinates
    - Update city and country counts
    """
    location = f"{city}, {country}"

    # Check if person already exists
    existing_idx = find_individual_by_name(data, name)

    # Geocode the location
    lat, lon = geocode_location(city, country)

    if lat is None or lon is None:
        print(f"Warning: Could not geocode {location}. Using default coordinates.")
        # Try to find existing coordinates for this city
        for entry in data:
            if entry.get("location", "").lower() == location.lower():
                lat = entry.get("lat", 0)
                lon = entry.get("lon", 0)
                break
        if lat is None:
            lat, lon = 0, 0

    new_entry = {
        "location": location,
        "lat": lat,
        "lon": lon,
        "count": 1,
        "type": "individual",
        "name": name.strip(),
        "affiliation": affiliation.strip(),
        "interests": interests.strip() if interests else ""
    }

    if existing_idx is not None:
        # Update existing entry
        print(f"Updating existing entry for {name}")
        old_location = data[existing_idx].get("location", "")
        data[existing_idx] = new_entry

        # If location changed, update counts
        if old_location.lower() != location.lower():
            data = update_aggregate_counts(data, old_location, -1)
            data = update_aggregate_counts(data, location, 1)
    else:
        # Add new entry
        print(f"Adding new individual: {name}")
        data.append(new_entry)

        # Update aggregate counts
        data = update_aggregate_counts(data, location, 1)

    return data


def withdraw_individual(data: list[dict], name: str) -> list[dict]:
    """
    Remove an individual from the dataset (opt-out).
    Updates aggregate counts accordingly.
    """
    idx = find_individual_by_name(data, name)

    if idx is None:
        print(f"Warning: No individual found with name '{name}'")
        return data

    location = data[idx].get("location", "")
    print(f"Removing individual: {name} from {location}")

    # Remove the entry
    del data[idx]

    # Update aggregate counts
    if location:
        data = update_aggregate_counts(data, location, -1)

    return data


def update_aggregate_counts(data: list[dict], location: str, delta: int) -> list[dict]:
    """
    Update city and country aggregate counts.

    Args:
        data: The full dataset
        location: City, Country format string
        delta: +1 for adding, -1 for removing
    """
    if not location or "," not in location:
        return data

    parts = location.split(",")
    city = parts[0].strip()
    country = parts[-1].strip()

    city_location = f"{city}, {country}"

    # Update city count
    city_found = False
    for entry in data:
        if entry.get("type") == "city" and entry.get("location", "").lower() == city_location.lower():
            entry["count"] = max(0, entry.get("count", 0) + delta)
            city_found = True
            print(f"Updated city count for {city_location}: {entry['count']}")
            break

    # Update country count
    for entry in data:
        if entry.get("type") == "country" and entry.get("location", "").lower() == country.lower():
            entry["count"] = max(0, entry.get("count", 0) + delta)
            print(f"Updated country count for {country}: {entry['count']}")
            break

    return data


def get_submission_data() -> dict:
    """
    Extract submission data from environment variables.
    Handles both repository_dispatch and workflow_dispatch events.
    """
    event_name = os.environ.get("EVENT_NAME", "")

    if event_name == "repository_dispatch":
        # From Power Automate webhook
        payload_str = os.environ.get("DISPATCH_PAYLOAD", "{}")
        try:
            payload = json.loads(payload_str)
            return {
                "action": payload.get("action", "add"),
                "name": payload.get("name", ""),
                "affiliation": payload.get("affiliation", ""),
                "city": payload.get("city", ""),
                "country": payload.get("country", ""),
                "interests": payload.get("interests", "")
            }
        except json.JSONDecodeError as e:
            print(f"Error parsing dispatch payload: {e}")
            return {}
    else:
        # From manual workflow_dispatch
        return {
            "action": os.environ.get("INPUT_ACTION", "add"),
            "name": os.environ.get("INPUT_NAME", ""),
            "affiliation": os.environ.get("INPUT_AFFILIATION", ""),
            "city": os.environ.get("INPUT_CITY", ""),
            "country": os.environ.get("INPUT_COUNTRY", ""),
            "interests": os.environ.get("INPUT_INTERESTS", "")
        }


def main():
    """Main entry point."""
    data_file = "academics_data.json"

    # Get submission data
    submission = get_submission_data()
    print(f"Processing submission: {submission}")

    # Validate required fields
    if not submission.get("name"):
        print("Error: Name is required")
        return

    # Load existing data
    data = load_data(data_file)
    print(f"Loaded {len(data)} existing entries")

    # Process based on action type
    action = submission.get("action", "add").lower()

    if action == "withdraw":
        data = withdraw_individual(data, submission["name"])
    else:
        # Validate required fields for adding
        if not all([submission.get("affiliation"),
                    submission.get("city"),
                    submission.get("country")]):
            print("Error: affiliation, city, and country are required for adding")
            return

        data = add_individual(
            data,
            name=submission["name"],
            affiliation=submission["affiliation"],
            city=submission["city"],
            country=submission["country"],
            interests=submission.get("interests", "")
        )

    # Save updated data
    save_data(data_file, data)
    print("Done!")


if __name__ == "__main__":
    main()
