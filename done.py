import tkinter as tk
from load import load_tasks

def mark_done(conn, task_listbox):
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_id = task_listbox.get(selected_task_index)[0]
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET done=? WHERE id=?', (True, task_id))
        conn.commit()
        load_tasks(conn, task_listbox)