import tkinter as tk
from load import load_tasks

def delete_task(conn, task_listbox):
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_id = task_listbox.get(selected_task_index)[0]

        cursor = conn.cursor()
        # Pobierz priorytet usuwanego zadania
        cursor.execute('SELECT priority FROM tasks WHERE id=?', (task_id,))
        deleted_priority = cursor.fetchone()[0]

        # Usuń zadanie
        cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        conn.commit()

        # Aktualizuj priorytety pozostałych zadań
        update_priorities_after_delete(conn, deleted_priority)

        # Wczytaj zadania po usunięciu
        load_tasks(conn, task_listbox)

def update_priorities_after_delete(conn, deleted_priority):
    cursor = conn.cursor()
    # Pobierz zadania z priorytetem większym niż usuwane zadanie
    cursor.execute('SELECT id, priority FROM tasks WHERE priority > ?', (deleted_priority,))
    tasks_to_update = cursor.fetchall()

    # Zaktualizuj priorytety
    for task in tasks_to_update:
        task_id = task[0]
        current_priority = task[1]
        new_priority = max(1, current_priority - 1)
        cursor.execute('UPDATE tasks SET priority=? WHERE id=?', (new_priority, task_id))

    # Zatwierdź zmiany
    conn.commit()