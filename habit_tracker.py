import sqlite3
from datetime import date, datetime, timedelta
import csv
import os
import threading
import time

# ------------ Database Setup ------------
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at DATE NOT NULL,
    last_completed DATE,
    streak INTEGER DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS completions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER,
    completed_on DATE,
    FOREIGN KEY (habit_id) REFERENCES habits(id)
)
''')

conn.commit()

# ------------ Core Functions ------------

def add_habit(name):
    cursor.execute("INSERT INTO habits (name, created_at) VALUES (?, ?)", (name, str(date.today())))
    conn.commit()
    print(f"Habit '{name}' added.")

def edit_habit(habit_id, new_name):
    cursor.execute("UPDATE habits SET name = ? WHERE id = ?", (new_name, habit_id))
    conn.commit()
    print(f"Habit {habit_id} renamed to '{new_name}'.")

def delete_habit(habit_id):
    cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    cursor.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
    conn.commit()
    print(f"Habit {habit_id} deleted.")

def mark_completed(habit_id):
    today = str(date.today())
    cursor.execute("SELECT last_completed, streak FROM habits WHERE id = ?", (habit_id,))
    row = cursor.fetchone()

    if not row:
        print("Habit not found.")
        return

    last_completed, streak = row
    if last_completed == today:
        print("Already marked as completed today.")
        return

    if last_completed:
        last_date = datetime.strptime(last_completed, "%Y-%m-%d").date()
        if (date.today() - last_date).days == 1:
            streak += 1
        else:
            streak = 1
    else:
        streak = 1

    cursor.execute("UPDATE habits SET last_completed = ?, streak = ? WHERE id = ?",
                   (today, streak, habit_id))
    cursor.execute("INSERT INTO completions (habit_id, completed_on) VALUES (?, ?)",
                   (habit_id, today))
    conn.commit()
    print("Habit marked as completed for today.")

def list_habits():
    cursor.execute("SELECT id, name, created_at, last_completed, streak FROM habits")
    rows = cursor.fetchall()
    if rows:
        print("\nYour Habits:")
        print("ID | Name         | Created   | Last Done | Streak")
        print("--------------------------------------------------")
        for row in rows:
            print(f"{row[0]:<3}| {row[1]:<12}| {row[2]} | {row[3] or '-':<10} | {row[4]}")
    else:
        print("No habits found.")

def view_stats(habit_id):
    today = date.today()
    last_7 = today - timedelta(days=6)
    last_30 = today - timedelta(days=29)

    cursor.execute("SELECT COUNT(*) FROM completions WHERE habit_id = ? AND completed_on >= ?", (habit_id, last_7))
    week_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM completions WHERE habit_id = ? AND completed_on >= ?", (habit_id, last_30))
    month_count = cursor.fetchone()[0]

    print(f"Last 7 days: {week_count} completions")
    print(f"Last 30 days: {month_count} completions")

def export_to_csv():
    filename = "habit_data.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Habit Name", "Date Completed"])
        cursor.execute('''
            SELECT habits.name, completions.completed_on
            FROM completions
            JOIN habits ON completions.habit_id = habits.id
            ORDER BY completions.completed_on
        ''')
        for row in cursor.fetchall():
            writer.writerow(row)
    print(f"Data exported to {filename}")

# ------------ Reminder Thread ------------
def reminder_loop():
    while True:
        time.sleep(4 * 60 * 60)  # 4 hours
        print("\nReminder: Don't forget to mark your habits today!\n")

reminder_thread = threading.Thread(target=reminder_loop, daemon=True)
reminder_thread.start()

# ------------ CLI Menu ------------
def main():
    while True:
        print("\n=== Habit Tracker CLI Menu ===")
        print("1. Add Habit")
        print("2. Edit Habit")
        print("3. Delete Habit")
        print("4. Mark Habit as Completed")
        print("5. View All Habits")
        print("6. View Weekly/Monthly Stats")
        print("7. Export Data to CSV")
        print("8. Exit")

        choice = input("Enter choice (1-8): ")

        if choice == '1':
            name = input("Enter habit name: ")
            add_habit(name)
        elif choice == '2':
            habit_id = int(input("Enter habit ID to edit: "))
            new_name = input("Enter new name: ")
            edit_habit(habit_id, new_name)
        elif choice == '3':
            habit_id = int(input("Enter habit ID to delete: "))
            delete_habit(habit_id)
        elif choice == '4':
            habit_id = int(input("Enter habit ID to mark complete: "))
            mark_completed(habit_id)
        elif choice == '5':
            list_habits()
        elif choice == '6':
            habit_id = int(input("Enter habit ID for stats: "))
            view_stats(habit_id)
        elif choice == '7':
            export_to_csv()
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
