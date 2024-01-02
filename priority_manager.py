import sqlite3
import tkinter as tk

def dynamic_priority(conn, task_listbox, priority_entry):
    # Pobierz zadania z bazy danych
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY priority ASC')
    tasks = cursor.fetchall()

    # Zaktualizuj priorytety
    for i, task in enumerate(tasks, start=1):
        task_id = task[0]
        cursor.execute('UPDATE tasks SET priority=? WHERE id=?', (i, task_id))

    # Usuń zadania o priorytetach większych niż ilość pozostałych zadań
    cursor.execute('DELETE FROM tasks WHERE priority > ?', (len(tasks),))

    # Wyświetl zaktualizowane zadania
    load_tasks(conn, task_listbox)

    # Aktualizuj widoczny priorytet w polu Entry
    next_priority = len(tasks) + 1
    priority_entry.delete(0, tk.END)
    priority_entry.insert(tk.END, next_priority)

    # Zatwierdź zmiany
    conn.commit()

def load_tasks(conn, task_listbox):
    task_listbox.delete(0, tk.END)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY priority ASC')
    tasks = cursor.fetchall()
    for task in tasks:
        task_text = f"[{'x' if task[2] else ' '}] {task[1]} (Priorytet: {task[3]}, Data wykonania: {task[4]})"
        task_listbox.insert(tk.END, (task[0], task_text))