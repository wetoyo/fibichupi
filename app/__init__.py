
from flask import Flask, render_template, request, session, redirect, url_for
app = Flask(__name__)
app.secret_key = '5d13cfb7ed33261d8f37a3d1b54632e67c328d6f674a174cefd31ac5d1938e66'

@app.route("/", methods=["GET", "POST"])
def homepage():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("home.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("user_id").strip()
        password = request.form.get("password").strip()
        if auth.user_exists(username):
            if auth.login(username, password):
                session["user_id"] = username
                return redirect(url_for("homepage"))
            else:
                error_msg = "Password is incorrect."
        else:
            error_msg = "User does not exist. Please register."
    return render_template("login.html", error = error_msg)
if __name__ == "__main__":
    app.debug = True
    app.run() 
