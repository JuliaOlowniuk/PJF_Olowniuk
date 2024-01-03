import sqlite3
import tkinter as tk
from tkinter import filedialog
from add import add_task
from done import mark_done
from delete import delete_task
from load import load_tasks
from sort import sort_tasks
from todolist_db import create_table
from search import search_task
from edit import edit_description
from saveToFile import save_tasks_to_file
from theme_manager import set_light_theme, set_dark_theme
from priority_manager import dynamic_priority

class ToDoListApp:
    def initialize(self, root):
        self.root = root
        self.root.title("ToDo List App")

        self.conn = sqlite3.connect('todolist.db')
        create_table(self.conn)

        self.task_entry = tk.Entry(root, width=50)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        self.priority_entry_label = tk.Label(root, text="Priorytet:")
        self.priority_entry_label.grid(row=0, column=1, padx=10, pady=10)

        self.priority_entry = tk.Entry(root, width=5)
        self.priority_entry.grid(row=0, column=2, padx=10, pady=10)

        self.due_date_entry_label = tk.Label(root, text="Data wykonania (YYYY-MM-DD):")
        self.due_date_entry_label.grid(row=0, column=4, padx=10, pady=10)

        self.sort_button = tk.Button(root, text="Sortuj zadania", command=lambda: sort_tasks(self.conn, self.task_listbox))
        self.sort_button.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        self.search_button = tk.Button(root, text="Wyszukaj zadanie", command=lambda: search_task(self.conn, self.task_listbox))
        self.search_button.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

        self.edit_description_button = tk.Button(root, text="Edytuj opis zadania", command=lambda: edit_description(self.conn, self.task_listbox))
        self.edit_description_button.grid(row=2, column=4, padx=10, pady=10, sticky="nsew")

        self.due_date_entry = tk.Entry(root, width=12)
        self.due_date_entry.grid(row=0, column=5, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Dodaj zadanie", command=self.add_task_with_dynamic_priority)
        self.add_button.grid(row=0, column=6, padx=10, pady=10)

        self.task_listbox = tk.Listbox(root, selectmode=tk.SINGLE, height=15, width=80)
        self.task_listbox.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        for i in range(6):
            root.grid_columnconfigure(i, weight=1)

        root.geometry("800x600")

        self.delete_button = tk.Button(root, text="Usuń zadanie", command=self.delete_task)
        self.delete_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.mark_done_button = tk.Button(root, text="Oznacz jako zrobione", command=lambda: mark_done(self.conn, self.task_listbox))
        self.mark_done_button.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        self.save_button = tk.Button(root, text="Zapisz do pliku", command=self.save_tasks_to_file)
        self.save_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.light_button = tk.Button(root, text="Jasny motyw", command=self.set_light_theme)
        self.light_button.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        self.dark_button = tk.Button(root, text="Ciemny motyw", command=self.set_dark_theme)
        self.dark_button.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

        self.load_tasks()

    def load_tasks(self):
        load_tasks(self.conn, self.task_listbox)

    def save_tasks_to_file(self):
        filetypes = [("Text files", "*.txt")]
        file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=filetypes)
        if file:
            filename = file.name
            file.close()
            save_tasks_to_file(self.conn, filename)

    def set_light_theme(self):
        set_light_theme()

    def set_dark_theme(self):
        set_dark_theme()

    def add_task_with_dynamic_priority(self):
        add_task(self.conn, self.task_entry, self.task_listbox, self.priority_entry, self.due_date_entry)
        dynamic_priority(self.conn, self.task_listbox, self.priority_entry)

    def delete_task(self):
        delete_task(self.conn, self.task_listbox)

if tk.TkVersion >= 8.6:
    root = tk.Tk()
else:
    root = tk.Tk(className="ToDo List App")

app = ToDoListApp()
app.initialize(root)
root.mainloop()
