from flask import Flask, render_template, request, redirect

app = Flask(__name__)

users = []
cart = []

products = {
    "milk": [
        {"id": 1, "name": "Amul Milk", "price": 30, "image": "milk.png"},
        {"id": 2, "name": "Mother Dairy Milk", "price": 32, "image": "milk.png"}
    ],
    "curd": [
        {"id": 3, "name": "Amul Curd", "price": 25, "image": "curd.png"}
    ],
    "butter": [
        {"id": 4, "name": "Amul Butter", "price": 55, "image": "butter.png"}
    ],
    "cheese": [
        {"id": 5, "name": "Amul Cheese", "price": 80, "image": "cheese.png"}
    ]
}

@app.route("/")
def home():
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users.append({
            "username": request.form["username"],
            "password": request.form["password"]
        })
        return redirect("/login")
    return render_template("register.html", cart=len(cart))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        for u in users:
            if u["username"] == request.form["username"] and u["password"] == request.form["password"]:
                return redirect("/shop")
    return render_template("login.html", cart=len(cart))


@app.route("/shop")
def shop():
    return render_template("shop.html", cart=len(cart))


@app.route("/category/<name>")
def category(name):
    items = products.get(name, [])
    return render_template("category.html", items=items, category=name, cart=len(cart))


@app.route("/add/<int:id>")
def add(id):
    for c in products.values():
        for item in c:
            if item["id"] == id:
                cart.append(item)
    return redirect("/cart")


@app.route("/cart")
def view_cart():
    total = sum(item["price"] for item in cart)
    return render_template("cart.html", cart_items=cart, total=total, cart=len(cart))


@app.route("/payment")
def payment():
    total = sum(item["price"] for item in cart)
    return render_template("receipt.html", cart_items=cart, total=total, cart=len(cart))


@app.route("/search")
def search():
    q = request.args.get("q", "").lower()
    result = []
    for c in products.values():
        for item in c:
            if q in item["name"].lower():
                result.append(item)
    return render_template("category.html", items=result, category="Search Results", cart=len(cart))


if __name__ == "__main__":
    app.run(debug=True)