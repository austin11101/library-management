from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, template_folder='template')

def connect_to_database():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('registeration.html')

def init_db():
    with sqlite3.connect('library.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                surname TEXT,
                email TEXT,
                password TEXT
            )
        ''')
        conn.commit()

@app.route('/register', methods=['POST'])
def submit_form():
    data = (
        request.form['first_name'],
        request.form['surname'],
        request.form['email'],
        request.form['password']
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
    except Exception as e:
        logging.error(f'Error submitting form: {str(e)}')

    return redirect('/success')

@app.route('/success')
def success():
    return "Registration successful!"

if __name__ == '__main__':
    init_db()  # Ensure the database is initialized
    app.run(debug=True)
