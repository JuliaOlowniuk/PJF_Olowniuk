import tkinter as tk

def refresh_task_listbox(conn, task_listbox):
    task_listbox.delete(0, tk.END)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY id DESC')
    tasks = cursor.fetchall()
    for task in tasks:
        elements = [f"[{'x' if task[2] else ' '}] {task[1]}", f"Priorytet: {task[3]}"]

        # Dodaj datę wykonania, jeśli dostępna i nie jest pusta
        if task[4] is not None and task[4] != '':
            elements.append(f"Data wykonania: {task[4]}")

        task_text = ' - '.join(elements)
        task_listbox.insert(tk.END, (task[0], task_text))

def load_tasks(conn, task_listbox):
    task_listbox.delete(0, tk.END)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY id DESC')
    tasks = cursor.fetchall()
    for task in tasks:
        elements = [f"[{'x' if task[2] else ' '}] {task[1]}", f"Priorytet: {task[3]}"]

        # Dodaj datę wykonania, jeśli dostępna i nie jest pusta
        if task[4] is not None and task[4] != '':
            elements.append(f"Data wykonania: {task[4]}")

        task_text = ' - '.join(elements)
        task_listbox.insert(tk.END, (task[0], task_text))
