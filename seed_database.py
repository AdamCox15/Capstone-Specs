import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server


os.system("rm hockey_shop.db")


model.connect_to_db(server.app)
model.db.create_all()

with open('data/products.json') as f:
    hockey_data = json.loads(f.read())

hockey_in_db = []
for hockey in hockey_data:
    name, product_path, price, brand, category = (
        hockey["name"], hockey["product_path"], hockey["price"], hockey["brand"], hockey["category"])
    db_hockey = crud.create_product(name, product_path, price, brand, category)
    hockey_in_db.append(db_hockey)
    print(hockey_in_db)
model.db.session.add_all(hockey_in_db)
model.db.session.commit()