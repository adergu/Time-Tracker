from datetime import datetime
from collections import defaultdict

# Function to parse an ISO 8601 timestamp string into a datetime object.
def parse_iso_timestamp(timestamp_str):
    """
    Parse an ISO 8601 timestamp string into a datetime object.
    - timestamp_str (str): The timestamp string.

    Returns:
        datetime: Parsed datetime object.
    """
    return datetime.fromisoformat(timestamp_str)

# Function to validate the format type for export/import operations (either 'csv' or 'json').
def validate_format(format_type):
    """
    Validate the format type for export/import operations.
    - format_type (str): The format type ('csv' or 'json').

    Raises:
        ValueError: If the format is not supported.
    """
    if format_type not in {"csv", "json"}:
        raise ValueError("Supported formats are 'csv' and 'json'.")

# Function to group a list of events by their respective day, using the event timestamp.
def group_events_by_day(events):
    """
    Group events by their respective day.
    - events (list): List of event dictionaries.

    Returns:
        dict: Dictionary with dates as keys and event lists as values.
    """
    grouped = defaultdict(list)  # Using defaultdict to simplify appending events to days.
    for event in events:
        date = event["timestamp"].date()  # Extract the date portion of the timestamp.
        grouped[date].append(event)  # Group the event under the corresponding date.
    return grouped
# Function to format a duration (in seconds) into a human-readable string (e.g., "1h 5m 30s").
def format_duration(seconds):
    """
    Format a duration in seconds into a human-readable string.
    - seconds (float): Duration in seconds.

    Returns:
        str: Formatted string (e.g., "1h 5m 30s").
    """
    seconds = int(seconds)  # Ensure the duration is an integer.
    hours, seconds = divmod(seconds, 3600)  # Calculate hours and remaining seconds.
    minutes, seconds = divmod(seconds, 60)  # Calculate minutes and remaining seconds.
    parts = []  # List to hold formatted parts of the duration.
    if hours:
        parts.append(f"{hours}h")  # Add hours if present.
    if minutes:
        parts.append(f"{minutes}m")  # Add minutes if present.
    if seconds:
        parts.append(f"{seconds}s")  # Add seconds if present.
    return " ".join(parts)  # Join all parts into a single string.