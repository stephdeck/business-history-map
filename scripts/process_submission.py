#!/usr/bin/env python3
"""
Process Microsoft Form submissions and update academics_data.json

This script handles both:
1. repository_dispatch events (from Power Automate webhook)
2. workflow_dispatch events (manual testing)

Consent Options:
- option1: Add anonymously (count only, no personal details displayed)
- option2: Add with full details (title, affiliation, interests visible)
- option3: Remove from map only (keep in underlying directory - no map action needed)
- option4: Remove from map and directory completely
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


def get_or_create_city_entry(data: list[dict], city: str, country: str) -> tuple[list[dict], float, float]:
    """
    Find existing city entry or create coordinates for a new location.
    Returns (data, lat, lon).
    """
    location = f"{city}, {country}"

    # Check if city already exists
    for entry in data:
        if entry.get("type") == "city" and entry.get("location", "").lower() == location.lower():
            return data, entry.get("lat", 0), entry.get("lon", 0)

    # Geocode the new location
    lat, lon = geocode_location(city, country)

    if lat is None or lon is None:
        print(f"Warning: Could not geocode {location}. Using default coordinates.")
        lat, lon = 0, 0

    return data, lat, lon


def add_individual_visible(data: list[dict], name: str, title: str, affiliation: str,
                           city: str, country: str, interests: str) -> list[dict]:
    """
    Option 2: Add individual with full details visible on map.
    Shows: name, title, affiliation, research interests.
    """
    location = f"{city}, {country}"

    # Check if person already exists
    existing_idx = find_individual_by_name(data, name)

    # Get coordinates
    data, lat, lon = get_or_create_city_entry(data, city, country)

    # Build affiliation string with title
    full_affiliation = f"{title}, {affiliation}" if title else affiliation

    new_entry = {
        "location": location,
        "lat": lat,
        "lon": lon,
        "count": 1,
        "type": "individual",
        "name": name.strip(),
        "affiliation": full_affiliation.strip(),
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
        print(f"Adding new visible individual: {name}")
        data.append(new_entry)

        # Update aggregate counts
        data = update_aggregate_counts(data, location, 1)

    return data


def add_anonymous(data: list[dict], name: str, city: str, country: str) -> list[dict]:
    """
    Option 1: Add anonymously - only increment city/country counts.
    No individual marker is shown, just contributes to aggregate numbers.

    If person previously had a visible entry, remove it first.
    """
    location = f"{city}, {country}"

    # Check if person already has a visible entry - if so, remove it
    existing_idx = find_individual_by_name(data, name)
    if existing_idx is not None:
        old_location = data[existing_idx].get("location", "")
        print(f"Removing visible entry for {name} (switching to anonymous)")
        del data[existing_idx]
        # Don't decrement counts since they're staying in directory
        if old_location.lower() != location.lower():
            # Location changed - adjust counts
            data = update_aggregate_counts(data, old_location, -1)
            data = update_aggregate_counts(data, location, 1)
    else:
        # New anonymous entry - just increment counts
        print(f"Adding anonymous entry for location: {location}")
        data = update_aggregate_counts(data, location, 1)

    return data


def remove_from_map(data: list[dict], name: str) -> list[dict]:
    """
    Option 4: Remove individual from map completely.
    Removes their visible marker and decrements counts.
    """
    idx = find_individual_by_name(data, name)

    if idx is None:
        print(f"Warning: No visible individual found with name '{name}'")
        return data

    location = data[idx].get("location", "")
    print(f"Removing individual from map: {name} from {location}")

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

    # If city doesn't exist and we're adding, create it
    if not city_found and delta > 0:
        lat, lon = geocode_location(city, country)
        if lat and lon:
            new_city = {
                "location": city_location,
                "lat": lat,
                "lon": lon,
                "count": 1,
                "type": "city"
            }
            data.append(new_city)
            print(f"Created new city entry: {city_location}")

    # Update country count
    country_found = False
    for entry in data:
        if entry.get("type") == "country" and entry.get("location", "").lower() == country.lower():
            entry["count"] = max(0, entry.get("count", 0) + delta)
            country_found = True
            print(f"Updated country count for {country}: {entry['count']}")
            break

    # If country doesn't exist and we're adding, we'd need coordinates
    # For now, just log a warning
    if not country_found and delta > 0:
        print(f"Warning: Country '{country}' not found in data. May need to add manually.")

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
                "consent_option": payload.get("consent_option", ""),
                "first_name": payload.get("first_name", ""),
                "surname": payload.get("surname", ""),
                "title": payload.get("title", ""),
                "affiliation": payload.get("affiliation", ""),
                "department": payload.get("department", ""),
                "city_country": payload.get("city_country", ""),
                "interests": payload.get("interests", ""),
                "email": payload.get("email", "")
            }
        except json.JSONDecodeError as e:
            print(f"Error parsing dispatch payload: {e}")
            return {}
    else:
        # From manual workflow_dispatch
        return {
            "consent_option": os.environ.get("INPUT_CONSENT_OPTION", "option2"),
            "first_name": os.environ.get("INPUT_FIRST_NAME", ""),
            "surname": os.environ.get("INPUT_SURNAME", ""),
            "title": os.environ.get("INPUT_TITLE", ""),
            "affiliation": os.environ.get("INPUT_AFFILIATION", ""),
            "department": os.environ.get("INPUT_DEPARTMENT", ""),
            "city_country": os.environ.get("INPUT_CITY_COUNTRY", ""),
            "interests": os.environ.get("INPUT_INTERESTS", ""),
            "email": os.environ.get("INPUT_EMAIL", "")
        }


def parse_city_country(city_country: str) -> tuple[str, str]:
    """
    Parse 'City and Country' field into separate city and country.
    Expected format: 'City, Country' or 'City Country'
    """
    if "," in city_country:
        parts = city_country.split(",", 1)
        return parts[0].strip(), parts[1].strip()
    else:
        # Try to split on last space (City Name Country)
        parts = city_country.rsplit(" ", 1)
        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()
        return city_country.strip(), ""


def determine_action(consent_option: str) -> str:
    """
    Map consent option text to action code.
    """
    consent_lower = consent_option.lower()

    if "anonymously" in consent_lower or "count only" in consent_lower:
        return "anonymous"  # Option 1
    elif "display" in consent_lower or "title" in consent_lower or "affiliation" in consent_lower:
        return "visible"    # Option 2
    elif "remove" in consent_lower and "directory" in consent_lower:
        return "remove_all" # Option 4
    elif "remove" in consent_lower:
        return "remove_map" # Option 3
    else:
        # Default to visible if unclear
        print(f"Warning: Could not determine action from consent: '{consent_option}'. Defaulting to visible.")
        return "visible"


def main():
    """Main entry point."""
    data_file = "academics_data.json"

    # Get submission data
    submission = get_submission_data()
    print(f"Processing submission: {submission}")

    # Build full name
    first_name = submission.get("first_name", "").strip()
    surname = submission.get("surname", "").strip()
    full_name = f"{first_name} {surname}".strip()

    if not full_name:
        print("Error: Name is required")
        return

    # Parse city and country
    city_country = submission.get("city_country", "")
    city, country = parse_city_country(city_country)

    # Determine action from consent option
    consent_option = submission.get("consent_option", "")
    action = determine_action(consent_option)
    print(f"Consent option: '{consent_option}' -> Action: {action}")

    # Load existing data
    data = load_data(data_file)
    print(f"Loaded {len(data)} existing entries")

    # Process based on action type
    if action == "anonymous":
        # Option 1: Add anonymously (count only)
        if not city or not country:
            print("Error: City and Country required for anonymous add")
            return
        data = add_anonymous(data, full_name, city, country)

    elif action == "visible":
        # Option 2: Add with full details visible
        if not city or not country:
            print("Error: City and Country required")
            return

        # Build affiliation with department
        affiliation = submission.get("affiliation", "")
        department = submission.get("department", "")
        if department and affiliation:
            full_affiliation = f"{department}, {affiliation}"
        else:
            full_affiliation = affiliation or department

        data = add_individual_visible(
            data,
            name=full_name,
            title=submission.get("title", ""),
            affiliation=full_affiliation,
            city=city,
            country=country,
            interests=submission.get("interests", "")
        )

    elif action == "remove_map":
        # Option 3: Remove from map only (keep in directory)
        # This doesn't require map update - just log it
        print(f"Option 3: {full_name} removed from map display only. No map data change needed.")
        data = remove_from_map(data, full_name)

    elif action == "remove_all":
        # Option 4: Remove from map and directory completely
        data = remove_from_map(data, full_name)

    # Save updated data
    save_data(data_file, data)
    print("Done!")


if __name__ == "__main__":
    main()
