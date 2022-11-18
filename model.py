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
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

class Sticks(db.Model):
    __tablename__='sticks'

    stick_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    stick_path = db.Column(db.String)
    price = db.Column(db.Integer)
    brand = db.Column(db.String)

    def __init__(self, name, stick_path, price, brand):
        self.name = name
        self.stick_path = stick_path
        self.price = price
        self.brand = brand

    def __repr__(self):
        return f"<Stick stick_id= {self.stick_id} name = {self.name}>"

class Skates(db.Model):
    __tablename__='skates'

    skates_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    skate_path = db.Column(db.String)
    price = db.Column(db.Integer)
    brand = db.Column(db.String)

    def __init__(self, name, skate_path, price, brand):
        self.name = name
        self.skate_path = skate_path
        self.price = price
        self.brand = brand 

    def __repr__(self):
        return f"<Skate skate_id= {self.skates_id} name = {self.name}>"

class Gloves(db.Model):
    __tablename__='gloves'

    gloves_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    glove_path = db.Column(db.String)
    price = db.Column(db.Integer)
    brand = db.Column(db.String)

    def __init__(self, name, glove_path, price, brand):
        self.name = name
        self.glove_path = glove_path
        self.price = price
        self.brand = brand 

    def __repr__(self):
        return f"<Glove glove_id= {self.gloves_id} name = {self.name}>"


class Rating(db.Model):
    __tablename__="ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    stick_id = db.Column(db.Integer, db.ForeignKey("sticks.stick_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    skate_id = db.Column(db.Integer, db.ForeignKey("skates.skates_id"))
    glove_id = db.Column(db.Integer, db.ForeignKey("gloves.gloves_id"))

    stick = db.relationship("Sticks", backref = "ratings")
    skate = db.relationship("Skates", backref = "ratings")
    glove = db.relationship("Gloves", backref = "ratings")
    user = db.relationship("User", backref = "ratings")

    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
