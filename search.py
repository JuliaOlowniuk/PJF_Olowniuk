import tkinter as tk
from tkinter import simpledialog
from datetime import datetime

# Dodaj zmienną globalną do przechowywania oryginalnych zadań przed wyszukiwaniem
oryginalne_zadania = []

def search_task(conn, task_listbox):
    global oryginalne_zadania
    search_query = simpledialog.askstring("Wyszukiwanie", "Wpisz zadanie do wyszukania:")

    if search_query:
        search_query = search_query.lower()
        # Zapisz oryginalne zadania przed wyszukiwaniem
        oryginalne_zadania = load_original_tasks(conn)
        search_results = find_matching_tasks(conn, search_query)
        display_search_results(task_listbox, search_results)

def load_original_tasks(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    return cursor.fetchall()

def undo_search(conn, task_listbox):
    global oryginalne_zadania
    display_search_results(task_listbox, oryginalne_zadania)
    oryginalne_zadania = []  # Wyczyść oryginalne zadania po cofnięciu wyszukiwania

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
        task_text = f"[{'x' if task[2] else ' '}] {task[1]} - Priorytet: {task[3]}"
        # Dodaj napis "Data wyszukiwania:" tylko, jeśli data jest dostępna
        if task[4] is not None and task[4] != '':
            task_text += f" - Data wykonania: {format_due_date(task[4])}"
        task_listbox.insert(tk.END, (task[0], task_text))
def format_due_date(due_date):
    try:
        parsed_date = datetime.strptime(due_date, "%Y-%m-%d")
        return parsed_date.strftime("%d-%m-%Y")
    except ValueError:
        return due_date