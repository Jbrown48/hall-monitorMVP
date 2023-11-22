from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite database setup
DATABASE = "database.db"

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS your_table (id INTEGER PRIMARY KEY, data TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS using_hall_pass (id INTEGER PRIMARY KEY, data TEXT)")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    create_table()

    # Fetch data from the "Using Hall Pass Now" list and update the count
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM using_hall_pass")
    using_hall_pass = cursor.fetchall()
    hall_pass_count = len(using_hall_pass)
    conn.close()

    # Fetch all data for the main list
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM your_table")
    data = cursor.fetchall()
    conn.close()

    return render_template('index.html', data=data, using_hall_pass=using_hall_pass, hall_pass_count=hall_pass_count)

@app.route('/add', methods=['POST'])
def add_data():
    # Add data to the database
    new_data = request.form['new_data']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO your_table (data) VALUES (?)", (new_data,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/check_pass', methods=['POST'])
def check_pass():
    # Check if the entered number is in the database
    hall_pass_number = request.form['check_pass']
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM your_table WHERE data=?", (hall_pass_number,))
    result = cursor.fetchall()
    conn.close()

    # If the number is found, add it to the "Using Hall Pass Now" list
    if result:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO using_hall_pass (data) VALUES (?)", (hall_pass_number,))
        conn.commit()
        conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)