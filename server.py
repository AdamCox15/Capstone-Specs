from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "McDavid"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/products')
def all_products():
    products = crud.get_products()

    return render_template('products.html', products= products)

@app.route('/products/,product_id>')
def show_product(product_id):

    product = crud.get_product_by_id(product_id)

    return render_template('product_details.html', product = product)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(port="5420", debug=True)
