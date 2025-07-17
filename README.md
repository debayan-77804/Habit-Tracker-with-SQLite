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
