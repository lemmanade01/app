"""drops, creates and automatically populate the databse with data"""

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

# Create 10 users
for n in range(10):
    email = f"user{n}@test.com"
    password = "test"

    user = crud.create_user("Bob"+ str(n) ,  "Obo" + str(n) , email, "",password, "Hi")

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
    
    
    
# Store Spotify track data into database
# username = os.environ["SPOTIFY_USERNAME"]
# playlist_id = os.environ["SPOTIFY_PLAYLIST_ID"]

# playlist_tracks = spotify.get_playlist_tracks(username, playlist_id)

# for track_dict in playlist_tracks:
#     print(track)
#     print("**************")

# def get_playlist_tracks(username, playlist_id):
#     """get and return playlist track data from a specific playlist on my Spotify"""

#     username = os.environ["SPOTIFY_USERNAME"]
#     playlist_id = os.environ["SPOTIFY_PLAYLIST_ID"]

#     results = sp.user_playlist_tracks(username, playlist_id)
    
#     # create an open dictionary to store retrieved Spotify playlist data
#     playlist_tracks = {}
    
#     for item in results['items']:
#         track = item['track']
#         artist_name = track['artists'][0]['name']
#         track_name = track['name']
#         image_url = track['album']['images'][0]['url']
#         spotify_url = track['external_urls']['spotify']
#         preview_link = track['preview_url']
        
#         # the key for the dictionary playlist_tracks
#         track_key = track_name + artist_name
#         # assign a list of variables (which are representative of strings) to the key "track_key"
#         playlist_tracks[track_key] = [track_name,artist_name, image_url, spotify_url, preview_link]
#         # create a track instance and store it into the database
#         db_track = crud.create_meditations(track_name, artist_name, image_url, spotify_url, preview_link, user_id)
   
#     # return the dictionary
#     return playlist_tracks

    
# Create quotes with .json file
with open("data/quotes.json") as f:
    quote_data = json.loads(f.read())

    quotes_in_db = []
    for quote in quote_data:
        inspo_quote, author = (
            quote["inspo_quote"],
            quote["author"],
        )   

        db_quote = crud.create_quotes(inspo_quote, author)
        quotes_in_db.append(db_quote)
        
        
# Create notifications with text message .json file
with open("data/txt_message_notifications.json") as f:
    txt_message_data = json.loads(f.read())

    txt_messages_in_db = []
    for message in txt_message_data:
        txt_message = (
            message["txt_message"],
        )   

        db_txt_message = crud.create_txt_message(txt_message)
        txt_messages_in_db.append(db_txt_message)