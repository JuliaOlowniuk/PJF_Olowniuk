import sqlite3
import bcrypt

def create_tables(conn):
    try:
        create_users_table(conn)  # Tworzy tabelę użytkowników
        create_tasks_table(conn)  # Tworzy tabelę zadań
        print("Baza danych utworzona pomyślnie.")
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")

def create_users_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()
        print("Tabela users utworzona pomyślnie.")
    except sqlite3.Error as e:
        print(f"Błąd SQLite przy tworzeniu tabeli users: {e}")

def create_tasks_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                task_name TEXT NOT NULL,
                priority INTEGER NOT NULL,
                due_date DATE,
                done BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()
        print("Tabela tasks utworzona pomyślnie.")
    except sqlite3.Error as e:
        print(f"Błąd SQLite przy tworzeniu tabeli tasks: {e}")

def clear_unassigned_tasks(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE user_id IS NULL')
        conn.commit()
        print("Nieprzypisane zadania zostały wyczyszczone.")
    except sqlite3.Error as e:
        print(f"Błąd SQLite przy usuwaniu nieprzypisanych zadań: {e}")

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def get_user_by_email(conn, email):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email=?', (email,))
    user = cursor.fetchone()
    return user

def authenticate_user(conn, email, password):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email=?', (email,))
    user = cursor.fetchone()
    if user and check_password(password, user[2]):
        return user
    else:
        print("Nieprawidłowy e-mail lub hasło.")
        return None

def register_new_user(conn, email, password_hash):
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, password_hash) VALUES (?, ?)', (email, hash_password(password_hash)))
        conn.commit()
        print("Nowy użytkownik zarejestrowany.")
        return True
    except sqlite3.IntegrityError as e:
        print(f"Błąd SQLite przy rejestracji nowego użytkownika: {e}")
        return False