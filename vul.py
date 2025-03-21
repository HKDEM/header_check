import sqlite3
import os
import pickle

# Hardcoded secret (bad practice)
API_KEY = "12345-secret-key"

# Insecure database query (SQL Injection)
def get_user_data(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    query = f"SELECT * FROM users WHERE username = '{username}'"  # Vulnerable to SQL Injection
    cursor.execute(query)
    
    result = cursor.fetchall()
    conn.close()
    
    return result

# Command Injection Vulnerability
def execute_command(user_input):
    os.system("echo " + user_input)  # Vulnerable to command injection

# Insecure Deserialization
def load_user_data(serialized_data):
    return pickle.loads(serialized_data)  # Vulnerable to arbitrary code execution

# Example Usage
if __name__ == "__main__":
    # Simulating user input for SQL Injection
    username = input("Enter username: ")  # Try: ' OR 1=1 --
    print(get_user_data(username))

    # Simulating command injection
    command = input("Enter command: ")  # Try: ; rm -rf /
    execute_command(command)

    # Simulating unsafe deserialization
    malicious_data = b"cos\nsystem\n(S'echo Hacked!'\ntR."  # This executes `echo Hacked!`
    load_user_data(malicious_data)
