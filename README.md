# Habit Tracker CLI App (Python + SQLite)

## Overview

This is a **Command-Line Interface (CLI)** based Habit Tracker application developed in Python.  
It helps users maintain consistency with their daily habits by tracking completions, calculating streaks, generating statistics, and offering reminders.  
All data is stored locally using an **SQLite database**.

## Features

- Add new habits  
- Edit existing habit names  
- Delete habits  
- Mark habits as completed for the current day  
- View all habits with streaks and dates  
- Track weekly and monthly completion statistics  
- Export all habit data to a CSV file  
- Reminder functionality (runs in background every 4 hours)

## Technologies Used

- Python 3  
- SQLite (`sqlite3` module)  
- `datetime` module  
- `threading` module  
- `csv` module  

## How to Run

1. Make sure Python 3 is installed on your system.
2. Save the script as `habit_tracker.py`.
3. Open a terminal and navigate to the script directory.
4. Run the script using:

   ```bash
   python habit_tracker.py
   ```

## App Menu Options

Once the app starts, you'll see the following menu:

```
>> Habit Tracker Menu <<

1. Add Habit  
2. Edit Habit Name  
3. Delete Habit  
4. Mark Habit as Completed  
5. View All Habits  
6. Weekly and Monthly Statistics  
7. Export Habit Data to CSV  
8. Exit  
```

## Export to CSV

- Selecting **option 7** will create a file named `habit_report.csv` in the same folder.
- This file contains all recorded habit data and can be opened with any spreadsheet program like Excel or Google Sheets.

## Notes

- The app creates a local file named `database.db` to store all habit records.
- Reminders run in the background and prompt users to check in every 4 hours.
- All features work offline without any internet requirement.

## File Summary

| File Name           | Description                                        |
|---------------------|----------------------------------------------------|
| `habit_tracker.py`  | Main CLI application script with all features      |
| `database.db`       | SQLite database file (auto-generated at runtime)   |
| `habit_report.csv`  | CSV export file (created when you choose option 7) |

## Who Can Use This?

This project is ideal for:

- Students looking to track study routines  
- Professionals managing daily goals  
- Anyone aiming to build consistent daily habits

## License

This project is open-source and free to use.
