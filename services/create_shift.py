from datetime import datetime
from flask import request, redirect, url_for, render_template

from models import db, Shift


def create_shift_form():
    return render_template("shift_form.html")


def create_shift():
    parsed_date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()

    shift = Shift(
        date=parsed_date,
        shift_type=request.form["shift_type"],
        hours_worked=float(request.form["hours_worked"]),
        cash_tips=float(request.form.get("cash_tips") or 0),
        credit_tips=float(request.form.get("credit_tips") or 0),
    )

    db.session.add(shift)
    db.session.commit()

    return redirect(url_for("shifts.make_shift"))