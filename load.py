import tkinter as tk

def load_tasks(conn, task_listbox):
    task_listbox.delete(0, tk.END)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY id DESC')
    tasks = cursor.fetchall()
    for task in tasks:
        task_text = f"[{'x' if task[2] else ' '}] {task[1]}"
        task_listbox.insert(tk.END, (task[0], task_text))
