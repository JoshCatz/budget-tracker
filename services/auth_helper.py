from flask_login import current_user
from flask import redirect, url_for, flash, request


def require_login():
    if not current_user.is_authenticated:
        flash("This action requires sign in.")
        return redirect(request.referrer or url_for("dashboard.read_dashboard"))
    return None