import os
import json
import pytest
from unittest.mock import patch, mock_open
from datetime import datetime
from time_tracker import (
    load_events,
    save_events,
    start_task,
    stop_task,
    export_events,
    import_events,
)

# Test fixture to mock the file system
@pytest.fixture
def mock_file():
    with patch("builtins.open", mock_open()) as mocked_file:
        yield mocked_file

@pytest.fixture
def mock_events_file():
    events = [
        {
            "timestamp": datetime.now().isoformat(),
            "event": "start",
            "activity": "Fixing bug",
        }
    ]
    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data=json.dumps(events))
    ):
        yield events

def test_load_events_empty_file(mock_file):
    with patch("os.path.exists", return_value=False):
        events = load_events()
        assert events == []

def test_load_events_non_empty_file(mock_events_file):
    events = load_events()
    assert len(events) == 1
    assert events[0]["event"] == "start"
    assert events[0]["activity"] == "Fixing bug"

def test_save_events(mock_file):
    events = [
        {
            "timestamp": datetime.now().isoformat(),
            "event": "start",
            "activity": "Testing save",
        }
    ]
    save_events(events)
    mock_file().write.assert_called_once_with(json.dumps(events, indent=4))

def test_start_task_no_existing_task(mock_file):
    with patch("os.path.exists", return_value=False):
        start_task("New Task")
        handle = mock_file()
        handle.write.assert_called_once()
        written_data = json.loads(handle.write.call_args[0][0])
        assert written_data[0]["event"] == "start"
        assert written_data[0]["activity"] == "New Task"

def test_start_task_existing_task(mock_events_file):
    with pytest.raises(ValueError, match="A task is already running."):
        start_task("Another Task")

def test_stop_task_running_task(mock_events_file, mock_file):
    stop_task()
    handle = mock_file()
    handle.write.assert_called_once()
    written_data = json.loads(handle.write.call_args[0][0])
    assert written_data[-1]["event"] == "stop"
    assert written_data[-1]["activity"] == "Fixing bug"

def test_stop_task_no_running_task(mock_file):
    with patch("os.path.exists", return_value=False):
        with pytest.raises(ValueError, match="No task is currently running."):
            stop_task()

def test_export_events_to_json(mock_events_file, mock_file):
    export_events("json", "test_events.json")
    handle = mock_file()
    handle.write.assert_called_once()
    written_data = json.loads(handle.write.call_args[0][0])
    assert len(written_data) == 1
    assert written_data[0]["event"] == "start"

def test_export_events_to_csv(mock_events_file, mock_file):
    with patch("csv.DictWriter") as mock_csv_writer:
        export_events("csv", "test_events.csv")
        mock_csv_writer().writeheader.assert_called_once()
        mock_csv_writer().writerows.assert_called_once()

def test_import_events_from_json(mock_file):
    imported_data = [
        {
            "timestamp": datetime.now().isoformat(),
            "event": "start",
            "activity": "Imported Task",
        }
    ]
    mock_file().read.return_value = json.dumps(imported_data)

    with patch("os.path.exists", return_value=True):
        import_events("json", "imported_events.json")
        handle = mock_file()
        handle.write.assert_called_once()
        written_data = json.loads(handle.write.call_args[0][0])
        assert len(written_data) == 1
        assert written_data[0]["event"] == "start"
        assert written_data[0]["activity"] == "Imported Task"

def test_import_events_from_csv(mock_file):
    imported_csv_data = "timestamp,event,activity\n2023-11-21T10:00:00,start,CSV Task"
    mock_file().read.return_value = imported_csv_data

    with patch("os.path.exists", return_value=True), patch("csv.DictReader") as mock_csv_reader:
        mock_csv_reader.return_value = [
            {"timestamp": "2023-11-21T10:00:00", "event": "start", "activity": "CSV Task"}
        ]
        import_events("csv", "imported_events.csv")
        handle = mock_file()
        handle.write.assert_called_once()
        written_data = json.loads(handle.write.call_args[0][0])
        assert len(written_data) == 1
        assert written_data[0]["event"] == "start"
        assert written_data[0]["activity"] == "CSV Task"