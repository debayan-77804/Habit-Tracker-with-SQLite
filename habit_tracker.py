import sqlite3
from datetime import date, datetime

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
conn.commit()

# ------------ Core Functions ------------

def add_habit(name):
    cursor.execute("INSERT INTO habits (name, created_at) VALUES (?, ?)", (name, str(date.today())))
    conn.commit()
    print(f"✔ Habit '{name}' added.")

def delete_habit(habit_id):
    cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.commit()
    print(f"X️ Habit {habit_id} deleted.")

def mark_completed(habit_id):
    today = str(date.today())
    cursor.execute("SELECT last_completed, streak FROM habits WHERE id = ?", (habit_id,))
    row = cursor.fetchone()
    
    if not row:
        print("❌ Habit not found.")
        return

    last_completed, streak = row
    if last_completed == str(today):
        print("⚠️ Already marked for today.")
        return

    if last_completed:
        last_date = datetime.strptime(last_completed, "%Y-%m-%d").date()
        if (today - last_date).days == 1:
            streak += 1
        else:
            streak = 1
    else:
        streak = 1

    cursor.execute("UPDATE habits SET last_completed = ?, streak = ? WHERE id = ?", (today, streak, habit_id))
    conn.commit()
    print("✅ Habit marked as completed.")

def list_habits():
    cursor.execute("SELECT id, name, created_at, last_completed, streak FROM habits")
    rows = cursor.fetchall()
    if rows:
        print("\n📋 Your Habits:")
        print("ID | Name             | Created At | Last Completed | Streak")
        print("-------------------------------------------------------------")
        for row in rows:
            print(f"{row[0]:<3}| {row[1]:<17}| {row[2]} | {row[3]}       | {row[4]}")
    else:
        print("❗ No habits found.")

# ------------ CLI Menu ------------

def main():
    while True:
        print("\n >> Habit Tracker Menu <<")
        print("1. ➕ Add Habit")
        print("2. ✅ Mark Habit as Completed")
        print("3. 📄 View All Habits")
        print("4. 🗑️ Delete Habit")
        print("5. Bye! Exit")

        choice = input(">>>Enter your choice: ")

        if choice == '1':
            name = input("Enter habit name: ")
            add_habit(name)
        elif choice == '2':
            habit_id = int(input("Enter habit ID to mark completed: "))
            mark_completed(habit_id)
        elif choice == '3':
            list_habits()
        elif choice == '4':
            habit_id = int(input("Enter habit ID to delete: "))
            delete_habit(habit_id)
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
