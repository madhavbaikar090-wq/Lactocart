from flask import Flask, render_template, request, redirect

app = Flask(__name__)

cart = []
products = {
    "Amul Milk": 30,
    "Mother Dairy Milk": 28,
    "Amul Curd": 35,
    "Mother Dairy Curd": 32,
    "Amul Butter": 55,
    "Heritage Butter": 50,
    "Amul Cheese": 80,
    "Britannia Cheese": 75
}

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def do_login():
    return redirect("/shop")


@app.route("/shop")
def shop():
    return render_template("shop.html")


@app.route("/milk")
def milk():
    return render_template("milk.html")


@app.route("/curd")
def curd():
    return render_template("curd.html")


@app.route("/add_to_cart/<item>")
def add_to_cart(item):
    cart.append(item)
    return redirect("/cart")


@app.route("/cart")
def view_cart():

    total = 0
    items = []

    for item in cart:
        price = products.get(item, 0)
        total += price
        items.append({"name": item, "price": price})

    return render_template("cart.html", items=items, total=total)

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/payment")
def payment():
    return render_template("payment.html")


@app.route("/order")
def order():
    return render_template("order.html")

@app.route("/cheese")
def cheese():
    return render_template("cheese.html")

@app.route("/butter")
def butter():
    return render_template("butter.html")

@app.route("/receipt")
def receipt():

    total = 0
    items = []

    for item in cart:
        price = products.get(item, 0)
        total += price
        items.append({"name": item, "price": price})

    return render_template("receipt.html", items=items, total=total)

if __name__ == "__main__":
    app.run()