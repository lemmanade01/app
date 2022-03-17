
import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()
client_id = os.environ["SPOTIPY_CLIENT_ID"]
client_secret = os.environ["SPOTIPY_CLIENT_SECRET"]
auth_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)


def get_playlist_tracks(username, playlist_id):
    """get and return playlist track data from a specific playlist on my Spotify"""

    username = os.environ["SPOTIFY_USERNAME"]
    playlist_id = os.environ["SPOTIFY_PLAYLIST_ID"]

    results = sp.user_playlist_tracks(username, playlist_id)
    
    # Create an open dictionary to store retrieved Spotify playlist data
    playlist_tracks = {}
    
    for item in results['items']:
        track = item['track']
        artist_name = track['artists'][0]['name']
        track_name = track['name']
        image_url = track['album']['images'][0]['url']
        spotify_url = track['external_urls']['spotify']
        preview_link = track['preview_url']
        
        # The key for the dictionary playlist_tracks
        track_key = track_name + artist_name
        # Assign a list of variables (which are representative of strings) to the key "track_key"
        playlist_tracks[track_key] = [track_name,artist_name, image_url, spotify_url, preview_link]
   
    # Return the dictionary
    return playlist_tracks