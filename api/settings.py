from flask import Blueprint, request, render_template

from services.settings import read, update

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")

@settings_bp.route("/", methods=["GET"])
def read_settings():
    return read()

@settings_bp.route("/update", methods=["POST"])
def update_settings():
    return update()