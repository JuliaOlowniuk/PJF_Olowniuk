import tkinter as tk
from tkinter import simpledialog, messagebox
from load import load_tasks

def edit_task_name(conn, task_listbox):
    selected_task_index = task_listbox.curselection()

    if not selected_task_index:
        messagebox.showerror("Błąd", "Wybierz zadanie przed edycją nazwy.")
        return

    task_id = task_listbox.get(selected_task_index)[0]

    cursor = conn.cursor()
    cursor.execute('SELECT task FROM tasks WHERE id=?', (task_id,))
    current_name = cursor.fetchone()[0]

    new_name = simpledialog.askstring("Edytuj zadanie", "Wprowadź nowy opis zadania:", initialvalue=current_name)

    if new_name is not None and new_name != current_name:
        cursor.execute('UPDATE tasks SET task=? WHERE id=?', (new_name, task_id))
        conn.commit()
        load_tasks(conn, task_listbox)
        messagebox.showinfo("Sukces", "Opis zadania został pomyślnie zaktualizowany.")
    elif new_name is not None and new_name == current_name:
        messagebox.showinfo("Informacja", "Opis zadania nie został zmieniony.")