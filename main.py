#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, flash, redirect, render_template, request, session, abort, json
from flask_recaptcha import ReCaptcha
from subprocess import Popen, PIPE, STDOUT
import hashlib
import threading
import random
import string
import re
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

app.config.from_pyfile('config.py')
recaptcha = ReCaptcha(app=app)
db_connection = None

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

    if not re.match(r"^[a-zA-Z0-9_.-]+$", username):
        error = "Username can only be made of letters, digits and _ . - "

    elif password != confirm_pass:
        error = "Passwords are different"

    elif len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
        error = "Password has to be 8 caracters long and contain caracter(s) plus digit(s)"

    elif len(email) > 0 and not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        error = "Invalid email address"

    elif not recaptcha.verify():
        error = "Invalid Captcha"

    if not error:
        cur = db_connection.cursor()
        cur.execute("SELECT username FROM users_waiting_approval")
        users_waiting = cur.fetchall()
        db_connection.commit()
        users_waiting = [user[0] for user in users_waiting]

        if username in users_waiting:
            error = "User already in registration process"
        else:
            # Register user using register_new_matrix_user program
            p = Popen(["register_new_matrix_user", "-c", app.config["SYNAPSE_CONFIG_FILE"], "https://localhost:" + str(app.config["FEDERATION_PORT"]), "-u", username, "-p", password], stdout=PIPE, stdin=PIPE, stderr=PIPE)
            p.communicate(input="no")
            code = p.wait()

            if code == 1:
                error = "User already registered"

            elif code == 2:
                print("Is SYNAPSE_CONFIG_FILE valid in the config file ?")
                exit(1)

            else:
                # Get the hash from database and store it in the users_waiting_approval table
                cur.execute("SELECT password_hash FROM users WHERE name LIKE ?", ["%"+username+"%"])
                hash = cur.fetchall()[0][0]
                db_connection.commit()
                cur.execute("INSERT INTO users_waiting_approval (username, password, email) VALUES (?, ?, ?)", [username, hash, email])
                db_connection.commit()

                # Remove the hash from database (user can't login until he's approved by an admin)
                cur.execute("UPDATE users SET password_hash = '' WHERE name LIKE ?", ["%"+username+"%"])
                db_connection.commit()

    return json.dumps(error)


@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():

    if 'connected' in session:
        return redirect("/admin", code=302)

    error = None

    if request.method == "POST":
        if not recaptcha.verify():
            error = "Invalid Captcha"

        else:
            password = hashlib.sha512(request.form.get('password').encode("utf-8")).hexdigest()

            if password == app.config["ADMIN_PASSWORD"]:
                session['connected'] = 'ok'
                return redirect("/admin", code=302)
            else:
                error = "Wrong password"

    return render_template('admin_login.html', error=error)


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect("/admin/login", code=302)

@app.route("/admin")
def admin():

    if 'connected' not in session:
        return redirect("/admin/login", code=302)

    # Admin is connected

    cur = db_connection.cursor()
    cur.execute("SELECT username, email FROM users_waiting_approval")
    db_connection.commit()

    return render_template('admin.html', users=cur.fetchall())


@app.route("/approve/<username>")
def approve(username):

    if 'connected' not in session:
        return redirect("/admin/login", code=302)

    cur = db_connection.cursor()
    cur.execute("SELECT password, email FROM users_waiting_approval WHERE username = ?", [username])
    user = cur.fetchall()[0]
    db_connection.commit()

    # Restore hash in database and remove user from waiting table
    cur.execute("UPDATE users SET password_hash = ? WHERE name LIKE ?", [user[0], "%"+username+"%"])
    db_connection.commit()
    cur.execute("DELETE FROM users_waiting_approval WHERE username = ?", [username])
    db_connection.commit()

    # Send email to notify the user (if email specified)
    if user[1] is not None and len(user[1]) > 0:
        msg = MIMEText("Your account %s has been approved on %s" % (username, app.config['MATRIX_DOMAIN']))
        msg['Subject'] = 'Account approved'
        msg['From'] = app.config['EMAIL_FROM']
        msg['To'] = user[1]
        s = smtplib.SMTP(app.config['SMTP_HOST'])
        s.sendmail(app.config["WEBSITE_NAME"], user[1], msg.as_string())
        s.quit()
        print("Email sent to " + user[1])

    return username + " approved."


@app.route("/deny/<username>")
def deny(username):

    if 'connected' not in session:
        return redirect("/admin/login", code=302)

    cur = db_connection.cursor()
    cur.execute("DELETE FROM users_waiting_approval WHERE username = ?", [username])
    db_connection.commit()

    # Unregister user from database maybe coming soon ?
    # A user can't be removed... https://github.com/matrix-org/synapse/issues/1941

    return username + " removed."


# Maybe coming soon
def parse_synapse_yaml():
    pass

def change_config_values():

    # If the admin password in the config file is not hashed, we do it
    # If the SECRET_KEY is not set, we create a random one

    something_changed = False

    lines = []
    config_file = open("config.py", "r")

    for line in config_file:
        if line.startswith("ADMIN_PASSWORD") and len(app.config['ADMIN_PASSWORD']) != 128:
            hashed = hashlib.sha512(app.config['ADMIN_PASSWORD'].encode('utf-8')).hexdigest()
            lines.append("ADMIN_PASSWORD = \"" + hashed + "\"\n")
            app.config['ADMIN_PASSWORD'] = hashed
            something_changed = True

        elif line.startswith("SECRET_KEY") and len(app.config['SECRET_KEY']) == 0:
            new_key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(24)])
            lines.append("SECRET_KEY = \"" + new_key + "\"\n")
            app.config['SECRET_KEY'] = new_key
            something_changed = True

        else:
            lines.append(line)

    config_file.close()

    if something_changed:
        config_file = open("config.py", "w")
        
        for line in lines:
            config_file.write(line)

        config_file.close()


if __name__ == "__main__":

    if len(app.config['ADMIN_PASSWORD']) == 0:
        print("Please choose an admin password.")
        exit(1)

    parse_synapse_yaml()
    change_config_values()

    if(app.config["DB_TYPE"] == "sqlite"):
        import sqlite3
        db_connection = sqlite3.connect(app.config["DB_FILE_SQLITE"])

    elif(app.config["DB_TYPE"] == "postgres"):
        import psycopg2
        try:
            db_connection = psycopg2.connect("dbname='" + app.config["DB_NAME"] + "' user='" + app.config["DB_USER"] + "' host='" + app.config["DB_HOST"] + "' password='" + app.config["DB_PASS"] + "'")
        except:
            print("Can't conect to postgres database")
            exit(1)

    else:
        print(app.config["DB_TYPE"] + " not supported yet.")
        exit(1)


    # Create the required table to store users waiting for approval
    cur = db_connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users_waiting_approval (username VARCHAR(100) NOT NULL PRIMARY KEY, password VARCHAR(128) NOT NULL, email VARCHAR(200))")
    db_connection.commit()

    print("Running server " + app.config['WEBSITE_NAME'] + "...")
    app.run(host='192.168.1.6', port=1337)
    print("Stopping...")

