"""
FILE:       app.py
DATE:       28 APR 2021
AUTHOR:     Ben Simcox
PROJECT:    bnsmcx.com
PURPOSE:    Flask entry point.
"""
from csv import DictReader
from flask import Flask, render_template, request, redirect
from passlib.hash import argon2

app = Flask(__name__)
credentials = app.root_path + '/users.csv'
authenticated_user_sessions = {}


@app.route('/')
def landing_page():
    """landing page defaults to resume"""
    return resume()


@app.route('/resume')
def resume():
    """render the resume page"""
    return render_template('resume.html')


@app.route('/blog')
def blog():
    """render the blog page"""
    return render_template('blog.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """render the login page and process login attempts"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if count_users() == 0:
            return render_template('login.html', error="User not found")
        with open(credentials, 'r') as f:
            reader = DictReader(f)
            for row in reader:
                if username == row['username']:
                    if argon2.verify(password, row['password']):
                        response = redirect('/manage')
                        response.set_cookie('session_cookie', row['id'])
                        authenticated_user_sessions[row['id']] = username
                        return response
                    else:
                        return render_template('login.html', error="Invalid Password")
            return render_template('login.html', error="User not found")

    return render_template('login.html', error="")


def username_available(username: str) -> bool:
    """check if the username is available"""
    with open(credentials, 'r') as f:
        reader = DictReader(f)
        for row in reader:
            if row['username'] == username:
                return False
    return True


def is_complex_password(password: str) -> bool:
    """check password meets complexity requirements"""
    if len(password) > 11:
        if any(char.isupper() for char in password):
            if any(char.islower() for char in password):
                if any(char.isnumeric() for char in password):
                    if not password.isalnum():
                        return True
    return False


def add_user(username, password):
    """add a new user record to users.csv"""
    password_hash = argon2.hash(password)
    with open(credentials, 'a+') as f:
        next_id = count_users()
        if next_id > 0:
            f.write('\n')
        f.write('"' + username + '","' + password_hash + '",' + str(count_users()))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """accept user info, validate it, and create a new account"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password != request.form['confirm_password']:
            return render_template('register.html', error="Passwords don't match")
        if username_available(username):
            if is_complex_password(password):
                add_user(username, password)
                return redirect('/login')
            else:
                return render_template('register.html',
                                       error="""Insufficient password complexity, 
                                                must be 12 characters and include 
                                                at least 1 uppercase, 1 lowercase, 
                                                1 number and 1 special character"""
                                       )
        else:
            return render_template('register.html', error="Username not available")
    return render_template('register.html', error="")


@app.route('/manage')
def management():
    """force users to the login page if they aren't authenticated"""
    cookie = request.cookies.get('session_cookie')
    if cookie not in authenticated_user_sessions.keys():
        return redirect('/login')
    else:
        user = authenticated_user_sessions[cookie]
        return render_template('management.html', name=user)


def count_users() -> int:
    """count the number of registered users"""
    users = 0
    with open(credentials, 'r') as f:
        reader = DictReader(f)
        for row in reader:
            users = reader.line_num
    return users


@app.route('/logout')
def logout():
    """logout the user"""
    cookie = request.cookies.get('session_cookie')
    if cookie in authenticated_user_sessions.keys():
        authenticated_user_sessions.pop(cookie)
    return redirect('/resume')


if __name__ == '__main__':
    print(count_users())
    app.run()
