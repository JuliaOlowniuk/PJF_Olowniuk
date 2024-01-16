import csv
import sqlite3
from tkinter import filedialog, messagebox
from load import load_tasks
from datetime import datetime

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

            cursor = conn.cursor()
            for row in csv_reader:
                # Wartości w cudzysłowach, oddzielone przecinkiem
                values = row[0].split(',')
                values = [value.strip('"') for value in values]

                if len(values) == 5:  # Oczekuję pięciu wartości w jednym wierszu
                    task, done, priority, due_date, note = values
                    done = bool(
                        int(done)) if done.isdigit() else done.lower() == 'true'  # Konwertuj do wartości logicznej

                    # Sprawdź, czy data została podana
                    if due_date.strip():
                        try:
                            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
                        except ValueError:
                            messagebox.showwarning("Uwaga", f"Nieprawidłowy format daty: {due_date}")
                            return
                    else:
                        due_date = None

                    cursor.execute('INSERT INTO tasks (task, done, priority, due_date, note) VALUES (?, ?, ?, ?, ?)',
                                   (task, done, int(priority), due_date, note))
                else:
                    messagebox.showwarning("Uwaga", "Nieprawidłowy format danych w pliku CSV.")
                    return

        conn.commit()
        load_tasks(conn, task_listbox)  # Załaduj zadania po imporcie
        messagebox.showinfo("Sukces", "Dane zaimportowano pomyślnie.")

    except sqlite3.Error as e:
        messagebox.showerror("Błąd SQLite", f"Błąd SQLite podczas importu danych: {e}")
    except Exception as e:
        messagebox.showerror("Błąd", f"Błąd podczas importu danych: {e}")