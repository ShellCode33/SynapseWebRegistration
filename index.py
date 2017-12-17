from flask import Flask, flash, redirect, render_template, request, session, abort

app = Flask(__name__)
  
@app.route("/")
def index():
    return "Flask App!"

@app.route("/register")
def register():
    return render_template('main.html',name="main")

def main():
    print("Running server...")
    app.run(host='localhost', port=1337)
    print("Stopping...")

if __name__ == "__main__":
    main()
