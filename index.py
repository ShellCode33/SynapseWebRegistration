#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, flash, redirect, render_template, request, session, abort, json
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


@app.route("/thanks")
def thanks():
    return render_template('thanks.html')


@app.route("/register", methods=['POST'])
def register():

    error = None

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_pass = request.form.get("confirm_password")

    if password != confirm_pass:
        error = "Passwords are different"

    if not recaptcha.verify():
        error = "Invalid Captcha"

    if not error:
        pass
        # Register user using ejabberdctl
        # Get the hash from database and store it internally user:hash
        # Remove the hash from the database (user can't login)
        # When the user is approved by an admin, insert the hash where it was to enable the user

    return json.dumps(error);

if __name__ == "__main__":
    print("Running server " + app.config['WEBSITE_NAME'] + "...")
    app.run(host='localhost', port=1337)
    print("Stopping...")
