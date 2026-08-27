
from flask import Blueprint, request, render_template

from services.balances import read, update

balances_bp = Blueprint("balances", __name__, url_prefix="/balances")

@balances_bp.route("/", methods=["GET", "POST"])
def balances():
    if request.method == "POST":
        return update()
    else:
        return read()

