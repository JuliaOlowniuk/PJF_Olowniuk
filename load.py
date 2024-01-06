import tkinter as tk
def load_tasks(conn, task_listbox):
    task_listbox.delete(0, tk.END)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY id DESC')
    tasks = cursor.fetchall()
    for task in tasks:
        task_text = f"[{'x' if task[2] else ' '}] {task[1]} - Priorytet: {task[3]}"

        # Dodaj datę wykonania tylko jeśli pole daty nie jest None
        if task[4] is not None and task[4] != 'None':
            task_text += f" - Data wykonania: {task[4]}"

        task_listbox.insert(tk.END, task_text)