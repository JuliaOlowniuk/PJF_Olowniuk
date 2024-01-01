import sqlite3
def save_tasks_to_file(conn, filename):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks ORDER BY priority ASC')
        tasks = cursor.fetchall()

        with open(filename, 'w') as file:
            for task in tasks:
                task_text = f"[{'x' if task[2] else ' '}] {task[1]} (Priorytet: {task[3]})"
                file.write(task_text + '\n')

        print(f"Zadania zapisane do pliku {filename} pomyślnie.")
    except sqlite3.Error as e:
        print(f"Błąd SQLite przy zapisywaniu zadań do pliku: {e}")
