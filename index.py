#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_recaptcha import ReCaptcha

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

app.config.from_pyfile('config.py')
recaptcha = ReCaptcha(app=app)

@app.route("/")
def index():
    return render_template('register.html')

@app.route("/register")
def register():

    error = None

    if not recaptcha.verify():
        error = "Invalid Captcha"
    


if __name__ == "__main__":
    print("Running server " + app.config['WEBSITE_NAME'] + "...")
    app.run(host='localhost', port=1337)
    print("Stopping...")
