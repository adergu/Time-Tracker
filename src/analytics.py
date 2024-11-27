from datetime import datetime, timedelta
from collections import defaultdict
from utils import group_events_by_day, format_duration


def parse_events(events):
    """
    Convert event timestamps to datetime objects.
    - events (list): List of event dictionaries, each with a 'timestamp' string.
    
    Returns:
        list: Updated event list with parsed 'timestamp' as datetime objects.
    """
    # Iterate over each event and convert its 'timestamp' string to a datetime object
    for event in events:
        event["timestamp"] = datetime.fromisoformat(event["timestamp"])
    return events


def compute_cumulative_time(events):
    """
    Compute total time spent on each task.
    - events (list): List of event dictionaries, each with 'timestamp', 'event', and 'activity' (task name).
    
    Returns:
        dict: Task names as keys and total time spent on the task in seconds as values.
    """
    # Initialize a dictionary to store the total time for each task using defaultdict
    tasks = defaultdict(timedelta)
    
    # Variables to track the current task and its start time
    current_task = None
    start_time = None

    # Loop through each event in the list of events
    for event in events:
        if event["event"] == "start":
            # Start a new task: record the task name and the start time
            current_task = event["activity"]
            start_time = event["timestamp"]
        elif event["event"] == "stop" and current_task and start_time:
            # Stop the task: calculate the time spent on it and add to the total
            tasks[current_task] += event["timestamp"] - start_time
            current_task = None  # Reset the current task
            start_time = None  # Reset the start time

    # Return the cumulative time for each task in seconds
    return {task: time.total_seconds() for task, time in tasks.items()}


def compute_average_time_per_weekday(events):
    """
    Compute the average time spent per weekday.
    - events (list): List of event dictionaries.
    
    Returns:
        dict: Weekdays as keys (0=Monday, 6=Sunday) and average time spent on that weekday in seconds.
    """
    # Initialize a dictionary to store durations grouped by weekdays (0=Monday, 6=Sunday)
    weekdays = defaultdict(list)

    # Iterate over pairs of start and stop events
    for i in range(0, len(events) - 1, 2):
        if events[i]["event"] == "start" and events[i + 1]["event"] == "stop":
            # Calculate the duration for this task on the current day
            duration = events[i + 1]["timestamp"] - events[i]["timestamp"]
            weekdays[events[i]["timestamp"].weekday()].append(duration)

    # Calculate the average time for each weekday
    return {day: sum(durations, timedelta()).total_seconds() / len(durations) for day, durations in weekdays.items()}


def compute_average_tracked_time(events):
    """
    Compute the average tracked time per day.
    - events (list): List of event dictionaries.
    
    Returns:
        float: The average tracked time in seconds per day.
    """
    # Group the events by day using the utility function 'group_events_by_day'
    grouped_days = group_events_by_day(events)
    
    total_seconds = 0
    total_days = len(grouped_days)

    # Iterate over the grouped days and compute the total time for each day
    for date, day_events in grouped_days.items():
        # Sum the time differences between the start time and each stop event for the day
        daily_seconds = sum((e["timestamp"] - day_events[0]["timestamp"]).total_seconds() for e in day_events[1:])
        total_seconds += daily_seconds

    # Return the average tracked time per day, if there are any days
    return total_seconds / total_days if total_days > 0 else 0


def compute_analytics(events):
    """
    Display all analytics based on the tracked events.
    - events (list): List of event dictionaries.
    """
    # Parse the event timestamps into datetime objects
    events = parse_events(events)

    # Compute the cumulative time for each task
    cumulative_time = compute_cumulative_time(events)
    # Compute the average time spent per weekday
    avg_time_per_weekday = compute_average_time_per_weekday(events)
    # Compute the average tracked time per day
    avg_tracked_time = compute_average_tracked_time(events)

    # Print out the cumulative time per task
    print("Cumulative time per task:")
    for task, time in cumulative_time.items():
        print(f"- {task}: {format_duration(time)}")  # Format the time before displaying

    # Print out the average time per weekday
    print("\nAverage time per weekday:")
    for day, time in avg_time_per_weekday.items():
        print(f"- {['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][day]}: {format_duration(time)}")
    # Print out the average tracked time per day
    print(f"\nAverage tracked time per day: {format_duration(avg_tracked_time)}")