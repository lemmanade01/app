"""Drops, creates and automatically populate the databse with data"""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import spotify
import server

os.system("dropdb meditations")
os.system("createdb meditations")

model.connect_to_db(server.app)
model.db.create_all()


# Create a mock user
fname = "Ava"
lname = "Williams"
email = "ava34@gmail.com"
phone_num = "3105556710"
password = "Password1"
quote = " "

# Create user
user = crud.create_user(fname, lname, email, phone_num, password, quote)
# Create a meditations catalog for that user with their user id
crud.create_meditations(1)


# Create user's favorites
# meditation_id = 29
# user_id = 1

# fav = crud.create_favorite(meditation_id, user_id)


# Create user's mock journal entries
# with open("data/mock_journal_entries.json") as f:
#     journal_entries = json.loads(f.read())

#     entries_in_db = []
#     for entry in journal_entries:
#         scale, mood, color, gratitude_1, gratitude_2, gratitude_3, journal_input, time_stamp, mnth, user_id = (
#             entry["scale"],
#             entry["mood"],
#             entry["color"],
#             entry["gratitude_1"],
#             entry["gratitude_2"],
#             entry["gratitude_3"],
#             entry["journal_input"],
#             entry["time_stamp"],
#             entry["mnth"],
#             entry["user_id"]
#         )   

#         db_entry = crud.create_journal_entry(scale, mood, color, gratitude_1, gratitude_2, gratitude_3, journal_input, time_stamp, mnth, user_id)
#         entries_in_db.append(db_entry)

    
# Create quotes with .json file
with open("data/quotes.json") as f:
    quote_data = json.loads(f.read())

    quotes_in_db = []
    for quote in quote_data:
        quote_id, inspo_quote, author = (
            quote["quote_id"],
            quote["inspo_quote"],
            quote["author"],
        )   

        db_quote = crud.create_quote(quote_id, inspo_quote, author)
        quotes_in_db.append(db_quote)
        
        
# Create notifications with text message .json file
with open("data/txt_message_notifications.json") as f:
    txt_message_data = json.loads(f.read())

    txt_messages_in_db = []
    for message in txt_message_data:
        message_id, txt_message, reminder_type = (
            message["message_id"],
            message["txt_message"],
            message["reminder_type"]
        ) 

        db_txt_message = crud.create_txt_message(message_id, txt_message, reminder_type)
        txt_messages_in_db.append(db_txt_message)
        
        
# Create wellness tips with .json file
with open("data/wellness_tips.json") as f:
    wellness_tips_data = json.loads(f.read())

    wellness_tips_in_db = []
    for tip in wellness_tips_data:
        tip_id, wellness_tip, source = (
            tip["tip_id"],
            tip["wellness_tip"],
            tip["source"]
        ) 

        db_wellness_tip = crud.create_wellness_tip(tip_id, wellness_tip, source)
        wellness_tips_in_db.append(db_wellness_tip)
        
print("Database has been seeded!")
  

# Create 10 users
# for n in range(10):
#     email = f"user{n}@test.com"
#     password = "test"

#     user = crud.create_user("Bob"+ str(n) ,  "Obo" + str(n) , email, "",password, "Hi")


# create mock meditations with .json file
# with open("data/meditations.json") as f:
#     meditation_data = json.loads(f.read())

#     meditations_in_db = []
#     for meditation in meditation_data:
#         track_name, artist_name, image_url, spotify_url, preview_link, user_id = (
#             meditation["track_name"],
#             meditation["artist_name"],
#             meditation["image_url"],
#             meditation["spotify_url"],
#             meditation["preview_link"],
#             meditation["user_id"],
#         )   

#     db_meditation = crud.create_meditations(track_name, artist_name, image_url, spotify_url, preview_link, 1)
#     meditations_in_db.append(db_meditation)
    