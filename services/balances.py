from flask import request, redirect, url_for

from models import db, Destination


def read():
    balances = Destination.query.all()
    balance_cards = []

    for balance in balances:
        current_balance = {
            "name": balance.name,
            "type": balance.type,
            "current_balance": balance.current_balance
        }

        balance_cards.append(current_balance)

    return balance_cards

def update():
    balances = Destination.query.all()

    for balance in balances:
        field_name = f"balance_{balance.id}"
        if field_name in request.form:
            balance.current_balance = float(request.form[field_name])
 
    db.session.commit()

    return redirect(url_for("dashboard.read_dashboard"))
