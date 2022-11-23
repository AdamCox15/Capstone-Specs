from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri="sqlite:///hockey_shop.db", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    # flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


class User(db.Model):
    __tablename__= "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.Integer, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Products(db.Model):
    __tablename__='products'

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    product_path = db.Column(db.String)
    price = db.Column(db.Float)
    brand = db.Column(db.String)
    category = db.Column(db.String)

    def __init__(self, name, product_path, price, brand, category):
        self.name = name
        self.product_path = product_path
        self.price = price
        self.brand = brand
        self.category = category

    def __repr__(self):
        return f"<Product product_id= {self.product_id} name = {self.name}>"


class Rating(db.Model):
    __tablename__="ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    product = db.relationship("Products", backref = "ratings")
    user = db.relationship("User", backref = "ratings")

    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
