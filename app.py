from datetime import datetime
from flask import Flask, render_template, url_for, redirect
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
app = Flask(__name__)
db = client.wad_users

def create(username, password):
    db.user.insert_one({
            "username": username,
            "password": password
        })
    print("Добавлен")

@app.route('/profile')
def profile():
    name="Elizaveta Polukhina"
    time = datetime.now()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', name=name, time=formatted_time)

@app.route('/')
def index():
    return redirect(url_for('profile'))


if __name__ == "__main__":
    #app.run(debug=True)

    
     