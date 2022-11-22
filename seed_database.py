import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server


os.system("dropdb hockey_shop")
os.system("createdb hockey_shop")

model.connect_to_db(server.app)
model.db.create_all()

with open('data/hockey_shop.json') as f:
    hockey_data = json.loads(f.read())