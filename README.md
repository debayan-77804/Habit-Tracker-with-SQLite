# Habit Tracker App (Python + SQLite + Tkinter)

## What is this project about?

This is a Habit Tracking App developed in Python. It comes in two versions:

* A command-line (CLI) version: `habit_tracker.py`
* A GUI version with additional features: `habit_tracker_gui.py`

The purpose of this app is to help users build and maintain positive daily habits by tracking progress over time.

### Users can:

* Add their personal habits (e.g., Exercise, Study, Drink Water)
* Mark habits as completed each day
* Track consistency through a streak counter
* View habit completion trends over the past 7 and 30 days
* Export their habit history to a CSV file
* Receive reminders every 4 hours (GUI version)

---

## Key Features (GUI version)

* Add & Delete Habits
* Track Daily Progress
* Weekly/Monthly Statistics
* Export to CSV
* Pop-up Reminders every 4 hours

---

## Technologies Used

* Python 3.x
* Tkinter – GUI interface
* SQLite – Local database
* CSV module – Data export
* Threading – Background reminders (GUI)

---

## How to Run This App

### To run the GUI version:

1. Make sure Python 3 is installed.

2. Run the GUI script:
   'habit_tracker_gui.py'
   

3. Use the interface to:

   * Enter a habit
   * Mark as complete
   * View streaks, stats, and export

### To run the CLI version:

1. Run:
'habit_tracker.py'

2. Use the menu to add, complete, and view habits from the terminal.

---

## Files in this Project

> Note: The `database.db` file is automatically created the first time you run the app. You do not need to include it in the repository.

* `habit_tracker.py` – CLI version (basic tracking)
* `habit_tracker_gui.py` – Full-featured GUI version
* `README.md` – Project documentation

---

## Bonus Functionality (GUI only)

* Export data to `.csv`
* Weekly and monthly stats view
* Automatic pop-up reminders every 4 hours
