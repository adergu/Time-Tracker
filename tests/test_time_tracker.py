import os
import csv  # Import csv module
import json  # Import json module
import unittest
from unittest.mock import patch
import sys
# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from time_tracker import (
    start_task,
    stop_task,
    export_events,
    import_events,
    load_events,
    save_events
)

class TestTimeTracker(unittest.TestCase):
    EVENTS_FILE = "test_events.json"  # Use a test-specific file

    def setUp(self):
        # Mock the events file location
        self.patcher = patch("time_tracker.EVENTS_FILE", self.EVENTS_FILE)
        self.patcher.start()
        if os.path.exists(self.EVENTS_FILE):
            os.remove(self.EVENTS_FILE)  # Ensure a clean slate for each test

    def tearDown(self):
        # Stop the patcher and remove the test events file
        self.patcher.stop()
        if os.path.exists(self.EVENTS_FILE):
            os.remove(self.EVENTS_FILE)

    def test_start_task(self):
        start_task("Test Task")
        events = load_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["activity"], "Test Task")

    def test_start_task_when_task_running(self):
        start_task("Test Task")
        with self.assertRaises(ValueError) as context:
            start_task("Another Task")
        self.assertEqual(str(context.exception), "A task is already running. Stop it before starting a new one.")

    def test_stop_task(self):
        start_task("Test Task")
        stop_task()
        events = load_events()
        self.assertEqual(len(events), 2)
        self.assertEqual(events[-1]["event"], "stop")

    def test_stop_task_when_no_task_running(self):
        with self.assertRaises(ValueError) as context:
            stop_task()
        self.assertEqual(str(context.exception), "No task is currently running.")

    def test_export_events_to_csv(self):
        start_task("Test Task")
        stop_task()
        export_events("csv", "test_export.csv")
        self.assertTrue(os.path.exists("test_export.csv"))

    def test_export_events_to_json(self):
        start_task("Test Task")
        stop_task()
        export_events("json", "test_export.json")
        self.assertTrue(os.path.exists("test_export.json"))

    def test_import_events_from_csv(self):
        with open("test_import.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["timestamp", "event", "activity"])
            writer.writeheader()
            writer.writerow({"timestamp": "2023-01-01T00:00:00", "event": "start", "activity": "Imported Task"})
        import_events("csv", "test_import.csv")
        events = load_events()
        self.assertEqual(len(events), 1)

    def test_import_events_from_json(self):
        with open("test_import.json", "w") as file:
            json.dump([{"timestamp": "2023-01-01T00:00:00", "event": "start", "activity": "Imported Task"}], file)
        import_events("json", "test_import.json")
        events = load_events()
        self.assertEqual(len(events), 1)

if __name__ == "__main__":
    unittest.main()