from datetime import datetime
from flask import request, redirect, url_for, render_template

from models import db, Shift, PayPeriod, pay_period_start_for

### CHECK IF FINALIZED ###
def check_is_finalized(shift_id):
    shift = Shift.query.get_or_404(shift_id)
    period_start = pay_period_start_for(shift.date)
    pay_period = PayPeriod.query.filter_by(start_date=period_start).first()

    return pay_period

### CREATING A SHIFT ###
def create_form():
    return render_template("shift_form.html", shift=None)

def create():
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

    return redirect(url_for("shifts.create_shift"))

### READING SHIFTS ###
def read():
    all_shifts = Shift.query.order_by(Shift.date.desc()).all()
    return render_template("shifts.html", shifts=all_shifts)

### UPDATING A SHIFT ###
def update_form(shift_id):
    shift = Shift.query.get_or_404(shift_id)
    return render_template("shift_form.html", shift=shift)

def update(shift_id):
    shift = Shift.query.get_or_404(shift_id)

    shift.date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
    shift.shift_type = request.form["shift_type"]
    shift.hours_worked = float(request.form["hours_worked"])
    shift.cash_tips = float(request.form.get("cash_tips") or 0)
    shift.card_tips = float(request.form.get("card_tips") or 0)

    db.session.commit()
    return redirect(url_for("shifts.read_shift"))

### DELETING A SHIFT ###
def delete(shift_id):
    shift = Shift.query.get_or_404(shift_id)

    db.session.delete(shift)
    db.session.commit()