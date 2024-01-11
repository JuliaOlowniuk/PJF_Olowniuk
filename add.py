import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox
from load import load_tasks

def add_task(conn, task_entry_widget, task_listbox, priority_entry, due_date_entry, dynamic_priority_value=None):
    task = task_entry_widget.get().strip()
    priority = priority_entry.get().strip()
    due_date = due_date_entry.get().strip()

    if dynamic_priority_value is not None:
        # Jeśli dostarczono dynamiczny priorytet, użyj go
        priority = dynamic_priority_value

    if task and priority:
        try:
            priority = int(priority)
        except ValueError:
            messagebox.showwarning("Uwaga", "Priorytet musi być liczbą całkowitą!")
            return

        cursor = conn.cursor()

        cursor.execute('SELECT * FROM tasks WHERE priority=?', (priority,))
        existing_task = cursor.fetchone()

        if existing_task:
            cursor.execute('SELECT COUNT(*) FROM tasks WHERE priority < ?', (priority,))
            lower_priority_count = cursor.fetchone()[0]

            new_priority = lower_priority_count + 1

            user_response = simpledialog.askinteger("Nowy priorytet", f"Istnieje zadanie o priorytecie {priority}. Podaj nowy priorytet (na podstawie ilości zadań z niższymi priorytetami): {new_priority}")
            if user_response is not None:
                priority = user_response
            else:
                return

        try:
            # Sprawdź, czy data wykonania została dostarczona
            if due_date == '':
                # Jeśli nie, dodaj zadanie bez daty wykonania
                task_text = f"[{'x' if False else ' '}] {task} - Priorytet: {priority}"
            else:
                # Jeśli tak, dodaj zadanie z datą wykonania
                task_text = f"[{'x' if False else ' '}] {task} - Priorytet: {priority} - Data wykonania: {due_date}"

            cursor.execute('INSERT INTO tasks (task, done, priority, due_date) VALUES (?, ?, ?, ?)', (task, False, priority, due_date))
            conn.commit()
            task_entry_widget.delete(0, tk.END)
            priority_entry.delete(0, tk.END)
            due_date_entry.delete(0, tk.END)
            load_tasks(conn, task_listbox)
            print("Zadanie dodane pomyślnie")
        except sqlite3.Error as e:
            print(f"Błąd SQLite przy dodawaniu zadania do bazy danych: {e}")
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas dodawania zadania do bazy danych: {e}")
    else:
        messagebox.showwarning("Uwaga", "Wprowadź treść zadania i priorytet!")