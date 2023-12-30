import tkinter as tk
from load import load_tasks

def delete_task(conn, task_listbox):
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_id = task_listbox.get(selected_task_index)[0]
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        conn.commit()
        load_tasks(conn, task_listbox)
