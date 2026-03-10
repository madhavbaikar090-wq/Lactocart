from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def do_login():
    username = request.form["username"]
    password = request.form["password"]

    # simple login check
    if username and password:
        return redirect("/shop")

    return "Login Failed"


@app.route("/shop")
def shop():
    return render_template("shop.html")
@app.route("/milk")
def milk():
    return render_template("milk.html")
if __name__ == "__main__":
    app.run()