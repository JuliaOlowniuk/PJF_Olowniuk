import sqlite3
import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import filedialog, simpledialog, messagebox
import os
from add import add_task
from done import mark_done
from delete import delete_task, update_priorities_after_delete
from load import load_tasks
from sort import sort_tasks
from todolist_db import create_table
from search import search_task
from saveToFile import save_tasks_to_file
from priority_manager import dynamic_priority
from importCSV import import_from_csv
from editTask import edit_task_name
from description import add_description, show_description

class ToDoListApp:
    def initialize(self, root):
        self.root = root
        self.root.title("ToDo List App")

        self.conn = sqlite3.connect('todolist.db')
        create_table(self.conn)

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar_y = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollbar_x = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(self.main_frame, yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar_y.config(command=self.canvas.yview)
        self.scrollbar_x.config(command=self.canvas.xview)

        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)

        self.inner_frame.bind("<Configure>", self.on_frame_configure)

        self.create_widgets()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_widgets(self):
        self.task_entry = tk.Entry(self.inner_frame, width=50)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.priority_entry_label = tk.Label(self.inner_frame, text="Priorytet:")
        self.priority_entry_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.priority_entry = tk.Entry(self.inner_frame, width=5)
        self.priority_entry.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.due_date_entry_label = tk.Label(self.inner_frame, text="Data wykonania (YYYY-MM-DD):")
        self.due_date_entry_label.grid(row=0, column=4, padx=10, pady=10, sticky="w")

        self.calendar_button = tk.Button(self.inner_frame, text="Kalendarz", command=self.open_calendar)
        self.calendar_button.grid(row=0, column=7, padx=10, pady=10, sticky="w")

        self.sort_button = tk.Button(self.inner_frame, text="Sortuj zadania", command=lambda: sort_tasks(self.conn, self.task_listbox))
        self.sort_button.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        self.search_button = tk.Button(self.inner_frame, text="Wyszukaj zadanie", command=lambda: search_task(self.conn, self.task_listbox))
        self.search_button.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

        self.add_description_button = tk.Button(self.inner_frame, text="Dodaj opis", command=lambda: add_description(self.conn, self.task_listbox))
        self.add_description_button.grid(row=2, column=5, padx=10, pady=10, sticky="nsew")

        self.show_description_button = tk.Button(self.inner_frame, text="Pokaż opis", command=lambda: show_description(self.conn, self.task_listbox))
        self.show_description_button.grid(row=2, column=6, padx=10, pady=10, sticky="nsew")

        self.edit_description_button = tk.Button(self.inner_frame, text="Edytuj nazwe zadania", command=lambda: edit_task_name(self.conn, self.task_listbox))
        self.edit_description_button.grid(row=2, column=4, padx=10, pady=10, sticky="nsew")

        self.due_date_entry = tk.Entry(self.inner_frame, width=12)
        self.due_date_entry.grid(row=0, column=5, padx=10, pady=10, sticky="w")

        self.add_button = tk.Button(self.inner_frame, text="Dodaj zadanie", command=self.add_task_with_dynamic_priority)
        self.add_button.grid(row=0, column=6, padx=10, pady=10, sticky="w")

        self.task_listbox_frame = tk.Frame(self.inner_frame)
        self.task_listbox_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.task_listbox_scrollbar = tk.Scrollbar(self.task_listbox_frame, orient=tk.VERTICAL)
        self.task_listbox = tk.Listbox(self.task_listbox_frame, selectmode=tk.SINGLE, width=80, yscrollcommand=self.task_listbox_scrollbar.set)
        self.task_listbox.grid(row=0, column=0, sticky="nsew")

        self.task_listbox_scrollbar.config(command=self.task_listbox.yview)
        self.task_listbox_scrollbar.grid(row=0, column=1, sticky="ns")

        for i in range(6):
            self.inner_frame.grid_columnconfigure(i, weight=1)

        self.delete_button = tk.Button(self.inner_frame, text="Usuń zadanie", command=self.delete_task)
        self.delete_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.mark_done_button = tk.Button(self.inner_frame, text="Oznacz jako zrobione", command=lambda: mark_done(self.conn, self.task_listbox))
        self.mark_done_button.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        self.save_button = tk.Button(self.inner_frame, text="Zapisz do pliku", command=self.save_tasks_to_file)
        self.save_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.import_button = tk.Button(self.inner_frame, text="Importuj dane z CSV", command=self.import_data_from_csv)
        self.import_button.grid(row=3, column=3, padx=10, pady=10, sticky="nsew")

        self.load_tasks()

    def open_calendar(self):
        top = tk.Toplevel()

        def set_due_date():
            selected_date = cal.get_date()
            self.due_date_entry.delete(0, tk.END)
            self.due_date_entry.insert(0, selected_date)
            top.destroy()

        cal = DateEntry(top, width=12, year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
                        date_pattern='yyyy-mm-dd', background='darkblue', foreground='white', borderwidth=2)
        cal.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        confirm_button = tk.Button(top, text="Potwierdź", command=set_due_date)
        confirm_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        def on_closing():
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", on_closing)

    def load_tasks(self):
        load_tasks(self.conn, self.task_listbox)

    def save_tasks_to_file(self):
        filetypes = [("Text files", "*.txt"), ("Excel files", "*.xlsx"), ("Word files", "*.docx")]
        file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=filetypes)
        if file:
            filename = file.name
            file_format = os.path.splitext(filename)[1][1:].lower()
            file.close()
            save_tasks_to_file(self.conn, filename, file_format)

    def add_task_with_dynamic_priority(self):
        priority = dynamic_priority(self.conn, self.task_listbox)
        add_task(self.conn, self.task_entry, self.task_listbox, priority, self.due_date_entry)

    def import_data_from_csv(self):
        import_from_csv(self.conn, self.task_listbox)

    def delete_task(self):
        delete_task(self.conn, self.task_listbox)
        update_priorities_after_delete(self.conn, self.task_listbox)

    def add_description(self):
        add_description(self.conn, self.task_listbox)

    def show_description(self):
        show_description(self.conn, self.task_listbox)

if tk.TkVersion >= 8.6:
    root = tk.Tk()
else:
    root = tk.Tk(className="ToDo List App")

app = ToDoListApp()
app.initialize(root)
root.geometry("800x600")
root.resizable(True, True)
root.mainloop()