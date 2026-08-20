from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, date

db = SQLAlchemy()

def week_start_for(d):
    """Return the Monday of the week containing date d."""
    return d - timedelta(days=d.weekday())

def pay_period_start_for(d):
    """Return the start day of the pay period"""
    anchor_date = date(2026, 7, 31)
    period = (d - anchor_date).days // 14
    return anchor_date + timedelta(days=(period*14))

class Shift(db.Model):
    __tablename__="shift"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    shift_type = db.Column(db.String(2), nullable=False)
    hours_worked = db.Column(db.Float, nullable=False)
    cash_tips = db.Column(db.Float, nullable=False, default=0.0)
    card_tips = db.Column(db.Float, nullable=False, default=0.0)

    @property
    def week_start(self):
        return week_start_for(self.date)

class Destination(db.Model):
    __tablename__ = "destination"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=True)
    current_balance = db.Column(db.Float, nullable=False, default=0.0)

class AllocationRule(db.Model):
    __tablename__ = "allocation_rule"
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey("destination.id"), nullable=False)
    percentage = db.Column(db.Integer, nullable=False)

    destination = db.relationship("Destination", backref='allocation_rules', )

class Settings(db.Model):
    __tablename__ = "settings"
    id = db.Column(db.Integer, primary_key=True)
    checking_buffer = db.Column(db.Float, default=100.00, nullable=False)
    debt_payment_amount = db.Column(db.Float, default=250.00, nullable=False)

class AllocationLog(db.Model):
    __tablename__ = "allocation_log"
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey("destination.id"), nullable=False)
    pay_period_start = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    destination = db.relationship("Destination", backref="allocation_log")

class PayPeriod(db.Model):
    __tablename__ = "pay_period"
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False, unique=True)
    is_finalized = db.Column(db.Boolean, nullable=False, default=False)
    real_debt_payment = db.Column(db.Float, nullable=False, default=0.0)
    total_tips = db.Column(db.Float, nullable=False, default=0.0)
    checking_buffer_used = db.Column(db.Float, nullable=False)
    debt_payment_target = db.Column(db.Float, nullable=False)