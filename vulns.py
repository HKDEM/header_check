import os
import subprocess
import pickle
from flask import Flask, request
 
app = Flask(__name__)

# **1. Command Injection Vulnerability**
@app.route('/run', methods=['GET'])
def run_command():
    cmd = request.args.get('cmd')  # Taking user input for command execution
    output = subprocess.check_output(cmd, shell=True)  # **Vulnerable**
    return output

# **2. Insecure Deserialization Vulnerability**
@app.route('/load', methods=['POST'])
def insecure_deserialization():
    data = request.data  # Getting raw request data
    obj = pickle.loads(data)  # **Vulnerable**: Untrusted deserialization
    return str(obj)

# **3. Hardcoded Credentials**
DB_PASSWORD = "SuperSecret123"  # **Vulnerable**: Hardcoded password

# **4. Using MD5 for Password Hashing (Weak Hash Algorithm)**
import hashlib
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()  # **Vulnerable**: MD5 is weak

# **5. SQL Injection**
import sqlite3
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"  # **Vulnerable**
    cursor.execute(query)  # User input directly used in SQL query
    user = cursor.fetchone()
    
    if user:
        return "Login successful"
    else:
        return "Invalid credentials"

if __name__ == '__main__':
    app.run(debug=True)
