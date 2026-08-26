from flask import Flask, render_template
from models import db, Settings
from api.shifts import shifts_bp
from api.settings import settings_bp
from api.allocate import allocate_bp
from api.dashboard import dashboard_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tips.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(shifts_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(allocate_bp)
app.register_blueprint(dashboard_bp)

with app.app_context():
    db.create_all()

    if Settings.query.first() is None:
        db.session.add(
            Settings(
                checking_buffer=100.0,
                debt_payment_amount=250.0
            )
        )
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)