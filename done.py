import tkinter as tk
from tkinter import messagebox
from load import load_tasks

def mark_done(conn, task_listbox):
    try:
        selected_task_indices = task_listbox.curselection()

        if not selected_task_indices:
            raise ValueError("Wybierz zadanie")

        for selected_task_index in selected_task_indices:
            task_id = task_listbox.get(selected_task_index)[0]
            cursor = conn.cursor()

            # Sprawdź, czy zadanie jest już zrobione
            cursor.execute('SELECT done FROM tasks WHERE id=?', (task_id,))
            current_done_status = cursor.fetchone()[0]

            if current_done_status:
                raise ValueError("Zadanie już jest oznaczone jako zrobione.")

            cursor.execute('UPDATE tasks SET done=? WHERE id=?', (True, task_id))
            conn.commit()

        load_tasks(conn, task_listbox)

    except ValueError as e:
        # Komunikat błędu związany z próbą ponownego oznaczenia zrobionego zadania
        messagebox.showerror("Błąd", str(e))


def mark_undone(conn, task_listbox):
    try:
        selected_task_indices = task_listbox.curselection()

        if not selected_task_indices:
            raise ValueError("Wybierz zadanie")

        for selected_task_index in selected_task_indices:
            task_id = task_listbox.get(selected_task_index)[0]
            cursor = conn.cursor()

            # Sprawdź, czy zadanie jest już niezrobione
            cursor.execute('SELECT done FROM tasks WHERE id=?', (task_id,))
            current_done_status = cursor.fetchone()[0]

            if not current_done_status:
                raise ValueError("Zadanie już jest oznaczone jako niezrobione.")

            cursor.execute('UPDATE tasks SET done=? WHERE id=?', (False, task_id))
            conn.commit()

        load_tasks(conn, task_listbox)

    except ValueError as e:
        # Komunikat błędu związany z próbą ponownego oznaczenia niezrobionego zadania
        messagebox.showerror("Błąd", str(e))