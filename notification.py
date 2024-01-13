import sqlite3
from tkinter import simpledialog, messagebox
from plyer import notification
import schedule
from datetime import datetime, timedelta
from tkinter import messagebox

def show_tasks_for_today(conn):
    today = datetime.today().date()
    tasks_for_today = get_tasks_for_date(conn, today)

    if not tasks_for_today:
        messagebox.showinfo("Zadania na dzisiaj", "Brak zaplanowanych zadań na dzisiaj.")
    else:
        tasks_text = "\n".join([f"- {task[1]}" for task in tasks_for_today])
        messagebox.showinfo("Zadania na dzisiaj", f"Zaplanowane zadania na dzisiaj:\n\n{tasks_text}")

def get_tasks_for_date(conn, date):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE due_date=? AND done=0', (date,))
    return cursor.fetchall()

def check_due_dates_and_notify(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE due_date IS NOT NULL AND done=0')
    tasks = cursor.fetchall()

    today = datetime.today().date()

    for task in tasks:
        due_date = datetime.strptime(task[4], "%Y-%m-%d").date()
        if due_date == today:
            show_notification(task[1])

    # Uruchomienie zaplanowanych zadań
    schedule.run_pending()

def show_notification(task_name):
    notification.notify(
        title="Zadanie do wykonania!",
        message=f'Dziś jest termin wykonania zadania: {task_name}',
        timeout=10  # Czas trwania powiadomienia w sekundach
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