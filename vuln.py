import pickle
import subprocess
import os
import flask

app = flask.Flask(__name__)

# Insecure Deserialization
@app.route('/deserialize', methods=['POST'])
def deserialize():
    data = flask.request.data
    user_data = pickle.loads(data)  # Vulnerable!
    return f"Deserialized: {user_data}"

# Command Injection
@app.route('/execute', methods=['GET'])
def execute():
    command = flask.request.args.get('cmd')
    subprocess.run(command, shell=True, check=True) # Vulnerable!
    return "Command executed"

# Path Traversal
@app.route('/readfile', methods=['GET'])
def readfile():
    filename = flask.request.args.get('filename')
    filepath = os.path.join('/app/files', filename) # Vulnerable!
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "File not found"

# SQL Injection (if you had a database)
# Imagine this connecting to a database.
# @app.route('/users', methods=['GET'])
# def users():
#     username = flask.request.args.get('username')
#     #VULNERABLE!
#     query = f"SELECT * FROM users WHERE username = '{username}'"
#     # ...execute query...
#     return "Database query executed (not really, just imagine)"

# Cross-Site Scripting (XSS)
@app.route('/xss', methods=['GET'])
def xss():
    user_input = flask.request.args.get('input', '')
    return f"<div>
