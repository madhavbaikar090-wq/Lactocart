from flask import Flask, render_template, request, redirect

app = Flask(__name__)

cart = []

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
    return render_template("cart.html", cart=cart)


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/payment")
def payment():
    return render_template("payment.html")


@app.route("/order")
def order():
    return render_template("order.html")


if __name__ == "__main__":
    app.run()