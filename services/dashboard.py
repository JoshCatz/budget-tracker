from datetime import datetime, date, timedelta
from flask import request, redirect, url_for, render_template

from models import db, AllocationLog, Shift, PayPeriod, Destination
from services.pay_period_summary import pay_period_summary, pay_period_start_for

def read():
    current_start = pay_period_start_for(date.today())
    cards = []
    for i in range(4):
        period_start = current_start - timedelta(days=14*i)
        destinations = Destination.query.all()
        pay_period = pay_period_summary(period_start)

        existing = PayPeriod.query.filter_by(start_date=pay_period["period_start"]).first()
        is_finalized = existing is not None and existing.is_finalized

        if is_finalized:
            allocations = AllocationLog.query.filter_by(pay_period_start=period_start).all()
            card = {
                "is_finalized": is_finalized,
                "period_start": pay_period["period_start"],
                "period_end": pay_period["period_end"],
                "checking_buffer_used": existing.checking_buffer_used,
                "debt_payment_target": existing.debt_payment_target,
                "real_debt_payment": existing.real_debt_payment,
                "total_tips": existing.total_tips,
                "allocations": allocations,
                "destinations": destinations
            }
        else:
            card = {
                "is_finalized": is_finalized,
                "period_start": pay_period["period_start"],
                "period_end": pay_period["period_end"],
                "total_tips": pay_period["total_tips"],
                "shifts": pay_period["shifts"],
                "destinations": destinations
            }
        cards.append(card)

    return render_template("dashboard.html", cards=cards, destinations=destinations)