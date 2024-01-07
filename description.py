import tkinter as tk
from tkinter import simpledialog, messagebox

def add_description(conn, task_listbox):
    selected_task_indices = task_listbox.curselection()

    if selected_task_indices:
        # Pobierz ID zadania z pierwszego zaznaczonego elementu
        selected_task_index = selected_task_indices[0]
        task_id = task_listbox.get(selected_task_index)[0]

        new_note = simpledialog.askstring("Dodaj opis", "Wprowadź opis do zadania:")

        if new_note is not None:
            update_task_note(conn, task_id, new_note)
            refresh_task_listbox(conn, task_listbox)

def show_description(conn, task_listbox):
    selected_task_indices = task_listbox.curselection()

    if selected_task_indices:
        # Pobierz ID zadania z pierwszego zaznaczonego elementu
        selected_task_index = selected_task_indices[0]
        task_id = task_listbox.get(selected_task_index)[0]

        current_note = get_task_note(conn, task_id)
        if current_note is not None:
            tk.messagebox.showinfo("Opis zadania", current_note)
        else:
            tk.messagebox.showinfo("Opis zadania", "Brak opisu dla tego zadania.")

def get_task_note(conn, task_id):
    cursor = conn.cursor()
    cursor.execute('SELECT note FROM tasks WHERE id=?', (task_id,))
    result = cursor.fetchone()
    return result[0] if result else ""

def update_task_note(conn, task_id, new_note):
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET note=? WHERE id=?', (new_note, task_id))
    conn.commit()

def refresh_task_listbox(conn, task_listbox):
    # Nie aktualizuj listy tutaj, zamiast tego zaktualizuj po ponownym kliknięciu na zadanie
    pass