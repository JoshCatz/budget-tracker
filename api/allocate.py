from flask import Blueprint, request, redirect, url_for
from services.pay_period_summary import allocate_money, pay_period_summary
from models import PayPeriod, pay_period_start_for
from datetime import datetime
from flask_login import login_required

allocate_bp = Blueprint("allocation", __name__, url_prefix="/allocate")

@allocate_bp.route("/<date>", methods=["POST"])
@login_required
def allocate(date):
    if request.method == "POST":
        d = datetime.strptime(date, "%Y-%m-%d").date()
        pay_period = PayPeriod.query.filter_by(start_date=pay_period_start_for(d)).first()

        if pay_period and pay_period.is_finalized == True:
            return redirect(url_for("dashboard.read_dashboard"))
        else: 
            return allocate_money(pay_period_summary(d))
    else:
        return redirect(url_for("dashboard.read_dashboard"))