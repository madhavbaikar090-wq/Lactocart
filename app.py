from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lactocart.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# USER TABLE
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

# CREATE DB
with app.app_context():
    db.create_all()

cart = []

# HOME
@app.route("/")
def home():
    return redirect("/login")

# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Fill all fields")
            return redirect("/register")

        existing = User.query.filter_by(username=username).first()
        if existing:
            flash("User already exists")
            return redirect("/register")

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registered successfully! Please login")
        return redirect("/login")

    return render_template("register.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user"] = username
            return redirect("/shop")
        else:
            flash("Invalid username or password")
            return redirect("/login")

    return render_template("login.html")

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# SHOP
@app.route("/shop")
def shop():
    if "user" not in session:
        return redirect("/login")
    return render_template("shop.html", cart=len(cart))

# RUN
if __name__ == "__main__":
    app.run(debug=True)