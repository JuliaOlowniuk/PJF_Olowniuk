import tkinter as tk
from tkinter import simpledialog
from datetime import datetime

def search_task(conn, task_listbox):
    search_query = simpledialog.askstring("Wyszukiwanie", "Wpisz zadanie do wyszukania:")

    if search_query:
        search_query = search_query.lower()
        search_results = find_matching_tasks(conn, search_query)
        display_search_results(task_listbox, search_results)


def find_matching_tasks(conn, search_query):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()

    # Utwórz listę pasujących zadań
    matching_tasks = [task for task in tasks if search_query in task[1].lower()]

    return matching_tasks


def display_search_results(task_listbox, search_results):
    task_listbox.delete(0, tk.END)
    for task in search_results:
        task_text = f"[{'x' if task[2] else ' '}] {task[1]} - Priorytet: {task[3]} - Data wykonania: {format_due_date(task[4])}"
        task_listbox.insert(tk.END, (task[0], task_text))


def format_due_date(due_date):
    try:
        parsed_date = datetime.strptime(due_date, "%Y-%m-%d")
        return parsed_date.strftime("%d-%m-%Y")
    except ValueError:
        return due_date