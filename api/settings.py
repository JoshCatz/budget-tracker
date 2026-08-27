from flask import Blueprint, request, redirect, url_for

from services.settings import read, update
from flask_login import current_user
from services.auth_helper import require_login

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")

@settings_bp.route("/", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        blocked = require_login()
        if blocked:
            return blocked
        return update()
    else:
        return read()