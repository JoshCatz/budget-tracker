from models import db, Destination, Settings, AllocationRule


def seed_defaults():
    """Create default Destinations, Settings, and AllocationRules if none exist yet."""

    if Settings.query.first() is None:
        db.session.add(Settings(checking_buffer=100.0, debt_payment_amount=250.0))

    existing_names = {d.name for d in Destination.query.all()}
    defaults = [
        ("checking", "checking"),
        ("debt", "debt"),
        ("saving", "savings"),
        ("stock", "investment"),
    ]
    for name, dtype in defaults:
        if name not in existing_names:
            db.session.add(Destination(name=name, type=dtype, current_balance=0.0))

    db.session.commit()

    savings_dest = Destination.query.filter_by(name="saving").first()
    stock_dest = Destination.query.filter_by(name="stock").first()

    existing_rule_destinations = {r.destination_id for r in AllocationRule.query.all()}
    if savings_dest.id not in existing_rule_destinations:
        db.session.add(AllocationRule(destination_id=savings_dest.id, percentage=60))
    if stock_dest.id not in existing_rule_destinations:
        db.session.add(AllocationRule(destination_id=stock_dest.id, percentage=40))

    db.session.commit()