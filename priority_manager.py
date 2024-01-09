import tkinter as tk
from load import load_tasks

def dynamic_priority(conn, task_listbox):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE done=0 ORDER BY priority ASC')
        tasks = cursor.fetchall()

        next_priority = 1
        for task in tasks:
            task_id = task[0]
            cursor.execute('UPDATE tasks SET priority=? WHERE id=?', (next_priority, task_id))
            next_priority += 1

        conn.commit()

        load_tasks(conn, task_listbox)

        return next_priority

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def update_priorities_after_delete(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE done=0 ORDER BY priority ASC')
        tasks = cursor.fetchall()

        next_priority = 1
        for task in tasks:
            task_id = task[0]
            cursor.execute('UPDATE tasks SET priority=? WHERE id=?', (next_priority, task_id))
            next_priority += 1

        conn.commit()

    except Exception as e:
        print(f"Wystąpił błąd: {e}")