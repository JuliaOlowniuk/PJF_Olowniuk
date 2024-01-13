import tkinter as tk
from tkinter import ttk
from add import add_task

class WeeklyPlanner:
    def create_widgets(self, parent_frame, conn, task_listbox):
        self.parent_frame = parent_frame
        self.conn = conn
        self.task_listbox = task_listbox
        self.weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        self.weekday_combobox = ttk.Combobox(parent_frame, values=self.weekdays)
        self.weekday_combobox.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.add_task_button = tk.Button(parent_frame, text="Dodaj zadanie do dnia", command=self.add_task_to_day)
        self.add_task_button.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    def add_task_to_day(self):
        selected_weekday = self.weekday_combobox.get()
        if selected_weekday:
            add_task(self.conn, self.task_listbox, priority=1, due_date=selected_weekday)