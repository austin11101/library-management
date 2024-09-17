from flask import render_template, request, redirect, url_for
from app import app, bcrypt
import sqlite3
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_to_database():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('registration.html')

def init_db():
    with sqlite3.connect('library.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                surname TEXT,
                email TEXT UNIQUE,
                password TEXT
            )
        ''')
        conn.commit()

@app.route('/', methods=['POST'])
def submit_form():
    # Hash the password before saving
    hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    data = (
        request.form['first_name'],
        request.form['surname'],
        request.form['email'],
        hashed_password
    )

    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO students (first_name, surname, email, password)
                VALUES (?, ?, ?, ?)
            ''', data)
            conn.commit()
            logging.info('Record added successfully')
    except sqlite3.IntegrityError:
        logging.error('Integrity error occurred')
        return redirect('/error')
    except Exception as e:
        logging.error(f'Error submitting form: {str(e)}')
        return redirect('/error')

    return redirect('/success')

@app.route('/success')
def success():
    return "Registration successful!"

@app.route('/error')
def error():
    return "There was an error processing your registration."
