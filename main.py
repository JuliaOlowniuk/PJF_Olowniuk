import tkinter as tk
from tkinter import messagebox
import sqlite3
from todolist_db import create_table
from add import add_task
from delete import delete_task
from done import mark_done
from load import load_tasks

class ToDoListApp:
    def initialize(self, root):
        self.root = root
        self.root.title("ToDo List App")

        self.conn = sqlite3.connect('todolist.db')
        create_table(self.conn)

        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Dodaj zadanie", command=lambda: add_task(self.conn, self.task_entry, self.task_listbox))
        self.add_button.grid(row=0, column=1, padx=10, pady=10)

        self.task_listbox = tk.Listbox(root, selectmode=tk.SINGLE, height=10, width=50)
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.delete_button = tk.Button(root, text="Usuń zadanie", command=lambda: delete_task(self.conn, self.task_listbox))
        self.delete_button.grid(row=2, column=0, padx=10, pady=10)

        self.mark_done_button = tk.Button(root, text="Oznacz jako zrobione", command=lambda: mark_done(self.conn, self.task_listbox))
        self.mark_done_button.grid(row=2, column=1, padx=10, pady=10)

        self.load_tasks()

    def load_tasks(self):
        load_tasks(self.conn, self.task_listbox)

if tk.TkVersion >= 8.6:
    root = tk.Tk()
else:
    root = tk.Tk(className="ToDoListApp")

app = ToDoListApp()
app.initialize(root)
root.mainloop()