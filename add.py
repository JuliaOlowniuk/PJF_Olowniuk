import tkinter as tk
from tkinter import messagebox
from load import load_tasks

def add_task(conn, task_entry, task_listbox):
    task = task_entry.get()
    if task:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task, done) VALUES (?, ?)', (task, False))
        conn.commit()
        task_entry.delete(0, tk.END)
        load_tasks(conn, task_listbox)
    else:
        messagebox.showwarning("Uwaga", "Wprowadź treść zadania!")