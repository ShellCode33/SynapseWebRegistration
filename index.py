#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, flash, redirect, render_template, request, session, abort, json
from flask_recaptcha import ReCaptcha
from flask_mysqldb import MySQL
from subprocess import call

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

app.config.from_pyfile('config.py')
recaptcha = ReCaptcha(app=app)
db = MySQL(app)

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
        users_waiting = {}
        file = open("users_waiting_approval", "r")
        
        for line in file:
            tab = line.split(":")

            if len(tab) == 2:
                users_waiting[tab[0]] = tab[1]

        file.close()

        print("actual: " + str(users_waiting))

        if username in users_waiting:
            error = "User already in registration process"
        else:
            # Register user using ejabberdctl
            code = call(["/usr/sbin/ejabberdctl", "register", username, app.config["XMPP_HOST"], password])

            if code == 1:
                error = "User already registered"
                print(error)
                return json.dumps(error)

            # Get the hash from database and store it internally user:hash
            cur = db.connection.cursor()
            cur.execute("SELECT password FROM users WHERE username = %s", [username])
            hash = cur.fetchall()[0][0]

            users_waiting[username] = hash

            file = open("users_waiting_approval", "w")

            for username in users_waiting:
                file.write(username + ":" + users_waiting[username] + "\n")

            file.close()

            # Remove the hash from the database (user can't login until he's approved by an admin)
            cur.execute("UPDATE users SET password = '' WHERE username = %s", [username])
            db.connection.commit()

    return json.dumps(error)


@app.route("/admin/login")
def admin_login():
    return render_template('admin_login.html')


@app.route("/admin")
def admin():

    # Si la session n'est pas valide, on redirige sur /admin/login qui va demander un mdp

    return render_template('admin.html')


def extract_key_value(config_line):
    tab = config_line.strip().split(": ")

    if len(tab) == 1:
        return tab[0], None

    tab[1] = tab[1].replace("\"", "") # Config lines are already strings within python, so we remove the " read from the config file

    return tab[0], tab[1]

def parse_ejabberd_yml():
    # try to read MySQL parameters
    file = open(app.config['EJABBERD_CONFIG_FILE'], "r")
    
    for line in file:
        if not line.strip().startswith("#"): # If it is not a comment
            key, value = extract_key_value(line)

            # Test if the config file has some requirements

            if key == "auth_method" and value != "sql":
                print("only sql auth method is supported !")
                exit(1)

            if key == "sql_type" and value != "mysql":
                print("MySQL is the only supported DBMS")
                exit(1)

            if key == "auth_password_format" and value != "scram":
                print("scram password format is the only way to secure users' password, please use it.")
                exit(1)


            # Read DB parameters

            if key == "sql_server":
                app.config['MYSQL_HOST'] = value

            elif key == "sql_database":
                app.config['MYSQL_DB'] = value

            elif key == "sql_username":
                app.config['MYSQL_USER'] = value

            elif key == "sql_password":
                app.config['MYSQL_PASSWORD'] = value

            elif key == "sql_port":
                app.config['MYSQL_PORT'] = int(value)

    file.close()


if __name__ == "__main__":
    parse_ejabberd_yml()
    print("Running server " + app.config['WEBSITE_NAME'] + "...")
    app.run(host='localhost', port=1337)
    print("Stopping...")

