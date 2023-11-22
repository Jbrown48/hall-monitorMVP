from flask import Flask, render_template

app = Flask(__name__)

# SQLite database setup
DATABASE = "database.db"

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS your_table (id INTEGER PRIMARY KEY, data TEXT)")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    create_table()
    # Fetch data from the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM your_table")
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', data=data)

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

                                                                                    # Fetch data from the "Using Hall Pass Now" list and update the count
                                                                                        conn = sqlite3.connect(DATABASE)
                                                                                            cursor = conn.cursor()
                                                                                                cursor.execute("SELECT * FROM using_hall_pass")
                                                                                                    using_hall_pass = cursor.fetchall()
                                                                                                        hall_pass_count = len(using_hall_pass)
                                                                                                            conn.close()
