from flask import Flask, request

app = Flask(__name__)

@app.route("/greet")
def greet_user():
    # Vulnerable to XSS
    username = request.args.get('username')
    return f"Hello, {username}!"

if __name__ == '__main__':
    app.run(debug=True)
