from model import db, User, Products, Rating, connect_to_db


def create_user(email, password):

    user = User(email = email, password = password)

    return user

def create_product(name, product_path, price, brand, category):

    product = Products(name = name, product_path=product_path, price=price, brand=brand, category=category)

    return product

def create_rating(user, product, score):

    rating = Rating(user=user, product=product, score=score)

    return rating


if __name__ == '__main__':
    from server import app
    connect_to_db(app)