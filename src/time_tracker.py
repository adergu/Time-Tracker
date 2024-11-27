import os
import json
import csv
from datetime import datetime
from analytics import compute_analytics
from utils import parse_iso_timestamp, validate_format

# Define the file to store events
EVENTS_FILE = "events.json"

def load_events():
    """
    Load events from the events file.
    Returns:
        list: A list of events.
    """
    # Check if the events file exists. If not, return an empty list.
    if not os.path.exists(EVENTS_FILE):
        return []
    # Open the events file and load its contents as JSON.
    with open(EVENTS_FILE, "r") as file:
        return json.load(file)

def save_events(events):
    """
    Save events to the events file.
    - events (list): The list of events to save.
    """
    # Open the events file and write the list of events to it in JSON format.
    with open(EVENTS_FILE, "w") as file:
        json.dump(events, file, indent=4)

def start_task(task_name):
    """
    Starts tracking a task by logging a 'start' event.
    - task_name (str): The name of the task being started.
    Raises:
        ValueError: If a task is already running.
    """
    # Load existing events from the file.
    events = load_events()
    # If the last event is a "start" event, raise an error because a task is already running.
    if events and events[-1]["event"] == "start":
        raise ValueError("A task is already running. Stop it before starting a new one.")
    
    # Add the new start event to the events list.
    events.append({
        "timestamp": datetime.now().isoformat(),  # Current timestamp in ISO format
        "event": "start",  # The event type
        "activity": task_name,  # The task name being started
    })
    # Save the updated list of events.
    save_events(events)
    # Output confirmation message.
    print(f"Started task: {task_name}")

def stop_task():
    """
    Stops tracking the current task by logging a 'stop' event.
    Raises:
        ValueError: If no task is currently running.
    """
    # Load existing events from the file.
    events = load_events()
    # If no task is running (i.e., no "start" event), raise an error.
    if not events or events[-1]["event"] != "start":
        raise ValueError("No task is currently running.")
    
    # Get the name of the last running task (the one to stop).
    last_task = events[-1]["activity"]
    # Add the stop event for that task to the events list.
    events.append({
        "timestamp": datetime.now().isoformat(),  # Current timestamp in ISO format
        "event": "stop",  # The event type
        "activity": last_task,  # The task name being stopped
    })
    # Save the updated list of events.
    save_events(events)
    # Output confirmation message.
    print(f"Stopped task: {last_task}")

def export_events(format_type, file_name):
    """
    Exports logged events to a file in the specified format.
    - format_type (str): The format for export ('csv' or 'json').
    - file_name (str): The name of the output file.
    Raises:
        ValueError: If the format_type is not supported.
    """
    # Validate the format type to ensure it's either 'csv' or 'json'.
    validate_format(format_type)
    # Load the events from the events file.
    events = load_events()

    # Export the events based on the requested format.
    if format_type == "csv":
        # Write the events to a CSV file.
        with open(file_name, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["timestamp", "event", "activity"])
            writer.writeheader()  # Write the header row
            writer.writerows(events)  # Write the event rows
    elif format_type == "json":
        # Write the events to a JSON file.
        with open(file_name, mode="w") as file:
            json.dump(events, file, indent=4)

    # Output confirmation message indicating where the events were exported.
    print(f"Events exported to {file_name} in {format_type.upper()} format.")

def import_events(format_type, file_name):
    """
    Imports previously exported events from a file.
    - format_type (str): The format of the import file ('csv' or 'json').
    - file_name (str): The name of the file to import.
    Raises:
        ValueError: If the format_type is not supported.
    """
    # Validate the format type to ensure it's either 'csv' or 'json'.
    validate_format(format_type)

    # Import events based on the format type.
    if format_type == "csv":
        # Read events from a CSV file.
        with open(file_name, mode="r") as file:
            reader = csv.DictReader(file)
            imported_events = list(reader)  # Convert the reader to a list of dictionaries
    elif format_type == "json":
        # Read events from a JSON file.
        with open(file_name, mode="r") as file:
            imported_events = json.load(file)

    # Save the imported events to the events file.
    save_events(imported_events)
    # Output confirmation message indicating where the events were imported from.
    print(f"Events imported from {file_name} in {format_type.upper()} format.")

def main():
    """
    Command-line interface for TimeTracker.
    Provides functionality to start/stop tasks, export/import data, and view analytics.
    """
    import sys

    # If there are no command-line arguments, print usage instructions.
    if len(sys.argv) < 2:
        print("Usage: track-it <command> [arguments]")
        return

    # Get the command from the command-line arguments.
    command = sys.argv[1]

    try:
        # Handle different commands passed through the CLI.
        if command == "start":
            # Start a new task with the name provided as arguments.
            task_name = " ".join(sys.argv[2:])
            start_task(task_name)
        elif command == "stop":
            # Stop the current task.
            stop_task()
        elif command == "export":
            # Export events to a file in the specified format (csv/json).
            format_type = sys.argv[2].split("=")[1]
            export_events(format_type, f"events.{format_type}")
        elif command == "import":
            # Import events from a file in the specified format (csv/json).
            format_type = sys.argv[2].split("=")[1]
            import_events(format_type, f"events.{format_type}")
        elif command == "analytics":
            # Compute and display analytics on the logged events.
            events = load_events()
            compute_analytics(events)
        else:
            # If an unknown command is passed, print an error message.
            print(f"Unknown command: {command}")
    except Exception as e:
        # If an error occurs during any of the operations, print the error message.
        print(f"Error: {e}")

# Entry point for the program when executed directly.
if __name__ == "__main__":
    main()