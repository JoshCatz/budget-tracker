from flask import Blueprint, request, render_template

from services.settings import read, update

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")

@settings_bp.route("/", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        return update()
    else:
        return read()