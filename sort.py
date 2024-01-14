import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime

def sort_tasks(conn, task_listbox):
    result = simpledialog.askstring("Sortowanie",
                                    "Wybierz kryterium sortowania:\n1. Priorytet rosnąco\n2. Priorytet malejąco\n3. Data wykonania rosnąco\n4. Data wykonania malejąco")

    if result:
        if result == "1":
            sort_by_priority_asc(conn, task_listbox)
        elif result == "2":
            sort_by_priority_desc(conn, task_listbox)
        elif result == "3":
            sort_by_due_date_asc(conn, task_listbox)
        elif result == "4":
            sort_by_due_date_desc(conn, task_listbox)
        else:
            tk.messagebox.showwarning("Uwaga", "Nieprawidłowy wybór. Wybierz liczbę od 1 do 4.")


def sort_by_priority_asc(conn, task_listbox):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE due_date IS NOT NULL ORDER BY priority ASC, datetime(due_date) ASC')
    tasks_with_due_date = cursor.fetchall()

    cursor.execute('SELECT * FROM tasks WHERE due_date IS NULL ORDER BY priority ASC')
    tasks_without_due_date = cursor.fetchall()

    display_sorted_tasks(task_listbox, tasks_with_due_date + tasks_without_due_date)


def sort_by_priority_desc(conn, task_listbox):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE due_date IS NOT NULL ORDER BY priority DESC, datetime(due_date) ASC')
    tasks_with_due_date = cursor.fetchall()

    cursor.execute('SELECT * FROM tasks WHERE due_date IS NULL ORDER BY priority DESC')
    tasks_without_due_date = cursor.fetchall()

    display_sorted_tasks(task_listbox, tasks_with_due_date + tasks_without_due_date)


def sort_by_due_date_asc(conn, task_listbox):
    cursor = conn.cursor()
    # Posortuj zadania według daty wykonania (rosnąco) i priorytetu
    cursor.execute('SELECT * FROM tasks ORDER BY due_date IS NOT NULL, datetime(due_date) ASC, priority ASC')
    sorted_tasks = cursor.fetchall()
    # Wybierz zadania bez daty wykonania i dodaj na koniec listy
    cursor.execute('SELECT * FROM tasks WHERE due_date IS NULL')
    tasks_without_due_date = cursor.fetchall()
    sorted_tasks += tasks_without_due_date
    display_sorted_tasks(task_listbox, sorted_tasks)

def sort_by_due_date_desc(conn, task_listbox):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE due_date IS NOT NULL ORDER BY datetime(due_date) DESC, priority ASC')
    tasks_with_due_date = cursor.fetchall()

    cursor.execute('SELECT * FROM tasks WHERE due_date IS NULL')
    tasks_without_due_date = cursor.fetchall()

    display_sorted_tasks(task_listbox, tasks_with_due_date + tasks_without_due_date)

def display_sorted_tasks(task_listbox, tasks):
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_text = f"[{'x' if task[2] else ' '}] {task[1]} - Priorytet: {task[3]}"

        # Dodaj informację o dacie wykonania tylko, jeśli jest dostępna
        if len(task) > 4 and task[4]:
            task_text += f" - Data wykonania: {format_due_date(task[4])}"

        task_listbox.insert(tk.END, (task[0], task_text))

def format_due_date(due_date):
    try:
        parsed_date = datetime.strptime(due_date, "%Y-%m-%d")
        return parsed_date.strftime("%d-%m-%Y")
    except ValueError:
        return due_date


def display_unsorted_tasks(conn, task_listbox):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_text = f"[{'x' if task[2] else ' '}] {task[1]} - Priorytet: {task[3]}"

        # Dodaj informację o dacie wykonania tylko, jeśli jest dostępna
        if len(task) > 4 and task[4]:
            task_text += f" - Data wykonania: {format_due_date(task[4])}"

        task_listbox.insert(tk.END, (task[0], task_text))