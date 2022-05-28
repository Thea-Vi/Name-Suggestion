from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt

from flask_app import app
from flask_app.models.user import User

bycrypt = Bcrypt(app)

@app.route("/")
def index():
    
    if "uuid" in session:
        return redirect("/dashboard")

    
    return render_template("index.html")


@app.route("/register", methods = ["POST"])
def register():
    if not User.register_validator(request.form):
        return redirect("/")
    
    hash_hash = bycrypt.generate_password_hash(request.form["password"])
    data = {
        **request.form,
        # needs to add "password" since **request.form shortcut will rewrite the plain text password
        "password": hash_hash
    }
    
    user_id = User.create(data)
    
    # assign the user_id to session 
    #uuid = unique user id
    # key-value
    session["uuid"] = user_id
    
    return redirect("/dashboard")


@app.route("/login", methods = ["POST"])
def login():
    if not User.login_validator(request.form):
        return redirect("/")
    
    # if inputs valid, get user from database
    # user is an object
    user = User.get_by_email({"email": request.form["email"]})

    # to access the id, use user.id
    session["uuid"] = user.id
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    # clears session
    session.clear()
    
    return redirect("/")

