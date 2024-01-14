import tkinter as tk
from tkinter import simpledialog, messagebox
from load import refresh_task_listbox

def add_description(conn, task_listbox):
    selected_task_indices = task_listbox.curselection()

    if not selected_task_indices:
        messagebox.showerror("Błąd", "Wybierz zadanie przed dodaniem opisu.")
        return

    selected_task_index = selected_task_indices[0]
    task_id = task_listbox.get(selected_task_index)[0]

    current_note = get_task_note(conn, task_id)

    new_note = simpledialog.askstring("Dodaj opis", "Wprowadź opis do zadania:", initialvalue=current_note)

    if new_note is not None and new_note != current_note:
        update_task_note(conn, task_id, new_note)
        messagebox.showinfo("Sukces", "Opis zadania został pomyślnie zaktualizowany.")
    elif new_note is not None and new_note == current_note:
        messagebox.showinfo("Informacja", "Opis zadania nie został zmieniony.")

def show_description(conn, task_listbox):
    selected_task_indices = task_listbox.curselection()

    if not selected_task_indices:
        messagebox.showinfo("Opis zadania", "Nie wybrano zadania.")
        return

    selected_task_index = selected_task_indices[0]
    task_id = task_listbox.get(selected_task_index)[0]

    current_note = get_task_note(conn, task_id)

    if current_note:
        messagebox.showinfo("Opis zadania", current_note)
    else:
        messagebox.showinfo("Opis zadania", "Brak opisu dla tego zadania.")

def get_task_note(conn, task_id):
    cursor = conn.cursor()
    cursor.execute('SELECT note FROM tasks WHERE id=?', (task_id,))
    result = cursor.fetchone()
    return result[0] if result and result[0] is not None else ""

def update_task_note(conn, task_id, new_note):
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET note=? WHERE id=?', (new_note, task_id))
    conn.commit()
    # refresh_task_listbox(conn, task_listbox)  # Usunięto automatyczne odświeżanie