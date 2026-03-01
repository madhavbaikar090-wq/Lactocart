from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    return f"""
    <div style="text-align:center; margin-top:100px; font-family:Arial;">
        <h1 style="color:#ff9800;">Welcome {username} 🐄🥛</h1>
        <a href="/" style="text-decoration:none; font-size:18px;">Go Back</a>
    </div>
    """

import os

if __name__ == "__main__":
    app.run()