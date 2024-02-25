from datetime import datetime
from flask import Flask, render_template, url_for, redirect, request, session
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
app = Flask(__name__)
app.secret_key = b'^9p8A(h]bpJ)4nThp*b9'
db = client.wad_users

def create(username, password):
    db.user.insert_one({
            "username": username,
            "password": password
        })

def check_user():
    return 'username' in session

@app.route('/profile')
def profile():
    if not check_user():
        return redirect(url_for('login'))
    username = session['username']
    return render_template('profile.html', username=username)

@app.route("/")
def index():
    if check_user():
        return redirect(url_for('profile'))
    else:
        return render_template("index.html")

@app.route("/", methods=["GET", "POST"])
def login():
    if check_user():
        return redirect(url_for('profile'))

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = db.user.find_one({'username': username, 'password': password})
        if user:
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            return render_template('index.html', error='Invalid username or password')     
    else:
        return render_template("index.html")


@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)

    
     