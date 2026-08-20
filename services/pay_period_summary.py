from models import pay_period_start_for, Shift, AllocationRule, Settings, Destination, PayPeriod, db
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
    # Locations neeed to access by function
    settings = Settings.query.first()
    checking = Destination.query.filter_by(name="checking").first()
    debt = Destination.query.filter_by(name="debt").first()

    # if total_tips < checking_buffer -> all tips go to checking
    if period_summary["total_tips"] < settings.checking_buffer - checking.current_balance:
        checking.current_balance += period_summary["total_tips"]

    # if total_tips - checking_buffer - debt_payment_amt < 0 -> allocate funds to checking then rest to debt
    elif period_summary["total_tips"] - (settings.checking_buffer - checking.current_balance) - settings.debt_payment_amount <= 0:
        to_checking = settings.checking_buffer - checking.current_balance
        checking.current_balance += to_checking
        real_debt_payment = period_summary["total_tips"] - to_checking
        debt.current_balance += real_debt_payment
    else:
        # some code to access 'checking' destination and add checking buffer to Destination.current_balance
        # some code to access 'debt' destination and add remaining balance to Destination.current_balance
        # some code to access allocation percentages and apply them to the remaining total_tips and save to Destination
        pass

    db.session.commit()









