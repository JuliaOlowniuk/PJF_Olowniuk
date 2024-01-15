import sqlite3
import bcrypt

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
        print("Tabela użytkowników utworzona pomyślnie.")
    except sqlite3.Error as e:
        print(f"Błąd SQLite podczas tworzenia tabeli użytkowników: {e}")

    # Dodaj kolumnę "email", jeśli nie istnieje
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN email TEXT UNIQUE NOT NULL;')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Błąd SQLite przy dodawaniu kolumny 'email': {e}")
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

def register_new_user(conn, email, password):
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, password_hash) VALUES (?, ?)', (email, hash_password(password)))
        conn.commit()
        print("Nowy użytkownik zarejestrowany.")
        return True
    except sqlite3.IntegrityError as e:
        print(f"Błąd SQLite przy rejestracji nowego użytkownika: {e}")
        return False