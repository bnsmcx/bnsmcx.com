"""
FILE:       lab6.py
DATE:       28 APR 2021
AUTHOR:     Ben Simcox
PROJECT:    SDEV 300 -- Lab 6
PURPOSE:    Demonstrating flask functionality.
"""

from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def landing_page():
    """render the home page"""
    date_time = datetime.now()
    return render_template('home.html', date_time=date_time)


@app.route('/resume')
def resume():
    """render the resume page"""
    return render_template('resume.html')


@app.route('/blog')
def blog():
    """render the blog page"""
    return render_template('blog.html')


if __name__ == '__main__':
    app.run()
