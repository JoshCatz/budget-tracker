from flask import Blueprint, request, render_template

from services.shifts import check_is_finalized, create, create_form, read, update, update_form, delete

shifts_bp = Blueprint("shifts", __name__, url_prefix="/shifts")

@shifts_bp.route("/create", methods=["GET", "POST"])
def create_shift():
    if request.method == "POST":
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
        return "ERROR"
    
    if request.method == "POST":
        return update(shift_id)
    else:
        return update_form(shift_id)

@shifts_bp.route("/<int:shift_id>/delete", methods=["GET", "POST"])
def delete_shift(shift_id):
    pay_period = check_is_finalized(shift_id)
    if pay_period and pay_period.is_finalized:
        return "ERROR"

    if request.method == "POST":
        return delete(shift_id)

    return read()


