from flask import Flask, request, render_template, redirect, url_for, session, flash
import sqlite3
import logging

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, template_folder='template')
app.secret_key = 'your_secret_key'  # Replace with your own secret key for session management

def connect_to_database():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    print("Connected to database successfully")
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/books-shelves')
def books_shelves():
    return render_template('books-shelves.html')

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
        print("Table created successfully")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match. Please try again.")
            return redirect(url_for('register'))

        data = (first_name, surname, email, password)

        try:
            with sqlite3.connect('library.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO students (first_name, surname, email, password)
                    VALUES (?, ?, ?, ?)
                ''', data)
                conn.commit()
                logging.info('Record added successfully')
                return redirect('/student-login')
        except sqlite3.IntegrityError:
            flash("Email already exists. Please try again.")
            return redirect(url_for('register'))
        except Exception as e:
            logging.error(f'Error submitting form: {str(e)}')
            flash("An error occurred. Please try again.")
            return redirect(url_for('register'))
    
    return render_template('registration.html')

@app.route('/student-login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            with sqlite3.connect('library.db') as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM students WHERE email = ?', (email,))
                user = cursor.fetchone()

                if user and user['password'] == password:
                    session['user_id'] = user['id']
                    session['user_name'] = f"{user['first_name']} {user['surname']}"
                    logging.info(f'User logged in successfully: {user["email"]}')
                    return redirect('/success')
                else:
                    flash("Invalid email or password. Please try again.")
                    return redirect(url_for('student_login'))
        except Exception as e:
            logging.error(f'Error during login: {str(e)}')
            flash("An error occurred. Please try again.")
            return redirect(url_for('student_login'))

    return render_template('Student-Login.html')

@app.route('/success')
def success():
    return "Login successful!"

@app.route('/error')
def error():
    return "There was an error processing your request."

if __name__ == '__main__':
    init_db()  # Ensure the database and tables are created
    app.run(debug=True)
