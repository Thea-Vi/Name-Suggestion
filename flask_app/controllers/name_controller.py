from flask import render_template, redirect, request, session

from flask_app import app
from flask_app.models.user import User
from flask_app.models.name import Name

#  --------------- DISPLAY --------------

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


@app.route("/names/<int:id>")
def display_name(id):
    return render_template(
        "name.html",
        logged_in_user = User.get_by_id({"id": session["uuid"]}),
        name = Name.get_one({"id": id})
    )
    
@app.route("/names/<int:id>/edit")
def edit_name(id):
    return render_template(
        "edit_name.html",
        name = Name.get_one({"id": id})
        
    )
#  -------------- ACTION ----------------
# CREATE
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

#  UPDATE
@app.route("/names/<int:id>/update", methods = ["POST"])
def update_name(id):
    if not Name.validate(request.form):
        return redirect(f"/names/{id}/edit")
    
    data = {
        **request.form,
        "id": id
    }
    
    Name.update(data)
    
    return redirect("/dashboard")

# DELETE
@app.route("/names/<int:id>/delete")
def delete_name(id):
    Name.delete({"id":id})
    
    return redirect("/dashboard")