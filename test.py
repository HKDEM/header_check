import sqlite3
import os
import pickle
from flask import Flask, request

app = Flask(__name__)

# Vulnerable SQL Query (SQL Injection)
def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"  # Vulnerable to SQL Injection
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

# Vulnerable Command Execution (Command Injection)
@app.route("/ping", methods=["GET"])
def ping():
    ip = request.args.get("ip")
    response = os.popen(f"ping -c 1 {ip}").read()  # Vulnerable to Command Injection
    return response

# Vulnerable Deserialization (Pickle)
@app.route("/deserialize", methods=["POST"])
def deserialize():
    data = request.data
    obj = pickle.loads(data)  # Unsafe deserialization
    return str(obj)

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
