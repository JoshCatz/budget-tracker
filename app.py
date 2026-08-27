from flask import Flask
from flask_login import LoginManager
from services.seed import seed_defaults, seed_admin_user
from models import db, User
from api.shifts import shifts_bp
from api.settings import settings_bp
from api.allocate import allocate_bp
from api.dashboard import dashboard_bp
from api.balances import balances_bp
from api.login import login_bp

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tips.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

db.init_app(app)
app.register_blueprint(shifts_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(allocate_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(balances_bp)
app.register_blueprint(login_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()
    seed_defaults()
    seed_admin_user()


if __name__ == "__main__":
    app.run(debug=True)