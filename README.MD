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