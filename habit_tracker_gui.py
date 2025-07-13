import sqlite3
from datetime import date, datetime
import tkinter as tk
from tkinter import messagebox, ttk
import csv
from tkinter import filedialog
import threading
import time

# --- Database Setup ---
conn = sqlite3.connect("database.db")
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
    CREATE TABLE IF NOT EXISTS habit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        completed_on DATE NOT NULL,
        FOREIGN KEY (habit_id) REFERENCES habits(id)
    )
''')
conn.commit()

# --- Functional Methods ---

def add_habit():
    name = habit_entry.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Please enter a habit name.")
        return
    cursor.execute("INSERT INTO habits (name, created_at) VALUES (?, ?)", (name, str(date.today())))
    conn.commit()
    habit_entry.delete(0, tk.END)
    update_table()

def delete_habit():
    selected = habit_table.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "No habit selected.")
        return
    habit_id = habit_table.item(selected[0])["values"][0]
    cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.commit()
    update_table()

def mark_completed():
    selected = habit_table.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a habit.")
        return

    habit_id = habit_table.item(selected[0])["values"][0]
    today = date.today()
    cursor.execute("SELECT last_completed, streak FROM habits WHERE id = ?", (habit_id,))
    row = cursor.fetchone()

    if not row:
        return

    last_completed, streak = row
    if last_completed == str(today):
        messagebox.showinfo("Info", "This habit has already been marked for today.")
        return

    if last_completed:
        last_date = datetime.strptime(last_completed, "%Y-%m-%d").date()
        if (today - last_date).days == 1:
            streak += 1
        else:
            streak = 1
    else:
        streak = 1

    cursor.execute("UPDATE habits SET last_completed = ?, streak = ? WHERE id = ?", (str(today), streak, habit_id))
    cursor.execute("INSERT INTO habit_logs (habit_id, completed_on) VALUES (?, ?)", (habit_id, str(today)))
    conn.commit()
    update_table()

def export_to_csv():
    cursor.execute("SELECT * FROM habits")
    rows = cursor.fetchall()
    if not rows:
        messagebox.showinfo("No Data", "No habits to export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")],
                                             title="Save CSV File")
    if file_path:
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Habit Name", "Created At", "Last Completed", "Streak"])
            writer.writerows(rows)
        messagebox.showinfo("Exported", f"Data exported to {file_path}")

def show_stats():
    stats_window = tk.Toplevel(root)
    stats_window.title("Weekly & Monthly Stats")

    label = tk.Label(stats_window, text="Habit Completion Count (Last 7 & 30 Days)", font=("Arial", 12, "bold"))
    label.pack(pady=10)

    tree = ttk.Treeview(stats_window, columns=("Habit", "7-Day", "30-Day"), show="headings")
    tree.heading("Habit", text="Habit Name")
    tree.heading("7-Day", text="Last 7 Days")
    tree.heading("30-Day", text="Last 30 Days")
    tree.pack(fill="both", expand=True, padx=20, pady=10)

    cursor.execute("SELECT id, name FROM habits")
    habits = cursor.fetchall()

    for habit_id, name in habits:
        cursor.execute("SELECT COUNT(*) FROM habit_logs WHERE habit_id = ? AND completed_on >= date('now', '-7 days')", (habit_id,))
        week_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM habit_logs WHERE habit_id = ? AND completed_on >= date('now', '-30 days')", (habit_id,))
        month_count = cursor.fetchone()[0]
        tree.insert("", tk.END, values=(name, week_count, month_count))

def update_table():
    for item in habit_table.get_children():
        habit_table.delete(item)
    cursor.execute("SELECT id, name, created_at, last_completed, streak FROM habits")
    for row in cursor.fetchall():
        habit_table.insert("", tk.END, values=row)

# --- Reminder Function ---
def reminder_loop(interval_minutes=60):  # change to 0.1 for testing (~6 seconds)
    while True:
        time.sleep(interval_minutes * 60)
        root.after(0, lambda: messagebox.showinfo("Reminder ⏰", "Don't forget to complete your habits today!"))

def start_reminder_thread():
    reminder_thread = threading.Thread(target=reminder_loop, args=(240,), daemon=True)  # every 4 hours
    reminder_thread.start()

# --- GUI Setup ---

root = tk.Tk()
root.title("Habit Tracker")
root.geometry("800x450")

# Entry + Buttons
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

habit_entry = tk.Entry(top_frame, width=40, fg="grey")
habit_entry.insert(0, "Enter habit name...")
habit_entry.grid(row=0, column=0, padx=10)

def on_entry_click(event):
    if habit_entry.get() == "Enter habit name...":
        habit_entry.delete(0, tk.END)
        habit_entry.config(fg="black")

def on_focusout(event):
    if habit_entry.get() == "":
        habit_entry.insert(0, "Enter habit name...")
        habit_entry.config(fg="grey")

habit_entry.bind("<FocusIn>", on_entry_click)
habit_entry.bind("<FocusOut>", on_focusout)

add_btn = tk.Button(top_frame, text="Add your Habit", command=add_habit, bg="#27ae60", fg="white")
add_btn.grid(row=0, column=1, padx=5)

complete_btn = tk.Button(top_frame, text="Mark as Completed", command=mark_completed, bg="#f1c40f", fg="black")
complete_btn.grid(row=0, column=2, padx=5)

delete_btn = tk.Button(top_frame, text="Delete your Habit", command=delete_habit, bg="#e74c3c", fg="white")
delete_btn.grid(row=0, column=3, padx=5)

export_btn = tk.Button(top_frame, text="Export to CSV", command=export_to_csv, bg="#3498db", fg="white")
export_btn.grid(row=0, column=4, padx=5)

stats_btn = tk.Button(top_frame, text="Show Stats", command=show_stats, bg="#8e44ad", fg="white")
stats_btn.grid(row=0, column=5, padx=5)

# Habit Table
habit_table = ttk.Treeview(root, columns=("ID", "Name", "Created", "Last Completed", "Streak"), show="headings")
habit_table.heading("ID", text="ID")
habit_table.heading("Name", text="Habit Name")
habit_table.heading("Created", text="Created At")
habit_table.heading("Last Completed", text="Last Done")
habit_table.heading("Streak", text="Streak")

habit_table.column("ID", width=40, anchor="center")
habit_table.column("Name", width=180)
habit_table.column("Created", width=100, anchor="center")
habit_table.column("Last Completed", width=100, anchor="center")
habit_table.column("Streak", width=70, anchor="center")

habit_table.pack(pady=10, fill="x")
update_table()

# Start reminder in background
start_reminder_thread()

root.mainloop()
