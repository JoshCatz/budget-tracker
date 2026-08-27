from flask import Blueprint, request, redirect, url_for

from services.shifts import check_is_finalized, create, create_form, read, update, update_form, delete
from flask_login import current_user, login_required
from services.auth_helper import require_login

shifts_bp = Blueprint("shifts", __name__, url_prefix="/shifts")

@shifts_bp.route("/create", methods=["GET", "POST"])
def create_shift():
    if request.method == "POST":
        blocked = require_login()
        if blocked:
            return blocked
        return create()
    else:
        return create_form()

@shifts_bp.route("/")
def read_shift():
    return read()

@shifts_bp.route("/<int:shift_id>/update", methods=["GET", "POST"])
def update_shift(shift_id):
    pay_period = check_is_finalized(shift_id)
    if pay_period and pay_period.is_finalized:
        return redirect(url_for("dashboard.read_dashboard"))
    
    if request.method == "POST":
        blocked = require_login()
        if blocked:
            return blocked
        return update(shift_id)
    else:
        return update_form(shift_id)

@shifts_bp.route("/<int:shift_id>/delete", methods=["POST"])
@login_required
def delete_shift(shift_id):
    pay_period = check_is_finalized(shift_id)
    if pay_period and pay_period.is_finalized:
        return redirect(url_for("dashboard.read_dashboard"))
    return delete(shift_id)



