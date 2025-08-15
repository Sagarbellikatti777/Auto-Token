from flask import Flask, render_template, request, redirect, session
import mysql.connector
import random, string, time

app = Flask(__name__)
app.secret_key = 'secretkey'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Auto Token"
)
cursor = db.cursor()

@app.route('/')
def home():
    if 'token' in session:
        return render_template('index.html', token=session['token'])
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        if user:
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            cursor.execute("UPDATE users SET token=%s WHERE email=%s", (token, email))
            db.commit()
            session['token'] = token
            return redirect('/')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'token' in session:
        token = session['token']
        time.sleep(5)
        session.pop('token', None)
    return redirect('/register')


if __name__ == "__main__":
    app.run(debug=True)