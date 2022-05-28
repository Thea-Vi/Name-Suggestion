from flask import render_template, redirect, request, session

from flask_app import app
from flask_app.models.user import User
from flask_app.models.name import Name

@app.route("/dashboard")
def dashboard():
    
    if "uuid" not in session:
        return redirect("/")
    
    return render_template(  
        "dashboard.html",
        logged_in_user = User.get_by_id({"id": session["uuid"]}),
        all_names = Name.get_all()
        )
    
@app.route("/names/new")
def new_name():
    return render_template("new_name.html")

@app.route("/names/create", methods = ["POST"])
def create_name():
    if not Name.validate(request.form):
        return redirect("/names/new")
    
    data = {
        **request.form,
        "user_id": session["uuid"]
    }
    
    Name.create(data)
    return redirect("/dashboard")