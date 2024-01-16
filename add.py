import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox
from load import load_tasks

def add_task(conn, user_id, task_listbox, task_entry_widget, priority_entry, due_date_entry, dynamic_priority_value=None, display_mode=None, weekday_combobox=None):
    task = task_entry_widget.get().strip()
    priority = priority_entry.get().strip()
    due_date = due_date_entry.get().strip()

    print(f"Adding task for user {user_id}")  # Dodaj ten print
    print(f"Task: {task}, Priority: {priority}, Due Date: {due_date}")

    if dynamic_priority_value is not None:
        priority = dynamic_priority_value

    if not task and not priority:
        messagebox.showwarning("Uwaga", "Wprowadź treść zadania i priorytet!")
        return
    elif not priority:
        messagebox.showwarning("Uwaga", "Wprowadź priorytet!")
        return

    try:
        priority = int(priority)
    except ValueError:
        messagebox.showwarning("Uwaga", "Priorytet musi być liczbą całkowitą!")
        return

    cursor = conn.cursor()

    try:
        if due_date == '' and display_mode == 1:
            task_text = f"[{'x' if False else ' '}] {task} - Priorytet: {priority}"
        elif display_mode == 2 and weekday_combobox is not None:
            selected_weekday = weekday_combobox.get()
            task_text = f"[{'x' if False else ' '}] {task} - Priorytet: {priority} - Data wykonania: {selected_weekday}"
        else:
            task_text = f"[{'x' if False else ' '}] {task} - Priorytet: {priority} - Data wykonania: {due_date}"

        print(f"Executing SQL: INSERT INTO tasks (user_id, task_name, done, priority, due_date) VALUES (?, ?, ?, ?, ?)", (user_id, task, False, priority, due_date))
        cursor.execute('INSERT INTO tasks (user_id, task_name, done, priority, due_date) VALUES (?, ?, ?, ?, ?)', (user_id, task, False, priority, due_date))
        conn.commit()
        task_entry_widget.delete(0, tk.END)
        priority_entry.delete(0, tk.END)
        due_date_entry.delete(0, tk.END)
        load_tasks(conn, user_id, task_listbox)
        print("Zadanie dodane pomyślnie")
    except sqlite3.Error as e:
        print(f"Błąd SQLite przy dodawaniu zadania do bazy danych: {e}")
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas dodawania zadania do bazy danych: {e}")
