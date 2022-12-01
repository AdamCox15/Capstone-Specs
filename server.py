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

    # for product in products:
    #     if(product.category == "Sticks"):
    #         print(product)



    return render_template('products.html', products= products)


@app.route('/products/<product_id>')
def show_product(product_id):
    product = crud.get_product_by_id(product_id)
    rating = crud.get_rating_by_product_id(product_id)
    total = 0

    for r in rating:
        total = total + r.score
    if len(rating) != 0:
        avg = total/len(rating)
    else:
        avg = -1


    return render_template('product_details.html', product = product, rating = rating, avg = avg)

@ app.route("/products/<product_id>/rating", methods=["POST"])
def create_rating(product_id):

    logged_in_email = session.get("user_email")
    rating_score = request.form.get("rating")

    if logged_in_email is None:
        flash("You must log in to rate a product.")
    elif not rating_score:
        flash("Error: you didn't select a score for your rating.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        product = crud.get_product_by_id(product_id)

        rating = crud.create_rating(user, product, int(rating_score))
        db.session.add(rating)
        db.session.commit()

        flash(f"You rated this product {rating_score} out of 5.")

    return redirect(f"/products/{product_id}")

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
        user = crud.create_user(username, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    return redirect('/login')

@app.route("/login", methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect")
    else:
        session['user_email'] = user.email
        flash(f"Welcome Back, {user.username}!")
    return redirect("/")

@app.route("/logout")
def logout():
    del session['user_email']
    session["cart"] = {}
    flash("You're logged out")
    return redirect("/")

@app.route('/cart')
def cartPage():
    if 'user_email' not in session:
        flash("To view cart please login!")
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


@app.route("/empty-cart")
def empty_cart():
    session["cart"] = {}

    return redirect("/cart")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(port="5150", debug=True)
