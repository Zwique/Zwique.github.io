# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import subprocess




# Initialize Flask app
app = Flask(__name__)
DATABASE = 'database.db'  # Database file

# Function to establish connection to the database
def create_connection():
    conn = sqlite3.connect(DATABASE)
    return conn



# Function to create a users table if it doesn't exist in the database
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    # Create users table with columns: id, username, password
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT NOT NULL,
                      password TEXT NOT NULL,
                      score INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

# Route for the homepage, renders login.html
@app.route('/sign')
def index():
    return render_template('sign.html')

# Route for user signup, handles GET and POST requests
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve username and password from the form
        username = request.form['username']
        password = request.form['password']

        # Insert username and password into the users table
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('scoreboard'))  # Redirect to the homepage after signup

    return render_template('sign.html')  # Render the signup form

# Route for user login, only handles POST requests
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']  # Get username from the form
    password = request.form['password']  # Get password from the form

    conn = create_connection()
    cursor = conn.cursor()
    # Check if the provided username and password exist in the database
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    # Return a success message if user credentials are valid, else return an error message
    if user:
        return render_template('home.html')
    else:
        return "Invalid credentials. Please try again."




@app.route('/')

def home():
    return render_template('home.html')

@app.route('/tools')

def tools():
    return render_template('tools.html')

@app.route('/start')

def start():
    return render_template('start.html')



@app.route('/scoreboard', methods = ['GET'])

def scoreboard():
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT username, score FROM users")
    usernames = cursor.fetchall()
    conn.close()

    return render_template('scoreboard.html', usernames=usernames)
    

@app.route('/game')

def game():

    return render_template('game.html')


@app.route('/run_python_code')
def run_python_code():
    result = subprocess.check_output(['python', 'game.py'])
    return f"Python code executed successfully. Output: {result.decode('utf-8')}"


@app.route('/next')

def next():
    return render_template('next.html')



# Run the Flask app
if __name__ == '__main__':
    create_table()  # Create the users table if it doesn't exist
    app.run(debug=True, port=8080)  # Run the app in debug mode on port 8080



