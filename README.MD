
# Terminal-Based TimeTracker

TimeTracker is a straightforward terminal-based application tailored for developers to monitor the time spent on tasks. It assumes developers work on one task at a time. The application supports starting/stopping tasks, importing/exporting task logs, and generating analytics on logged data.

---

## Features

- **Start/Stop Tasks**: Track task durations with start and stop commands.
- **Export/Import Events**: Save and load event logs in CSV or JSON formats.
- **Analytics**:
  - Total time spent on each task.
  - Average time spent on tasks per weekday.
  - Average daily tracked time.

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/TimeTracker.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd TimeTracker
   ```

3. **Set up a virtual environment (optional but recommended)**:

   - On Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Start a Task
Start tracking a task with the following command:

```bash
python src/time_tracker.py start "Task Name"
```

**Example**: 
```bash
python src/time_tracker.py start "Fixing serialization bug"
```

---

### Stop a Task
Stop the currently active task with:

```bash
python src/time_tracker.py stop
```

---

### Export Events
Export task logs to a CSV or JSON file:

```bash
python src/time_tracker.py export --format=csv
python src/time_tracker.py export --format=json
```

---

### Import Events
Load task logs from a previously exported file:

```bash
python src/time_tracker.py import --format=csv
python src/time_tracker.py import --format=json
```

---

### View Analytics
Generate analytics on logged tasks with:

```bash
python src/time_tracker.py analytics
```

**This will display**:
- Total time spent on each task.
- Average time spent on tasks for each weekday.
- Average time tracked per day.

---

## Dependencies

The following Python packages are required:

- `pytz` - Handles time zones (if necessary).
- `pytest` - For testing.
- `csv` - CSV file handling (built-in module).
- `json` - JSON file handling (built-in module).

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## Project Structure

```plaintext
TimeTracker/
├── src/
│   ├──_init_.py    # Main application
│   ├── time_tracker.py    # Main application
│   ├── analytics.py       # Analytics computations
│   ├── utils.py           # Utility functions (e.g., file handling)
│── test/
|    |──_init_.py
|    |──test_time_tracker.py
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions workflow for CI
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .gitignore              # Ignored files
```