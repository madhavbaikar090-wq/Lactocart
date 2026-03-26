from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "lacto_secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lactocart.db'
db = SQLAlchemy(app)

# ------------------ DATABASE ------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

# ------------------ PRODUCTS ------------------

products = {
    "milk": [
        {"name": "Amul Gold", "price": 32, "img": "milk.png"},
        {"name": "Amul Taaza", "price": 28, "img": "milk.png"},
        {"name": "Mother Dairy", "price": 30, "img": "milk.png"},
        {"name": "Nestle Milk", "price": 34, "img": "milk.png"}
    ],
    "curd": [
        {"name": "Amul Curd", "price": 40, "img": "curd.png"},
        {"name": "Nestle Curd", "price": 45, "img": "curd.png"},
        {"name": "Mother Dairy Curd", "price": 42, "img": "curd.png"}
    ],
    "butter": [
        {"name": "Amul Butter", "price": 55, "img": "butter.png"},
        {"name": "Britannia Butter", "price": 60, "img": "butter.png"}
    ],
    "cheese": [
        {"name": "Amul Cheese", "price": 65, "img": "cheese.png"},
        {"name": "Go Cheese", "price": 70, "img": "cheese.png"}
    ]
}

# ------------------ ROUTES ------------------

@app.route('/')
def home():
    return redirect('/login')

# REGISTER
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user = User(username=request.form['username'],
                    password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

# LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username'],
            password=request.form['password']
        ).first()

        if user:
            session['user'] = user.username
            session['cart'] = []
            return redirect('/shop')

    return render_template('login.html')

# SHOP
@app.route('/shop')
def shop():
    return render_template('shop.html')

# PRODUCTS
@app.route('/products/<category>')
def products_page(category):
    return render_template('products.html',
                           items=products[category],
                           category=category)

# ADD TO CART
@app.route('/add/<name>/<int:price>')
def add(name, price):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append({"name": name, "price": price})
    session.modified = True
    return redirect('/cart')

# CART
@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

# PAYMENT
@app.route('/payment')
def payment():
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render_template('receipt.html', cart=cart, total=total)

# SEARCH
@app.route('/search', methods=['POST'])
def search():
    query = request.form['search'].lower()
    result = []

    for cat in products:
        for item in products[cat]:
            if query in item['name'].lower():
                result.append(item)

    return render_template('products.html',
                           items=result,
                           category="Search Results")

# ------------------ INIT DB ------------------
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)