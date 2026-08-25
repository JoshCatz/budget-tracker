
from flask import request, redirect, url_for, render_template

from models import db, Settings

def read():
    settings = Settings.query.first()
    return render_template("settings.html", settings=settings)

def update():
    settings = Settings.query.first()

    settings.checking_buffer = float(request.form["checking_buffer"])
    settings.debt_payment_amount = float(request.form["debt_payment"])
 
    db.session.commit()
    return redirect(url_for("shifts.read_shifts"))
