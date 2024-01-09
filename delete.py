import tkinter as tk
from tkinter import messagebox
from load import load_tasks

def delete_task(conn, task_listbox):
    selected_task_indices = task_listbox.curselection()

    if not selected_task_indices:
        messagebox.showwarning("Uwaga", "Nie wybrano zadania do usunięcia.")
        return

    selected_task_index = selected_task_indices[0]
    task_id, deleted_priority = task_listbox.get(selected_task_index)

    confirmation = messagebox.askyesno("Potwierdzenie", f"Czy na pewno chcesz usunąć zadanie o priorytecie {deleted_priority}?")

    if confirmation:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        conn.commit()

        # Dodaj wywołanie funkcji do aktualizacji priorytetów po usunięciu zadania
        update_priorities_after_delete(conn, task_listbox)
        load_tasks(conn, task_listbox)

def update_priorities_after_delete(conn, task_listbox):
    # Aktualizuj priorytety dla pozostałych zadań o niższym priorytecie
    selected_task_indices = task_listbox.curselection()

    if not selected_task_indices:
        return

    selected_task_index = selected_task_indices[0]
    deleted_priority = task_listbox.get(selected_task_index)[1]

    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET priority = priority - 1 WHERE priority > ?', (deleted_priority,))
    conn.commit()