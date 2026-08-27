
from flask import Blueprint, request, redirect, url_for

from services.balances import read, update
from flask_login import current_user
from services.auth_helper import require_login

balances_bp = Blueprint("balances", __name__, url_prefix="/balances")

@balances_bp.route("/", methods=["GET", "POST"])
def balances():
    if request.method == "POST":
        blocked = require_login()
        if blocked:
            return blocked
        return update()
    else:
        return read()

