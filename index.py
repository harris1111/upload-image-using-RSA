from flask import render_template,url_for,redirect
from flask_login.utils import login_required
from __init__ import app
from src.python.api.api_login import *
from src.python.api.api_list_img import *
from flask_login import current_user, login_user

@app.route("/",methods=["Get"])
@login_required
def home():
    return redirect(url_for("list_img"))
 
@app.route("/auth",methods=["Get"])
def auth():
    return render_template("decorators/login.html")

@app.route("/home",methods=["Get"])
@login_required
def list_img():
    return render_template("views/list_image.html")

if(__name__=="__main__"):
    with app.app_context():
        app.run(debug=1)


