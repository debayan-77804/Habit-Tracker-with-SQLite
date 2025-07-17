##Habit Tracker CLI App (Python + SQLite)##

Overview

This is a Command-Line Interface (CLI) based Habit Tracker application developed in Python. The app helps users maintain consistency with their daily habits by tracking completion, calculating streaks, and offering reminders. All data is stored locally using an SQLite database.

Features

Add new habits

Edit existing habit names

Delete habits

Mark habits as completed for the current day

View all habits with streaks and dates

Weekly and Monthly Statistics (completion count)

Export all habit data to a CSV file

Reminder Functionality: Pops up every 4 hours to remind users to check in

Technologies Used

Python 3

SQLite (via sqlite3 module)

CSV module

datetime module

threading for background reminders

How to Run

Ensure you have Python 3 installed on your system.

Save the script as habit_tracker.py.

Open your terminal and navigate to the folder containing the script.

Run the script:

python habit_tracker.py

App Menu Options

When running, the app will display the following menu:

 >> Habit Tracker Menu <<
1. Add Habit
2. Edit Habit Name
3. Delete Habit
4. Mark Habit as Completed
5. View All Habits
6. Weekly and Monthly Statistics
7. Export Habit Data to CSV
8. Exit

Export to CSV

When you choose option 7, the app creates a file named habit_report.csv in the same directory.

Open it using any spreadsheet viewer to review your data.

Notes

All habits are stored in database.db (auto-created locally).

Reminder functionality runs in the background and prompts you every 4 hours.

File Summary

habit_tracker.py - CLI app with all core and bonus features

database.db - SQLite database file (auto-generated)

habit_report.csv - Optional file generated when exporting data

This project is useful for students, professionals, and anyone who wants to build and maintain good habits through self-monitoring.
