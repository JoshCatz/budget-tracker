from flask import Flask, render_template
from models import db
from api.shifts import shifts_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tips.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(shifts_bp)

@app.route("/")
def dashboard():
    cards=[]
    return render_template("dashboard.html", cards=cards)


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)