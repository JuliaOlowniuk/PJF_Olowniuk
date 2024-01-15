import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import DateEntry
from datetime import datetime
from notification import set_notification_time, show_tasks_for_today
from tkinter import filedialog, messagebox
import os
from add import add_task
from done import mark_done, mark_undone
from delete import delete_task, update_priorities_after_delete
from load import load_tasks
from sort import sort_tasks, display_unsorted_tasks
from todolist_db import create_tables, get_user_by_username, register_new_user, hash_password, check_password
from search import search_task, undo_search
from saveToFile import save_tasks_to_file
from priority_manager import dynamic_priority
from importCSV import import_from_csv
from editTask import edit_task_name
from description import add_description, show_description
from chart import display_charts

class LoginOrRegisterWindow:
    def __init__(self, parent, mode, conn):
        self.parent = parent
        self.root = tk.Toplevel(parent)
        self.conn = conn
        self.root.title("Logowanie / Rejestracja")

        # Pole wprowadzania e-maila
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        # Pole wprowadzania hasła
        self.password_label = tk.Label(self.root, text="Hasło:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack(pady=10)

        # Przycisk "Zaloguj się" lub "Zarejestruj się" w zależności od trybu
        if mode == "login":
            self.action_button = tk.Button(self.root, text="Zaloguj się", command=self.login)
        elif mode == "register":
            self.action_button = tk.Button(self.root, text="Zarejestruj się", command=self.register)
        else:
            raise ValueError("Niewłaściwy tryb")

        self.action_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip().encode('utf-8')

        if not username or not password:
            messagebox.showwarning("Błąd", "Wprowadź username i hasło.")
            return

        user = get_user_by_username(self.conn, username)
        if user and check_password(password, user[2]):
            messagebox.showinfo("Logowanie", "Logowanie udane!")
            self.show_task_list(user[0])  # user[0] to id użytkownika
            self.root.destroy()
        else:
            messagebox.showwarning("Błąd", "Nieprawidłowy username lub hasło.")
    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Błąd", "Wprowadź username i hasło.")
            return
        user = get_user_by_username(self.conn, username)
        if not user:
            if register_new_user(self.conn, username, password):
                messagebox.showinfo("Rejestracja", "Rejestracja udana!")
                user = get_user_by_username(self.conn, username)
                self.show_task_list(user[0])  # user[0] to id użytkownika
                self.root.destroy()
            else:
                messagebox.showwarning("Błąd", "Błąd podczas rejestracji użytkownika.")
        else:
            messagebox.showwarning("Błąd", "Użytkownik o podanym username już istnieje.")

    def show_task_list(self, user_id):
        # Tutaj można dodać kod otwierający główne okno aplikacji ToDoListApp
        todo_app = ToDoListApp()
        todo_app.initialize(self.root)
        todo_app.create_widgets()
        self.root.destroy()

class LoginOrRegisterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ToDo List App")
        self.conn = sqlite3.connect('todolist.db')

        # Przyciski "Zaloguj się" i "Zarejestruj się"
        self.login_button = tk.Button(self.root, text="Zaloguj się", command=lambda: self.show_login_window())
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self.root, text="Zarejestruj się", command=lambda: self.show_register_window())
        self.register_button.pack(pady=10)

    def show_login_window(self):
        login_window = LoginOrRegisterWindow(self.root, mode="login", conn=self.conn)

    def show_register_window(self):
        register_window = LoginOrRegisterWindow(self.root, mode="register", conn=self.conn)

class ToDoListApp:

    def initialize(self, root):
        self.root = tk.Tk()
        self.root.title("ToDo List App")

        self.conn = sqlite3.connect('todolist.db')
        create_tables(self.conn)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.inner_frame = tk.Frame(self.root)
        self.inner_frame.pack(fill=tk.BOTH, expand= True)

        self.create_widgets()

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar_y = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollbar_x = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(self.main_frame, yscrollcommand=self.scrollbar_y.set,
                                xscrollcommand=self.scrollbar_x.set)
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
        # Ustawienie responsywności dla poszczególnych elementów
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

        self.search_button = tk.Button(self.inner_frame, text="Wyszukaj zadanie", command=lambda: search_task(self.conn, self.task_listbox))
        self.search_button.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

        self.display_chart_button = tk.Button(self.inner_frame, text="Wyświetl wykres", command=lambda: display_charts(self.conn, self.task_listbox))
        self.display_chart_button.grid(row=3, column=3, padx=10, pady=10, sticky="nsew")

        self.add_description_button = tk.Button(self.inner_frame, text="Dodaj opis", command=lambda: add_description(self.conn, self.task_listbox))
        self.add_description_button.grid(row=2, column=5, padx=10, pady=10, sticky="nsew")

        self.show_description_button = tk.Button(self.inner_frame, text="Pokaż opis", command=lambda: show_description(self.conn, self.task_listbox))
        self.show_description_button.grid(row=2, column=6, padx=10, pady=10, sticky="nsew")

        self.edit_description_button = tk.Button(self.inner_frame, text="Edytuj nazwę zadania", command=lambda: edit_task_name(self.conn, self.task_listbox))
        self.edit_description_button.grid(row=2, column=4, padx=10, pady=10, sticky="nsew")

        self.due_date_entry = tk.Entry(self.inner_frame, width=12)
        self.due_date_entry.grid(row=0, column=5, padx=10, pady=10, sticky="w")

        self.add_button = tk.Button(self.inner_frame, text="Dodaj zadanie", command=self.add_task_with_dynamic_priority)
        self.add_button.grid(row=0, column=6, padx=10, pady=10, sticky="w")

        self.show_today_button = tk.Button(self.inner_frame, text="Zadania na dzisiaj", command=self.show_tasks_for_today)
        self.show_today_button.grid(row=3, column=5, padx=10, pady=10, sticky="nsew")

        self.task_listbox_frame = tk.Frame(self.inner_frame)
        self.task_listbox_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.task_listbox_scrollbar = tk.Scrollbar(self.task_listbox_frame, orient=tk.VERTICAL)
        self.task_listbox = tk.Listbox(self.task_listbox_frame, selectmode=tk.SINGLE, width=80,
                                       yscrollcommand=self.task_listbox_scrollbar.set)
        self.task_listbox.grid(row=0, column=0, sticky="nsew")

        self.task_listbox_scrollbar.config(command=self.task_listbox.yview)
        self.task_listbox_scrollbar.grid(row=0, column=1, sticky="ns")

        for i in range(8):
            self.inner_frame.grid_columnconfigure(i, weight=1)

        self.delete_button = tk.Button(self.inner_frame, text="Usuń zadanie", command=self.delete_task)
        self.delete_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.mark_done_button = tk.Button(self.inner_frame, text="Oznacz jako zrobione", command=lambda: mark_done(self.conn, self.task_listbox))
        self.mark_done_button.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        self.undo_search_button = tk.Button(self.inner_frame, text="Cofnij wyszukiwanie", command=lambda: undo_search(self.conn, self.task_listbox))
        self.undo_search_button.grid(row=2, column=7, padx=10, pady=10, sticky="w")

        self.mark_undone_button = tk.Button(self.inner_frame, text="Oznacz jako niezrobione", command=lambda: mark_undone(self.conn, self.task_listbox))
        self.mark_undone_button.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        self.save_button = tk.Button(self.inner_frame, text="Zapisz do pliku", command=self.save_tasks_to_file)
        self.save_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.sort_button = tk.Button(self.inner_frame, text="Sortuj zadania", command=lambda: sort_tasks(self.conn, self.task_listbox))
        self.sort_button.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        self.unsorted_button = tk.Button(self.inner_frame, text="Nieposortowane zadania", command=lambda: display_unsorted_tasks(self.conn, self.task_listbox))
        self.unsorted_button.grid(row=3, column=4, padx=10, pady=10, sticky="nsew")

        self.import_button = tk.Button(self.inner_frame, text="Importuj dane z CSV", command=self.import_data_from_csv)
        self.import_button.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

        self.set_notification_button = tk.Button(self.inner_frame, text="Ustaw powiadomienie", command=lambda: set_notification_time(self.conn, self.task_listbox))
        self.set_notification_button.grid(row=2, column=8, padx=10, pady=10, sticky="nsew")

        self.weekly_planner_frame = tk.Frame(self.inner_frame)

        self.load_tasks()

    def adjust_font_size(self, event):
        # Przykładowe dostosowanie rozmiaru czcionki
        new_font_size = int(self.root.winfo_width() / 30)

        # Dostosuj rozmiar czcionki dla elementów
        self.task_entry.config(font=("Helvetica", new_font_size))
        self.priority_entry_label.config(font=("Helvetica", new_font_size))
        self.priority_entry.config(font=("Helvetica", new_font_size))
        # Dodaj resztę elementów do dostosowania

    def adjust_widgets(self, event):
        # Przykładowe dostosowanie rozmiaru czcionki
        new_font_size = int(self.root.winfo_width() / 30)

        # Dostosuj rozmiar czcionki dla elementów
        for widget in [
            self.task_entry, self.priority_entry_label, self.priority_entry,
            self.due_date_entry_label, self.calendar_button, self.search_button,
            self.display_chart_button, self.add_description_button,
            self.show_description_button, self.edit_description_button, self.due_date_entry,
            self.add_button, self.show_today_button, self.delete_button,
            self.mark_done_button, self.undo_search_button, self.mark_undone_button,
            self.save_button, self.sort_button, self.unsorted_button, self.import_button,
            self.set_notification_button, self.weekly_planner_frame, self.change_view_button,
            self.weekday_combobox,
            self.task_listbox_frame, self.task_listbox, self.mark_done_button,
            self.undo_search_button, self.mark_undone_button,
            self.save_button,self.sort_button,
            self.unsorted_button,self.import_button,
            self.set_notification_button,
            self.weekly_planner_frame,self.change_view_button,
            self.weekday_combobox

        ]:
            widget.config(font=("Helvetica", new_font_size))
            widget.grid(row=0, column=0, sticky="nsew")

        # Dostosuj rozmiar okna
        new_width = int(self.root.winfo_width() / 1.5)
        new_height = int(self.root.winfo_height() / 1.5)
        self.root.geometry(f"{new_width}x{new_height}")

    def open_calendar(self):
        top = tk.Toplevel()

        def set_due_date():
            selected_date = cal.get_date()
            self.due_date_entry.delete(0, tk.END)
            self.due_date_entry.insert(0, selected_date)
            top.destroy()

        cal = DateEntry(top, width=12, year=datetime.now().year, month=datetime.now().month,
                        day=datetime.now().day,
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
        # Pobierz zadanie
        task = self.task_entry.get().strip()

        # Pobierz priorytet
        priority_entry_value = self.priority_entry.get().strip()

        if priority_entry_value:
            try:
                priority = int(priority_entry_value)
            except ValueError:
                messagebox.showwarning("Uwaga", "Priorytet musi być liczbą całkowitą!")
                return
        else:
            # Jeśli pole priorytetu jest puste, uzyskaj priorytet dynamicznie
            priority = dynamic_priority(self.conn, self.task_listbox)

        # Sprawdź, czy due_date_entry jest puste
        due_date = self.due_date_entry.get().strip()
        if due_date == "":
            due_date = None  # Ustaw na None, jeśli nie podano

        # Wywołaj funkcję add_task, przekazując odpowiednie argumenty
        add_task(self.conn, self.task_listbox, task, priority, due_date)
    def import_data_from_csv(self):
        import_from_csv(self.conn, self.task_listbox)

    def delete_task(self):
        delete_task(self.conn, self.task_listbox)
        update_priorities_after_delete(self.conn, self.task_listbox)

    def add_description(self):
        add_description(self.conn, self.task_listbox)

    def show_description(self):
        show_description(self.conn, self.task_listbox)

    def show_tasks_for_today(self):
        show_tasks_for_today(self.conn)

    def add_task_to_day(self):
        selected_weekday = self.weekday_combobox.get()
        if selected_weekday:
            add_task(self.conn, self.task_listbox, priority=1, due_date=selected_weekday)

    def add_task_to_week(self):
        selected_weekday = self.weekly_planner_combobox.get()
        if selected_weekday:
           add_task(self.conn, self.task_listbox, priority=1, due_date=selected_weekday)

def run_main_app():
    # Utwórz główne okno programu ToDoListApp
    if tk.TkVersion >= 8.6:
        root = tk.Tk()
    else:
        root = tk.Tk(className="ToDo List App")

    app = ToDoListApp()
    app.initialize(root)
    root.geometry("1500x400")
    root.resizable(True, True)
    root.mainloop()

# Utwórz instancję klasy LoginOrRegisterWindow i uruchom jej metodę run()
login_register_app = LoginOrRegisterApp()
login_register_app.root.geometry("300x200")
login_register_app.root.resizable(False, False)
login_register_app.root.mainloop()