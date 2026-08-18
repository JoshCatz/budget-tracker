from flask import Blueprint, request
from services.create_shift import create_shift, create_shift_form

shifts_bp = Blueprint("shifts", __name__, url_prefix="/shifts")

@shifts_bp.route("/create", methods=["GET", "POST"])
def make_shift():
    if request.method == "POST":
        return create_shift()
    else:
        return create_shift_form()