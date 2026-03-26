from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lactocart.db"
db = SQLAlchemy(app)

# USER TABLE
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

# CREATE DB
with app.app_context():
    db.create_all()

cart = []

# PRODUCTS (MORE ITEMS)
products = {
    "milk": [
        {"id": 1, "name": "Amul Milk", "price": 30, "image": "milk.png"},
        {"id": 2, "name": "Mother Dairy Milk", "price": 32, "image": "milk.png"},
        {"id": 3, "name": "Nestle Milk", "price": 35, "image": "milk.png"}
    ],
    "curd": [
        {"id": 4, "name": "Amul Curd", "price": 25, "image": "curd.png"},
        {"id": 5, "name": "Mother Dairy Curd", "price": 28, "image": "curd.png"}
    ],
    "butter": [
        {"id": 6, "name": "Amul Butter", "price": 55, "image": "butter.png"},
        {"id": 7, "name": "Britannia Butter", "price": 60, "image": "butter.png"}
    ],
    "cheese": [
        {"id": 8, "name": "Amul Cheese", "price": 80, "image": "cheese.png"},
        {"id": 9, "name": "Go Cheese", "price": 90, "image": "cheese.png"}
    ]
}

# HOME
@app.route("/")
def home():
    if "user" in session:
        return redirect("/shop")
    return redirect("/login")

# REGISTER
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = User(username=request.form["username"], password=request.form["password"])
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form["username"],
            password=request.form["password"]
        ).first()

        if user:
            session["user"] = user.username
            return redirect("/shop")

    return render_template("login.html")

# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# SHOP
@app.route("/shop")
def shop():
    if "user" not in session:
        return redirect("/login")
    return render_template("shop.html", cart=len(cart))

# CATEGORY
@app.route("/category/<name>")
def category(name):
    return render_template("category.html", items=products.get(name, []), category=name, cart=len(cart))

# SEARCH
@app.route("/search")
def search():
    q = request.args.get("q", "").lower()
    result = []
    for c in products.values():
        for item in c:
            if q in item["name"].lower():
                result.append(item)
    return render_template("category.html", items=result, category="Search Results", cart=len(cart))

# ADD CART
@app.route("/add/<int:id>")
def add(id):
    for c in products.values():
        for item in c:
            if item["id"] == id:
                for cart_item in cart:
                    if cart_item["id"] == id:
                        cart_item["qty"] += 1
                        return redirect("/cart")
                cart.append({"id": id, "name": item["name"], "price": item["price"], "qty": 1})
    return redirect("/cart")

# CART
@app.route("/cart")
def view_cart():
    total = sum(item["price"] * item["qty"] for item in cart)
    return render_template("cart.html", cart_items=cart, total=total, cart=len(cart))

# PAYMENT
@app.route("/payment")
def payment():
    total = sum(item["price"] * item["qty"] for item in cart)
    return render_template("receipt.html", cart_items=cart, total=total, cart=len(cart))

if __name__ == "__main__":
    app.run()