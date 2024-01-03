import sqlite3
import tkinter as tk
from load import load_tasks

def dynamic_priority(conn, task_listbox, priority_entry):
    try:
        # Pobierz zadania z bazy danych
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE done=0 ORDER BY priority ASC')
        tasks = cursor.fetchall()

        # Znajdź zadania do usunięcia i zaktualizuj priorytet kolejnych
        next_priority = 1
        for task in tasks:
            task_id = task[0]
            cursor.execute('UPDATE tasks SET priority=? WHERE id=?', (next_priority, task_id))
            next_priority += 1

        # Zatwierdź zmiany
        conn.commit()

        # Wyświetl zaktualizowane zadania
        load_tasks(conn, task_listbox)

        # Aktualizuj widoczny priorytet w polu Entry
        priority_entry.delete(0, tk.END)
        priority_entry.insert(tk.END, str(next_priority))

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def load_tasks(conn, task_listbox):
    task_listbox.delete(0, tk.END)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY priority ASC')
    tasks = cursor.fetchall()
    for task in tasks:
        task_text = f"[{'x' if task[2] else ' '}] {task[1]} (Priorytet: {task[3]}, Data wykonania: {task[4]})"
        task_listbox.insert(tk.END, (task[0], task_text))
