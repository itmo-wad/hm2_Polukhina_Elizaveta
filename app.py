from datetime import datetime
from flask import Flask, render_template, url_for, redirect, request, session, send_from_directory
from pymongo import MongoClient
import hashlib
from gridfs import GridFS
from werkzeug.utils import secure_filename
import os

client = MongoClient('localhost', 27017)
app = Flask(__name__)
app.secret_key = b'^9p8A(h]bpJ)4nThp*b9'
db = client.wad_users
fs = GridFS(db)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def create(username, password):
    db.user.insert_one({
            "username": username,
            "password": password,
            "photo": "default",
            "city": "Not indicated",
            "hobby": "Not indicated"
        })

def check_user():
    return 'username' in session

def hash_password(password):
    # Converting a password into bytes and hashing using SHA-256
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password

@app.route('/profile')
def profile():
    if not check_user():
        return redirect(url_for('login'))
    username = session['username']
    user = db.user.find_one({"username": username})
    print(user)
    photo = user['photo']
    return render_template('profile.html', username=username, photo=photo, city=user["city"], hobby=user["hobby"])


#Authorisation
@app.route("/", methods=["GET", "POST"])
def login():
    if check_user():
        return redirect(url_for('profile'))

    if request.method == "POST":
        username = request.form['username']
        password = hash_password(request.form['password'])
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


#Registration
@app.route("/registration")
def reg_form():
    return render_template("registration.html")



@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form['username']
        user = db.user.find_one({'username': username})
        if user:
            return render_template("registration.html", error="User with this username is exist. Please, try again")
        else:
            password = hash_password(request.form['password'])
            create(username, password)
            return render_template('index.html', username=username) 

@app.route("/change_pass", methods=["GET", "POST"])
def change_pass():
    username = session['username']
    user = db.user.find_one({'username': username})
    old_password = hash_password(request.form['old_password'])
    if user['password'] == old_password:
        new_password = hash_password(request.form['new_password'])
        db.user.update_one({'username': username}, {'$set': {'password': new_password}})
    return redirect(url_for("profile"))




@app.route("/edit", methods=["GET", "POST"])
def edit_info():
    username = session['username']
    user = db.user.find_one({'username': username})
    if request.form['city']:
        city = request.form['city']
        db.user.update_one({'username': username}, {'$set': {'city': city}})

    if request.form['hobby']:
        db.user.update_one({'username': username}, {'$set': {'hobby': request.form['hobby']}})
    return redirect(url_for("profile"))

@app.route("/edit_photo", methods=['POST'])
def edit_photo():
    if 'new_image' not in request.files:
        pass

    photo = request.files['new_image']

    if photo.filename == '':
        pass

    if photo:
        username = session['username']
        # Сохранение фото в папке uploads на сервере
        filename = secure_filename(photo.filename)
        print(photo)
        print(filename)
        
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(username)
        # Обновление документа пользователя с путем к фотографии
        db.user.update_one({'username': username}, {'$set': {'photo': filename}})

        return redirect(url_for("profile"))



if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)

    
     