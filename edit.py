import tkinter as tk
from tkinter import simpledialog
import sqlite3
from load import load_tasks
def edit_description(conn, task_listbox):
    selected_task_indices = task_listbox.curselection()

    if selected_task_indices:
        # Pobierz ID zadania z pierwszego zaznaczonego elementu
        selected_task_index = selected_task_indices[0]
        task_id = task_listbox.get(selected_task_index)[0]

        current_description = get_task_description(conn, task_id)
        new_description = simpledialog.askstring("Edytuj opis", "Wprowadź nowy opis zadania:", initialvalue=current_description)

        if new_description is not None:
            update_task_description(conn, task_id, new_description)
            refresh_task_listbox(conn, task_listbox)

def get_task_description(conn, task_id):
    cursor = conn.cursor()
    cursor.execute('SELECT description FROM tasks WHERE id=?', (task_id,))
    result = cursor.fetchone()
    return result[0] if result else ""

def update_task_description(conn, task_id, new_description):
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET description=? WHERE id=?', (new_description, task_id))
    conn.commit()

def refresh_task_listbox(conn, task_listbox):
    load_tasks(conn, task_listbox)
