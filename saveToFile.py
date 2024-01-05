import sqlite3
from openpyxl import Workbook
from docx import Document

def save_tasks_to_file(conn, filename, file_format='txt'):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks ORDER BY priority ASC')
        tasks = cursor.fetchall()

        if file_format == 'txt':
            with open(filename, 'w') as file:
                for task in tasks:
                    task_text = f"[{'x' if task[2] else ' '}] {task[1]} (Priorytet: {task[3]})"
                    file.write(task_text + '\n')
            print(f"Zadania zapisane do pliku {filename} pomyślnie.")
        elif file_format == 'xls':
            workbook = Workbook()
            sheet = workbook.active
            sheet.append(['Zadanie', 'Priorytet'])

            for task in tasks:
                task_text = f"[{'x' if task[2] else ' '}] {task[1]}"
                sheet.append([task_text, task[3]])

            workbook.save(filename)
            print(f"Zadania zapisane do pliku {filename} pomyślnie.")
        elif file_format == 'docx':
            document = Document()
            document.add_heading('Zadania', level=1)

            for task in tasks:
                task_text = f"[{'x' if task[2] else ' '}] {task[1]} (Priorytet: {task[3]})"
                document.add_paragraph(task_text)

            document.save(filename)
            print(f"Zadania zapisane do pliku {filename} pomyślnie.")
        else:
            print("Nieprawidłowy format pliku. Wybierz 'txt', 'xls' lub 'docx'.")
    except sqlite3.Error as e:
        print(f"Błąd SQLite przy zapisywaniu zadań do pliku: {e}")