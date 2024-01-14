import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
from load import refresh_task_listbox

def display_charts(conn, task_listbox):
    # Okno dialogowe do wyboru rodzaju wykresu
    chart_type = simpledialog.askinteger("Wybierz rodzaj wykresu", "1. Wykres kołowy\n2. Wykres słupkowy", minvalue=1, maxvalue=2)

    if chart_type is None:
        return  # Użytkownik anulował wybór

    # Pobierz dane z listboxa
    tasks = refresh_task_listbox(conn, task_listbox)  # Teraz funkcja refresh_task_listbox zwraca listę zadań

    if tasks is None or len(tasks) == 0:
        messagebox.showinfo('Informacja', 'Brak danych do wyświetlenia wykresu.')
        return  # Upewnij się, że mamy dane do przetwarzania

    # Przetwórz dane z listboxa do postaci, którą można wykorzystać w wykresach

    # Pierwszy wykres - wykres kołowy
    if chart_type == 1:
        # Przykład: Zlicz zadania wykonane i niewykonane
        tasks_completed_count = sum(task[2] for task in tasks)
        tasks_incomplete_count = len(tasks) - tasks_completed_count

        if tasks_completed_count == 0 and tasks_incomplete_count == 0:
            messagebox.showinfo('Informacja', 'Brak danych do wyświetlenia wykresu.')
            return  # Upewnij się, że mamy dane do przetwarzania

        data_pie = {'Status': ['Wykonane', 'Niewykonane'], 'Count': [tasks_completed_count, tasks_incomplete_count]}
        df_pie = pd.DataFrame(data_pie)

        try:
            chart_pie = df_pie.plot.pie(y='Count', labels=df_pie['Status'], autopct='%1.1f%%', startangle=90, legend=False, figsize=(5, 5))
            chart_pie.set_title('Zadania wykonane vs. niewykonane (Wykres kołowy)')
            plt.show(block=False)  # Użyj block=False
        except Exception as e:
            messagebox.showerror('Błąd', f'Wystąpił błąd podczas wyświetlania wykresu kołowego: {str(e)}')

    # Drugi wykres - wykres słupkowy
    elif chart_type == 2:
        # Przykład: Zlicz zadania z datą i bez daty
        tasks_with_date_count = sum(task[4] is not None and task[4] != '' for task in tasks)
        tasks_without_date_count = len(tasks) - tasks_with_date_count

        if tasks_with_date_count == 0 and tasks_without_date_count == 0:
            messagebox.showinfo('Informacja', 'Brak danych do wyświetlenia wykresu.')
            return  # Upewnij się, że mamy dane do przetwarzania

        data_bar = {'Status': ['Z datą', 'Bez daty'], 'Count': [tasks_with_date_count, tasks_without_date_count]}
        df_bar = pd.DataFrame(data_bar)

        try:
            # Utwórz okno z wykresem
            chart_window = tk.Toplevel()

            # Aktualizuj okno główne, aby było gotowe przed utworzeniem nowego okna
            chart_window.update_idletasks()

            # Wyświetl wykres w oknie
            chart_bar = df_bar.plot.bar(x='Status', y='Count', legend=False, color=['green', 'orange'])
            chart_bar.set_title('Zadania z datą vs. zadania bez daty (Wykres słupkowy)')
            plt.show(block=False)

            # Uruchom główną pętlę aplikacji
            chart_window.mainloop()

        except Exception as e:
            messagebox.showerror('Błąd', f'Wystąpił błąd podczas wyświetlania wykresu słupkowego: {str(e)}')