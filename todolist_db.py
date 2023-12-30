import sqlite3

def create_table(conn):
    try:
        cursor = conn.cursor()
        # Usuń tabelę, jeśli istnieje
        cursor.execute('DROP TABLE IF EXISTS tasks')
        # Utwórz nową tabelę
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                done BOOLEAN NOT NULL,
                priority INTEGER DEFAULT 0,
                due_date TEXT
            )
        ''')
        conn.commit()
        print("Tabela utworzona pomyślnie.")
    except sqlite3.Error as e:
        print(f"Błąd SQLite przy tworzeniu tabeli: {e}")