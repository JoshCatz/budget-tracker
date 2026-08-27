
from flask import Blueprint, request, render_template
from services.login import login_form, handle_login, handle_logout

login_bp = Blueprint("login", __name__, url_prefix="/")

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return handle_login()
    else:
        return login_form()

    
@login_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        return handle_logout()
    else:
        return login_form()