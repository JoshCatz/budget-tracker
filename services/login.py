from flask_login import login_user, logout_user, current_user
from flask import flash, render_template, redirect, url_for, request
from werkzeug.security import check_password_hash
from models import User
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

def login_form():
    return render_template("login_form.html")

def handle_login():
    user = User.query.filter_by(username=request.form["username"]).first()

    if not user:
        flash("Incorrect username or password!")
        return redirect(url_for("login.login"))

    if check_password_hash(user.password_hash, request.form["password"]):
        login_user(user=user, duration=timedelta(days=int(os.environ.get("COOKIE_DURATION", 7))))
        return redirect(url_for("dashboard.read_dashboard"))
    else:
        flash("Incorrect username or password!")
        return redirect(url_for("login.login"))

def handle_logout():
    logout_user()
    return redirect(url_for("login.login"))


    

