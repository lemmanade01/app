import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
from pprint import pprint
from time import sleep

# load environment variables from .env.
load_dotenv()  

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)


def get_playlist_tracks(username, playlist_id):
    """get and return playlist track data from a specific playlist on my Spotify"""

    username = os.environ["SPOTIFY_USERNAME"]
    playlist_id = os.environ["SPOTIFY_PLAYLIST_ID"]

    results = sp.user_playlist_tracks(username,playlist_id)
    
    # create an open dictionary to store retrieved Spotify playlist data
    playlist_tracks = {}
    
    for item in results['items']:
        track = item['track']
        artist_name = track['artists'][0]['name']
        track_name = track['name']
        image_url = track['album']['images'][0]['url']
        spotify_url = track['external_urls']['spotify']
        preview_link = track['preview_url']
        
        # the key for the dictionary playlist_tracks
        track_key = track_name + artist_name
        # assign a list of variables (which are representative of strings) to the key "track_key"
        playlist_tracks[track_key] = [track_name,artist_name, image_url, spotify_url, preview_link]
   
    # return the dictionary
    return playlist_tracks

# def player():
#     scope = "user-read-playback-state,user-modify-playback-state"
#     sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

#     # Shows playing devices
#     res = sp.devices()
#     pprint(res)

#     # Change track
#     sp.start_playback(uris=['spotify:track:6gdLoMygLsgktydTQ71b15'])

#     # Change volume
#     sp.volume(100)
#     sleep(2)
#     sp.volume(50)
#     sleep(2)
#     sp.volume(100)