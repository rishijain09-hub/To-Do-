import sqlite3
from datetime import datetime


DB_NAME = 'todo.db'

# Task table schema
CREATE_TASKS_TABLE = '''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT 0,
    important BOOLEAN NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    due_date TEXT,
    list_name TEXT,
    priority TEXT
);
'''

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(CREATE_TASKS_TABLE)
    # Add priority column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE tasks ADD COLUMN priority TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    conn.commit()
    conn.close()

# CRUD functions

def add_task(title, due_date=None, list_name='Tasks', priority=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    columns = "title, completed, created_at, due_date, list_name"
    values = [title, 0, datetime.now().isoformat(), due_date, list_name]
    params = values
    if priority:
        columns += ", priority"
        values.append(priority)
        params.append(priority)
    cursor.execute(
        f"INSERT INTO tasks ({columns}) VALUES ({','.join(['?' for _ in values])})",
        params
    )
    conn.commit()
    conn.close()


def get_tasks(filter_by=None, search=None, category=None, list_name=None, sort_by=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT * FROM tasks"
    params = []
    where_clauses = []
    if filter_by == 'completed':
        where_clauses.append("completed = 1")
    elif filter_by == 'pending':
        where_clauses.append("completed = 0")
    if category == 'My Day':
        today = datetime.now().date().isoformat()
        where_clauses.append("due_date = ?")
        params.append(today)

    elif category == 'Planned':
        where_clauses.append("due_date IS NOT NULL")
    elif category == 'Tasks':
        pass
    if list_name:
        where_clauses.append("list_name = ?")
        params.append(list_name)
    if search:
        where_clauses.append("title LIKE ?")
        params.append(f'%{search}%')
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    if category == 'Planned':
        query += " ORDER BY due_date ASC"
    elif sort_by:
        query += f" ORDER BY {sort_by}"
    cursor.execute(query, params)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def edit_task(task_id, title=None, due_date=None, priority=None, list_name=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    updates = []
    params = []
    if title is not None:
        updates.append("title = ?")
        params.append(title)
    if due_date is not None:
        updates.append("due_date = ?")
        params.append(due_date)
    if priority is not None:
        updates.append("priority = ?")
        params.append(priority)
    if list_name is not None:
        updates.append("list_name = ?")
        params.append(list_name)
    if updates:
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        params.append(task_id)
        cursor.execute(query, params)
        conn.commit()
    conn.close()


def update_task_status(task_id, completed):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (int(completed), task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def get_task_by_id(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

def create_list(list_name):
    # No separate table, just add tasks with new list_name
    return list_name

def get_lists():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT list_name FROM tasks")
    lists = [row[0] for row in cursor.fetchall() if row[0]]
    conn.close()
    return lists

