from model import db, User, Products, Rating, connect_to_db


def create_user(username, email, password):

    user = User(username, email, password)

    return user

def create_product(name, product_path, price, brand, category, info):

    product = Products(name = name, product_path=product_path, price=price, brand=brand, category=category, info=info)

    return product

def create_rating(user, product, score):

    rating = Rating(user=user, product=product, score=score)

    return rating

def get_rating_by_product_id(product_id):
    return Rating.query.filter_by(product_id=product_id).all()

def get_products():
    return Products.query.all()

def get_product_by_id(product_id):
    return Products.query.get(product_id)

def get_product_by_category(category):
    return Products.query.filter_by(category).all()


def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)