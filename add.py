import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox
from load import load_tasks

def add_task(conn, task_entry, task_listbox, priority_entry):
    task = task_entry.get()
    priority = priority_entry.get()

    print(f"Task: {task}, Priority: {priority}")

    if task:
        try:
            priority = int(priority)
        except ValueError:
            messagebox.showwarning("Uwaga", "Priorytet musi być liczbą całkowitą!")
            return

        cursor = conn.cursor()

        # Sprawdź, czy istnieje zadanie o takim samym priorytecie
        cursor.execute('SELECT * FROM tasks WHERE priority=?', (priority,))
        existing_task = cursor.fetchone()

        if existing_task:
            # Zadanie o tym priorytecie już istnieje, przypisz kolejny dostępny priorytet
            next_priority = priority + 1
            while True:
                cursor.execute('SELECT * FROM tasks WHERE priority=?', (next_priority,))
                existing_next_priority_task = cursor.fetchone()
                if not existing_next_priority_task:
                    break
                next_priority += 1

            user_response = simpledialog.askinteger("Nowy priorytet", f"Istnieje zadanie o priorytecie {priority}. Podaj nowy priorytet (następny dostępny to {next_priority}):")
            if user_response is not None:
                priority = user_response
                # Zaktualizuj istniejące zadanie na następny priorytet
                cursor.execute('UPDATE tasks SET priority=? WHERE priority=?', (next_priority, priority))
                conn.commit()
            else:
                return

        try:
            cursor.execute('INSERT INTO tasks (task, done, priority) VALUES (?, ?, ?)', (task, False, priority))
            conn.commit()
            task_entry.delete(0, tk.END)
            priority_entry.delete(0, tk.END)
            load_tasks(conn, task_listbox)
            print("Zadanie dodane pomyślnie.")
        except sqlite3.Error as e:
            print(f"Błąd SQLite przy dodawaniu zadania do bazy danych: {e}")
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas dodawania zadania do bazy danych: {e}")
    else:
        messagebox.showwarning("Uwaga", "Wprowadź treść zadania!")
