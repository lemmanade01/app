"""drops, creates and automatically populate the databse with data"""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb meditations")
os.system("createdb meditations")

model.connect_to_db(server.app)
model.db.create_all()

# Create 10 users
for n in range(10):
    email = f"user{n}@test.com"
    password = "test"

    user = crud.create_user("Bob"+ str(n) ,  "Obo" + str(n) , email, "",password, "Hi")

# create mock meditations with .json file
with open("data/meditations.json") as f:
    meditation_data = json.loads(f.read())

    meditations_in_db = []
    for meditation in meditation_data:
        track_name, artist_name, image_url, spotify_url, preview_link, user_id = (
            meditation["track_name"],
            meditation["artist_name"],
            meditation["image_url"],
            meditation["spotify_url"],
            meditation["preview_link"],
            meditation["user_id"],
        )   

    db_meditation = crud.create_meditations(track_name, artist_name, image_url, spotify_url, preview_link, 1)
    meditations_in_db.append(db_meditation)