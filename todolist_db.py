import sqlite3
from user_db import create_users_table

def create_table(conn):
    try:

        create_users_table(conn)

        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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