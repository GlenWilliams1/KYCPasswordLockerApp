from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm, LoginForm, SecurityQuestionsForm
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
csrf = CSRFProtect(app)

# SQLite database connection
conn = sqlite3.connect('database.db')
cur = conn.cursor()

# database schema 
cur.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    security_question1 TEXT NOT NULL,
    security_answer1 TEXT NOT NULL,
    security_question2 TEXT NOT NULL,
    security_answer2 TEXT NOT NULL
);''')

cur.execute('''CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    record_name TEXT NOT NULL,
    record_username TEXT NOT NULL,
    record_password TEXT NOT NULL
);''')

# Commit changes and close connection
conn.commit()
conn.close()

# Index page route
@app.route('/')
def index():
    return render_template('index.html')

# Registration page route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        security_question1 = form.security_question1.data
        security_answer1 = form.security_answer1.data
        security_question2 = form.security_question2.data
        security_answer2 = form.security_answer2.data
        
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password, security_question1, security_answer1, security_question2, security_answer2) VALUES (?, ?, ?, ?, ?, ?)", (username, password, security_question1, security_answer1, security_question2, security_answer2))
        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cur.fetchone()
        conn.close()
        
        if user:
            session['username'] = username
            return redirect(url_for('security_questions'))
        else:
            return render_template('login.html', form=form, message='Invalid username or password')
    
    return render_template('login.html', form=form)

# Security questions route
@app.route('/security_questions', methods=['GET', 'POST'])
def security_questions():
    if 'username' in session:
        form = SecurityQuestionsForm()
        # Define security questions
        security_questions = [
            "What is your grandmother's name?",
            "What school did you attend?",
            "What is your best friend's name?"
        ]
        
        if request.method == 'POST':
            answer1 = request.form['answer1']
            answer2 = request.form['answer2']
            
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute("SELECT security_question1, security_question2, security_answer1, security_answer2 FROM users WHERE username = ?", (session['username'],))
            questions = cur.fetchone()
            conn.close()
            
            if answer1 == questions[2] and answer2 == questions[3]:
                return redirect(url_for('dashboard'))
            else:
                return render_template('security_questions.html', message='Incorrect answers, please try again', security_questions=security_questions, form=form)
        
        return render_template('security_questions.html', security_questions=security_questions, form=form)
    else:
        return redirect(url_for('login'))

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM records WHERE username = ?", (session['username'],))
        records = cur.fetchall()
        conn.close()
        return render_template('dashboard.html', records=records)
    else:
        return redirect(url_for('login'))

# Adding records route
@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    if 'username' in session:
        form = SecurityQuestionsForm()  # Instantiate the SecurityQuestionsForm
        if request.method == 'POST':
            record_name = request.form['record_name']
            record_username = request.form['record_username']
            record_password = request.form['record_password']
            
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO records (username, record_name, record_username, record_password) VALUES (?, ?, ?, ?)", (session['username'], record_name, record_username, record_password))
            conn.commit()
            conn.close()
            
            return redirect(url_for('dashboard'))
        
        return render_template('add_record.html', form=form)  # Pass the form object to the template
    else:
        return redirect(url_for('login'))

# Deleting records route
@app.route('/delete_record/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    if 'username' in session:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM records WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    # Clear the user's session
    session.clear()
    # Redirect the user to the index page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
