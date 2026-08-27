from flask import Flask
from services.seed import seed_defaults
from models import db, Settings
from api.shifts import shifts_bp
from api.settings import settings_bp
from api.allocate import allocate_bp
from api.dashboard import dashboard_bp
from api.balances import balances_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tips.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(shifts_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(allocate_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(balances_bp)

with app.app_context():
    db.create_all()
    seed_defaults()

if __name__ == "__main__":
    app.run(debug=True)