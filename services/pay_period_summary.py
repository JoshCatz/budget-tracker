from models import pay_period_start_for, Shift, AllocationRule, AllocationLog, Settings, Destination, PayPeriod, db
from datetime import timedelta, datetime
from flask import redirect, url_for

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

def allocate_money(period_summary):
    # Locations neeed to access by function
    settings = Settings.query.first()
    checking = Destination.query.filter_by(name="checking").first()
    debt = Destination.query.filter_by(name="debt").first()
    savings = Destination.query.filter_by(name="saving").first()
    stocks = Destination.query.filter_by(name="stock").first()

    log = {}
    real_debt_payment = 0.0
    saving_payment = 0.0
    stock_payment = 0.0

    # if total_tips < checking_buffer -> all tips go to checking
    if period_summary["total_tips"] < settings.checking_buffer - checking.current_balance:
        to_checking = period_summary["total_tips"]
        checking.current_balance += to_checking

    # if total_tips - checking_buffer - debt_payment_amt < 0 -> allocate funds to checking then rest to debt
    elif period_summary["total_tips"] - (settings.checking_buffer - checking.current_balance) - settings.debt_payment_amount <= 0:
        to_checking = settings.checking_buffer - checking.current_balance
        checking.current_balance += to_checking
        real_debt_payment = period_summary["total_tips"] - to_checking
        debt.current_balance += real_debt_payment
    else:
        # CHECKING ALLOCATION #
        to_checking = settings.checking_buffer - checking.current_balance
        checking.current_balance += to_checking

        # DEBT ALLOCATION #
        real_debt_payment = settings.debt_payment_amount
        debt.current_balance += real_debt_payment

        remainder = period_summary["total_tips"] - to_checking - real_debt_payment

        # SAVINGS ALLOCATION #
        saving_rule = AllocationRule.query.filter_by(destination_id=savings.id).first()
        saving_payment = remainder * (saving_rule.percentage / 100)
        savings.current_balance += saving_payment

        # STOCKS ALLOCATION #
        stock_rule = AllocationRule.query.filter_by(destination_id=stocks.id).first()
        stock_payment = remainder * (stock_rule.percentage / 100)
        stocks.current_balance += stock_payment

    # UPDATE PAYPERIOD TABLE #
    pay_period_snapshot = PayPeriod(
        start_date=period_summary["period_start"],
        is_finalized=True,
        real_debt_payment=real_debt_payment,
        total_tips=period_summary["total_tips"],
        checking_buffer_used=settings.checking_buffer,
        debt_payment_target=settings.debt_payment_amount
    )
    db.session.add(pay_period_snapshot)

    # UPDATE ALLOCATION LOG #
    log[checking.id] = to_checking
    log[debt.id] = real_debt_payment
    log[savings.id] = saving_payment
    log[stocks.id] = stock_payment

    for account, value in log.items():
        account_log = AllocationLog(
            destination_id=account,
            pay_period_start=period_summary["period_start"],
            amount=value
        )
        db.session.add(account_log)

    db.session.commit()

    return redirect(url_for("dashboard.read_dashboard"))










