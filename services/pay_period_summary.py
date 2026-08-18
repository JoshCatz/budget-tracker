from models import pay_period_start_for, Shift
from datetime import timedelta


def pay_period_summary(d):
    """receives a day as input and returns aggregate data for a given period"""
    # calculate end of pay period
    start_period = pay_period_start_for(d)
    end_period = start_period + timedelta(days=13)

    shifts = Shift.query.filter(Shift.date >= start_period, Shift.date <= end_period).all()

    cash_tips = sum(s.cash_tips for s in shifts)
    card_tips = sum(s.card_tips for s in shifts)
    total_hours = sum(s.hours_worked for s in shifts)

    return {
        "period_start": start_period,
        "period_end": end_period,
        "cash_tips": cash_tips,
        "card_tips": card_tips,
        "total_tips": cash_tips + card_tips,
        "total_hours": total_hours,
        "shifts": shifts
    }







