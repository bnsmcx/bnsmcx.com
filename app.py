"""
FILE:       app.py
DATE:       28 APR 2021
AUTHOR:     Ben Simcox
PROJECT:    bnsmcx.com
PURPOSE:    Flask entry point.
"""
import shutil
from csv import DictReader, DictWriter
from datetime import datetime
from flask import Flask, render_template, request, redirect
from passlib.hash import argon2

app = Flask(__name__)
credentials = app.root_path + '/users.csv'
temp_credentials = app.root_path + '/temp_users.csv'
common_passwords = app.root_path + '/CommonPassword.txt'
authentication_logfile = app.root_path + '/authentication.log'
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
        user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        username = request.form['username']
        password = request.form['password']
        if count_users() == 0:
            return render_template('login.html', error="User not found")
        with open(credentials, 'r') as file:
            reader = DictReader(file)
            for row in reader:
                if username == row['username']:
                    if argon2.verify(password, row['password']):
                        response = redirect('/manage')
                        response.set_cookie('session_cookie', row['id'])
                        authenticated_user_sessions[row['id']] = username
                        log_authentication_attempt(True, user_ip, username)
                        return response
                    log_authentication_attempt(False, user_ip, username)
                    return render_template('login.html', error="Invalid Password")
            log_authentication_attempt(False, user_ip, username)
            return render_template('login.html', error="User not found")
    return render_template('login.html', error="")


@app.route('/logout')
def logout():
    """logout the user"""
    cookie = request.cookies.get('session_cookie')
    if cookie in authenticated_user_sessions.keys():
        authenticated_user_sessions.pop(cookie)
    return redirect('/resume')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """accept user info, validate it, and create a new account"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password != request.form['confirm_password']:
            return render_template('register.html', error="Passwords don't match")
        if username_available(username):
            if not is_uncommon_password(password):
                return render_template('register.html',
                                       error="Your password is too common.")
            if not is_complex_password(password):
                return render_template('register.html',
                                       error="""Insufficient password complexity,\n
                                       it must be 12 characters and include at least 1 uppercase,
                                        1 lowercase, 1 number and 1 special character""")
            add_user(username, password)
            return redirect('/login')
        return render_template('register.html', error="Username not available")
    return render_template('register.html', error="")


@app.route('/change_pass', methods=['GET', 'POST'])
def change_pass():
    """change a user's password"""
    if request.method == 'POST':
        username = authenticated_user_sessions[request.cookies.get('session_cookie')]
        password = request.form['password']
        if user_is_authenticated() and password == request.form['confirm_password']:
            if not is_uncommon_password(password):
                return render_template('change_password.html',
                                       error="Your password is too common.")
            if not is_complex_password(password):
                return render_template('change_password.html',
                                       error="""Insufficient password complexity,\n
                                       it must be 12 characters and include at least 1 uppercase,
                                        1 lowercase, 1 number and 1 special character""")
            set_password(username, password)
            return redirect('/manage')
        return render_template('change_password.html', error="Passwords don't match.")
    return render_template('change_password.html', error='')


@app.route('/manage')
def management():
    """force users to the login page if they aren't authenticated"""
    cookie = request.cookies.get('session_cookie')
    if user_is_authenticated():
        user = authenticated_user_sessions[cookie]
        return render_template('management.html', name=user)
    return redirect('/login')


def username_available(username: str) -> bool:
    """check if the username is available"""
    with open(credentials, 'r') as file:
        reader = DictReader(file)
        for row in reader:
            if row['username'] == username:
                return False
    return True


def log_authentication_attempt(successful: bool, user_ip: str, username: str):
    """log an authentication attempt"""
    outcome = 'SUCCESSFUL' if successful else 'FAILED'
    with open(authentication_logfile, 'a') as file:
        file.write(outcome + " login attempt for user " + username
                   + " from " + user_ip + " at " + str(datetime.now()) + "\n")


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
    with open(credentials, 'a+') as file:
        next_id = count_users()
        if next_id > 0:
            file.write('\n')
        file.write('"' + username + '","' + password_hash + '",' + str(count_users()))


def user_is_authenticated() -> bool:
    """check and see if a valid session exists for the user"""
    cookie = request.cookies.get('session_cookie')
    if cookie not in authenticated_user_sessions.keys():
        return False
    return True


def is_uncommon_password(password):
    """check to see if a password is in a file of common passwords"""
    with open(common_passwords, 'r') as file:
        word_list = file.read()
        if password in word_list:
            return False
    return True


def _prep_temp_credentials_file():
    """creates and adds the csv headers to the temp_credentials file"""
    with open(temp_credentials, 'w') as file:
        file.write("username,password,id")
        file.write("\n")


def set_password(username: str, password: str):
    """set the password for a given username"""
    password_hash = argon2.hash(password)
    _prep_temp_credentials_file()
    with open(credentials, 'r') as file, open(temp_credentials, 'a') as temp_file:
        reader = DictReader(file)
        fieldnames = ['username', 'password', 'id']
        writer = DictWriter(temp_file, fieldnames)
        for row in reader:
            if row['username'] == username:
                row['password'] = password_hash
                writer.writerow(row)
            else:
                writer.writerow(row)
    shutil.move(temp_credentials, credentials)


def count_users() -> int:
    """count the number of registered users"""
    users = 0
    with open(credentials, 'r') as file:
        reader = DictReader(file)
        for _ in reader:
            users = reader.line_num
    return users


if __name__ == '__main__':
    app.run()
