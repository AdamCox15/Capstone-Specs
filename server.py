from flask import (Flask, render_template, request, flash, session, redirect, url_for)
from model import connect_to_db, db

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "McDavid"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/create_account')
def create_account_page():
    return render_template("create_account.html")

@app.route('/products')
def all_products():
    products = crud.get_products()

    return render_template('products.html', products= products)

@app.route('/products/<product_id>')
def show_product(product_id):

    product = crud.get_product_by_id(product_id)

    return render_template('product_details.html', product = product)

@app.route("/users", methods=["POST"])
def register_user():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash(
            "Account with that email already exists. Please log in or try a different email")
        return redirect('/create_account')
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    return redirect('/login')


@app.route('/cart')
def cartPage():
    if 'user_email' not in session:
        return redirect('/login')
    order_total = 0
    cart_products = []
    cart = session.get("cart", {})
    for product_id, quantity in cart.items():
        product = crud.get_product_by_id(product_id)

        total_cost = quantity * product.price
        order_total += total_cost

        product.quantity = quantity
        product.total_cost = total_cost

        cart_products.append(product)

    return render_template("cart.html", cart_products=cart_products, order_total=order_total)


@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    if 'user_email' not in session:
        return redirect('/login')
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    cart[product_id] = cart.get(product_id, 0) + 1
    session.modified = True
    flash(f"Product {product_id} successfully added to cart.")
    print(cart)

    return redirect("/cart")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(port="5430", debug=True)
