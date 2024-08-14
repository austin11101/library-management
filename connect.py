import sqlite3

def connect_to_database():
    # Connect to the SQLite database
    conn = sqlite3.connect('library.db')
    return conn

def insert_student(first_name, surname, email, password):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (first_name, surname, email, password)
        VALUES (?, ?, ?, ?)
    ''', (first_name, surname, email, password))
    conn.commit()
    conn.close()

def fetch_students():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    conn.close()
    return rows

