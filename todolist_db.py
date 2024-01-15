import sqlite3
from user_db import create_users_table, hash_password, check_password

def create_table(conn):
    try:
        create_users_table(conn)

        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                task TEXT NOT NULL,
                done BOOLEAN NOT NULL,
                priority INTEGER DEFAULT 0,
                due_date TEXT,
                note TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()
        print("Tabela zadań utworzona pomyślnie.")
    except sqlite3.Error as e:
        print(f"Błąd SQLite przy tworzeniu tabeli zadań: {e}")

def clear_unassigned_tasks(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE user_id IS NULL')
        conn.commit()
        print("Nieprzypisane zadania zostały wyczyszczone.")
    except sqlite3.Error as e:
        print(f"Błąd SQLite przy usuwaniu nieprzypisanych zadań: {e}")