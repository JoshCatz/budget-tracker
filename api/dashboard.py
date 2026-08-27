
from flask import Blueprint, request, render_template

from services.dashboard import read

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/")

@dashboard_bp.route("/", methods=["GET"])
def read_dashboard():
    return read()

