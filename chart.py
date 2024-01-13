import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt  # Dodaj ten import
from tkinter import messagebox
from load import load_tasks

def display_pie_chart(conn, task_listbox):
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM tasks WHERE done=?', (True,))
    completed_count = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tasks WHERE done=?', (False,))
    incomplete_count = cursor.fetchone()[0]

    data = {'Status': ['Completed', 'Incomplete'], 'Count': [completed_count, incomplete_count]}
    df = pd.DataFrame(data)

    try:
        chart = df.plot.pie(y='Count', labels=df['Status'], autopct='%1.1f%%', startangle=90, legend=False, figsize=(5, 5))
        chart.set_title('Zadania ukończone vs. nieukończone')
        plt.show()
    except Exception as e:
        messagebox.showerror('Błąd', f'Wystąpił błąd podczas wyświetlania wykresu: {str(e)}')

    load_tasks(conn, task_listbox)  # Przeładuj zadania po wyświetleniu wykresu