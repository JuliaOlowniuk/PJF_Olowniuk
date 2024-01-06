import csv
import sqlite3
from tkinter import filedialog, messagebox
from load import load_tasks

def import_from_csv(conn, task_listbox):
    try:
        # Wybierz plik CSV do importu
        file_path = filedialog.askopenfilename(title="Wybierz plik CSV", filetypes=[("Pliki CSV", "*.csv")])

        if not file_path:
            messagebox.showwarning("Uwaga", "Nie wybrano pliku CSV.")
            return

        # Otwórz plik CSV i przeczytaj dane
        with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Pomijamy nagłówek

            # Iteruj przez wiersze i dodawaj do bazy danych
            cursor = conn.cursor()
            for row in csv_reader:
                task, done, priority, due_date = row
                cursor.execute('INSERT INTO tasks (task, done, priority, due_date) VALUES (?, ?, ?, ?)', (task, int(done), int(priority), due_date))

        conn.commit()
        load_tasks(conn, task_listbox)  # Załaduj zadania po imporcie
        messagebox.showinfo("Sukces", "Dane zaimportowano pomyślnie.")

    except sqlite3.Error as e:
        messagebox.showerror("Błąd SQLite", f"Błąd SQLite podczas importu danych: {e}")
    except Exception as e:
        messagebox.showerror("Błąd", f"Błąd podczas importu danych: {e}")