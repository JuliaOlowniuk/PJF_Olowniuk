import tkinter as tk
from tkinter import simpledialog,messagebox
from datetime import datetime

def sort_tasks(conn, task_listbox):

    result = simpledialog.askstring("Sortowanie", "Wybierz kryterium sortowania:\n1. Priorytet rosnąco\n2. Priorytet malejąco\n3. Data wykonania rosnąco\n4. Data wykonania malejąco")

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
    cursor.execute('SELECT * FROM tasks ORDER BY priority ASC')
    tasks = cursor.fetchall()
    display_sorted_tasks(task_listbox, tasks)

def sort_by_priority_desc(conn, task_listbox):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY priority DESC')
    tasks = cursor.fetchall()
    display_sorted_tasks(task_listbox, tasks)

def sort_by_due_date_asc(conn, task_listbox):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE due_date IS NOT NULL ORDER BY datetime(due_date) ASC')
    tasks = cursor.fetchall()
    display_sorted_tasks(task_listbox, tasks)

def sort_by_due_date_desc(conn, task_listbox):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE due_date IS NOT NULL ORDER BY datetime(due_date) DESC')
    tasks = cursor.fetchall()
    display_sorted_tasks(task_listbox, tasks)

def display_sorted_tasks(task_listbox, tasks):
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_text = f"[{'x' if task[2] else ' '}] {task[1]} - Priorytet: {task[3]} - Data wykonania: {format_due_date(task[4])}"
        task_listbox.insert(tk.END, (task[0], task_text))

def format_due_date(due_date):
    try:
        parsed_date = datetime.strptime(due_date, "%Y-%m-%d")
        return parsed_date.strftime("%d-%m-%Y")
    except ValueError:
        return due_date