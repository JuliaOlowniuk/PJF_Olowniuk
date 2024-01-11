import sqlite3
from datetime import datetime, timedelta
from tkinter import simpledialog, messagebox
import schedule
from win10toast import ToastNotifier

def check_due_dates_and_notify(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE due_date IS NOT NULL AND done=0')
    tasks = cursor.fetchall()

    today = datetime.today().date()

    for task in tasks:
        due_date = datetime.strptime(task[4], "%Y-%m-%d").date()
        if due_date == today:
            show_notification(task[1])

def show_notification(task_name):
    toaster = ToastNotifier()
    toaster.show_toast(
        "Zadanie do wykonania!",
        f'Dziś jest termin wykonania zadania: {task_name}',
        duration=10,  # Czas trwania powiadomienia w sekundach
        threaded=True
    )

def set_notification_time(conn, task_listbox):
    task_id = get_selected_task_id(task_listbox)

    if task_id is not None:
        due_date = get_due_date_for_task(conn, task_id)

        if due_date is not None:
            notification_time = simpledialog.askstring("Ustawienie powiadomienia", "Podaj godzinę powiadomienia (HH:MM):")

            if notification_time:
                try:
                    notification_time = datetime.strptime(notification_time, "%H:%M").time()
                    schedule_notification(due_date, notification_time, task_id)
                    messagebox.showinfo("Sukces", "Godzina powiadomienia została ustawiona pomyślnie.")
                except ValueError:
                    messagebox.showerror("Błąd", "Nieprawidłowy format godziny.")
        else:
            messagebox.showerror("Błąd", "To zadanie nie ma ustawionej daty wykonania.")

def schedule_notification(due_date, notification_time, task_id):
    combined_datetime = datetime.combine(due_date, notification_time)
    schedule.every().day.at(combined_datetime.strftime("%H:%M")).do(lambda: show_notification_for_task(task_id))

def show_notification_for_task(task_id):
    conn = sqlite3.connect('todolist.db')  # Utwórz połączenie do bazy danych
    task_name = get_task_name(conn, task_id)
    show_notification(task_name)

def get_task_name(conn, task_id):
    cursor = conn.cursor()
    cursor.execute('SELECT task FROM tasks WHERE id=?', (task_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_due_date_for_task(conn, task_id):
    cursor = conn.cursor()
    cursor.execute('SELECT due_date FROM tasks WHERE id=?', (task_id,))
    result = cursor.fetchone()

    if result and result[0]:
        return datetime.strptime(result[0], "%Y-%m-%d").date()
    else:
        return None

def get_selected_task_id(task_listbox):
    selected_task = task_listbox.curselection()

    if selected_task:
        return task_listbox.get(selected_task[0])[0]
    else:
        return None