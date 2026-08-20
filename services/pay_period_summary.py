from models import pay_period_start_for, Shift, AllocationRule, Settings, Destination, PayPeriod
from datetime import timedelta, datetime


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

period_summary = pay_period_summary(datetime.now().date)

def allocate_money(period_summary):
    if period_summary.total_tips < Settings.checking_buffer:
        # some code to access 'checking' destination and add total_tips to Destination.current_balance
        # no allocation
        pass
    elif period_summary.total_tips - Settings.checking_buffer - Settings.debt_payment_amount <= 0:
        real_debt_payment = period_summary.total_tips - Settings.checking_buffer
        # some code to access 'checking' destination and add checking buffer to Destination.current_balance
        # some code to access 'debt' destination and add remaining balance to Destination.current_balance
        # no allocation
    else:
        # some code to access 'checking' destination and add checking buffer to Destination.current_balance
        # some code to access 'debt' destination and add remaining balance to Destination.current_balance
        # some code to access allocation percentages and apply them to the remaining total_tips and save to Destination
        pass









