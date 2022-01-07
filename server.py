"""Server for mindfulness app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify, url_for
# from flask_apscheduler import APScheduler
from model import connect_to_db
from datetime import datetime
# from flask_oauthlib.client import OAuth, OAuthException

# from authlib.integrations.flask_client import OAuth

import random
import crud
import json
import requests
import re
import uuid

# import sys
# import subprocess
# from playsound import playsound
import pygame

# import calendar_oauth
# import google.oauth2.credentials
# import google_auth_oauthlib.flow
# import googleapiclient.discovery
# import vlc
# import time

import os
# from twilio.rest import Client

import spotipy
from spotipy import oauth2 
# from spotipy.oauth2 import SpotifyClientCredentials
# SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util

from jinja2 import StrictUndefined



PORT_NUMBER = 5000
SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = 'http://localhost:5000/callback'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'
# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "data/client_secret.json"


# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.events']
SCOPES = ['https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/calendar.events']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'

app = Flask(__name__)
# Required to use Flask sessions
app.secret_key = os.environ['SECRET_KEY']
# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
# scheduler = APScheduler()
app.jinja_env.undefined = StrictUndefined



# oauth = OAuth(app)

# spotify = oauth.remote_app(
#     'spotify',
#     consumer_key=os.environ["SPOTIPY_CLIENT_ID"],
#     consumer_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
#     # Change the scope to match whatever it us you need
#     # list of scopes can be found in the url below
#     # https://developer.spotify.com/web-api/using-scopes/
#     request_token_params={'scope': 'user-read-email'},
#     base_url='https://accounts.spotify.com',
#     request_token_url=None,
#     access_token_url='/api/token',
#     authorize_url='https://accounts.spotify.com/authorize'
# )

@app.route("/")
def show_homepage():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/create-account")
def create_account():
    """Show create account form"""

    return render_template("create_account.html")


@app.route("/handle-create-account", methods=["POST"])
def process_create_account():
    """Log new user into site."""

    fname = request.form.get("fname").capitalize()
    lname = request.form.get("lname").capitalize()
    email = request.form.get("email").lower()
    phone_num = request.form.get("phone-num")
    # username = request.form.get("username")
    password = request.form.get("password")
    quote = request.form.get("quote")
    
    user = crud.get_user_by_email(email)
    # user_username = crud.get_user_by_username(username)

    if user:
        flash("A user already exists with that email.")
        return redirect("/create-account")
    # elif -- how do i check if all required inputs aren't blank
    # Require 10 digit phone number, allowing dashes, and including (area code)
    # elif not re.match("/\d{3}\-\d{3}\-\d{4}/", phone_num):
    #     flash("Please enter a 10 digit phone number, including your area code")
    #     return redirect("/create-account")
  
    # phone_num = phone_num.split("-")
    # phone_num = f"{phone_num[0]}{phone_num[1]}{phone_num[2]}"
    crud.create_user(fname, lname, email, phone_num, password, quote)
    
    user = crud.get_user_by_email(email)
    user_id = user.user_id
    
    crud.create_meditations(user_id)
    
    # crud.create_meditations(track_name, artist_name, image_url, spotify_url, preview_link, user_id)
    
    flash(f"Welcome, {fname.capitalize()}! Please login.")
    return render_template("login.html")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/handle-login", methods=["POST"])
def process_login():
    """Log existing user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """
    
    email = request.form.get("email").lower()
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    
    if not user or user.password != password:
        flash("Email and Password do not match. Please enter a valid combination.")
        return redirect("/login")
    else:
        user_id = user.user_id
        
        session["user_email"] = user.email
        user_in_session = session["user_email"]
        
        # Check if they have spotify and gmail account
        
        # calendar_oauth.main()

        # print(token)
        # token = util.prompt_for_user_token("31xennyy3dcnjh4tmhm4qumdc7sm", #Spotify user
    
        #                                 'user-library-read',
        #                                 SPOTIPY_CLIENT_ID, 
        #                                 SPOTIPY_CLIENT_SECRET,
        #                                 SPOTIPY_REDIRECT_URI)

        # print("TOKEN"*20)
        # print(token)


        # if token:
        #     sp = spotipy.Spotify(auth=token)
        #     results = sp.current_user_saved_tracks()
        #     for item in results['items']:
        #         track = item['track']
        #         print(track['name'] + ' - ' + track['artists'][0]['name'])
        # else:
        #     print("Can't get token for", username)

        return redirect("/quote")
    
    
@app.route("/quote")
def display_quote():
    """Display entry quote upon login"""
    
    # playsound("C:/Users/emmalyddon/hb-dev/src/app/static/mp3/sea-waves-loop.mp3")
    
    # pygame.mixer.init()
    # pygame.mixer.music.load("/static/mp3/sea-waves-loop.mp3")
    # pygame.mixer.music.load("C:/Users/emmalyddon/Music/Music/Media/Music/Unknown Artist/Unknown Album/sea-waves-loop.mp3")
    # pygame.mixer.music.play()
     
    # Get a random quote from database
    quotes = crud.get_all_quotes()
    random_quote = random.choice(quotes)
    
    
    return render_template("quote.html", random_quote=random_quote)


@app.route("/suggested-meditation")
def display_suggested_meditation():
    """Display suggest meditation"""
    
    # Get user in session
    user_email = session.get("user_email")
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id
    
    # Get all meditations by user_id
    meditations = crud.get_all_meditations_by_user_id(user_id)
    # Get a random meditation
    random_meditation = random.choice(meditations)
    
    return render_template("suggested-meditation.html", random_meditation=random_meditation, user_id=user_id)
    

@app.route("/profile")
def redirect_to_profile():
    """Redirect to profile page with user information"""
    
    # Get user in session
    user_email = session.get("user_email")
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id
   
    return redirect(f"/profile/{user_id}")


@app.route("/profile/<user_id>")
def show_profile(user_id):
    """Show profile page with user information"""
    
    # This route is also available when selected from the navigation bar
     
    # Get user in session
    user_email = session.get("user_email")
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id
   
    return render_template("profile.html", user_id=user_id, user=user)


# @app.route("/callback")
# def callback_for_spotify():
    
#     code = request.args.get("code")
#     state = request.args.get("state")
#     print("************************************")
#     print(code)
#     print(state)

    
#     # token = util.prompt_for_user_token(user.fname,
#     #         SCOPE,
#     #         client_id = SPOTIPY_CLIENT_ID,
#     #         client_secret = SPOTIPY_CLIENT_SECRET)


    
#     user_email = session.get("user_email")
#     user = crud.get_user_by_email(user_email)
#     user_id = user.user_id
    
#     return redirect(f"/profile/{user_id}")
    

# def schedule_task():
#     random_meditation = random.choice(meditations)
#     print("This test runs every 15 seconds")
    
#     return random_meditation
    
    
@app.route("/logout")
def logout():
    """Log user out of session."""

    session.clear()
    flash("You are logged out.")
    return redirect("/login")    


@app.route("/meditation-catalog")
def list_meditations(): 
    """Return page showing a list of all available meditations"""

    user_email = session.get("user_email")
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id
    
    # Get all meditations by user id
    meditations = crud.get_all_meditations_by_user_id(user_id)
    
    # Get all of user's favorite meditations
    fav_meditations = crud.get_fav_meditations_by_user_id(user_id)
    if not fav_meditations:
        fav_meditations = []
    
    return render_template("all_meditations.html", meditations=meditations, fav_meditations=fav_meditations)


@app.route("/meditation/<meditation_id>")
def show_meditation(meditation_id):
    """Return page showing the details of a given meditation"""
    
    # Get each meditation by id
    meditation = crud.get_meditation_by_id(meditation_id)
    
    # Query favorites to see if selected meditation exists as a favorite    
    exists = crud.does_fav_meditation_exist(meditation_id)
    
    print(meditation.spotify_url)
    print("*****************")

    return render_template("meditation_details.html", display_meditation=meditation, exists=exists)  


@app.route("/journal")
def show_journal_prompt():
    """Show page with journaling prompt form"""

    return render_template("journal.html")


@app.route("/journal-submission")
def handle_journal_submission():
    """Show user they have successfully submitted their journal entry"""
   
    # Get user by user email, then pass in the user id
    user_email = session.get("user_email")
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id

    journal_count = crud.get_journal_count(user_id)
        
    if journal_count == 1:
        flash("Congrats on your first journal entry! Every small motion makes a difference.")
    else:
        # flash("Cheers to you! You have logged another journal entry. Keep up the self-reflection!")
        flash("Cheers to you! You have logged {journal_count} journal entries. Keep up the self-reflection!")

    return redirect("/profile/{user_id}")


@app.route("/friends")
def show_friends():
    """Show user's current friends
    
    when user searches for friends redirect to the search results page"""
    # returns page (friends.html)
    # shows user a list of their current friends
        # can engage with user by sending them a text
        # option to unfollow a friend from their list
    # user can invite friends
        # an invite form on friends.html page
    # user can search users by username and add them as a friend

    return render_template("friends.html")


@app.route("/reminders")
def show_reminders():
    """Return page that allows user's to schedule their meditation reminders"""

    return render_template("reminders.html")


@app.route("/schedule-reminder.json", methods=["POST"])
def scheudle_reminder():
    
    # Get user by user email, then pass in the user id
    user_email = session.get("user_email")
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id
    
    # Get user's reminder input
    date = request.json.get("date")
    # print(date_str)
    # print("******************")
    # # convert date string to a different date and time order
    # date = date_str.strftime("%m/%d/%Y, %H:%M:%S")
    # print(date)
    reminder_type = request.json.get("type")
    description = request.json.get("description")
    print(description)
    
    # retrieve the date from the notification table when sending an automated text and put a line before the retrieved random message
    # reminder_time = f"Your scheduled check-in is at {date}"
    
    # Get messages related to user's selected reminder type
    # Choose one random message from those messages
    # Get that specific message's message id 
    if reminder_type == "meditate":
        message = crud.get_messages_by_type(reminder_type)
        random_message= random.choice(message)
        message_id = random_message.message_id
        
    elif reminder_type == "journal":
        message = crud.get_messages_by_type(reminder_type)
        random_message = random.choice(message)
        message_id = random_message.message_id
        
    elif reminder_type == "meditate and journal":
        message = crud.get_messages_by_type(reminder_type)
        random_message = random.choice(message)
        message_id = random_message.message_id
        
    elif reminder_type == "inspo message":
        message = crud.get_messages_by_type(reminder_type)
        random_message = random.choice(message)
        message_id = random_message.message_id
    
    # create reminder for user in session
    crud.create_reminder(date=date,
                         reminder_type=reminder_type,
                         description=description,
                         user_id=user_id,
                         message_id=message_id)
    
    return jsonify({"Success": "Here is your reminder information", "Description": description, "Type": reminder_type, "Date": date})


@app.route("/remove-reminder.json")
def remove_reminder():
    
    return jsonify({})


@app.route("/search-meditations")
def search():
    """Show search bar to find specific meditations"""
    
    # user can search for meditation by title or artist name

    user_email = session.get("user_email")
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id
    
    # get all meditations
    meditations = crud.get_all_meditations_by_user_id(user_id)

    return render_template("search_by_meditations.html", meditations=meditations)


@app.route("/meditation-search-results", methods=["POST"])
def meditation_search_results():
    """Return meditation results from user's submitted keywords"""

    # get user's search input
    search_input = request.form.get("search-input")

    # get track names and artist names that match the user's input string
    search_results = crud.get_meditation_by_search_input(search_input)

    return render_template("search_results_meditations.html", search_results=search_results)

@app.route("/search-friends")
def search_friends():
    """Show search bar to find friends"""

    #   user can search for users by first and/or last name
    #   user can search through their friend list
    # get all friends
    friends = crud.get_all_friends()

    return render_template("search_by_friends.html", friends=friends)


@app.route("/friend-search-results", methods=["POST"])
def user_and_friend_search_results():
    """Return user and friend results from user's submitted keywords"""

    # get user's search input
    search_input = request.form.get("search-input")

    # get users's first and/or last names that match the user's input string
    user_search_results = crud.get_users_by_search_input(search_input)

    friend_search_results = crud.get_friends_by_search_input(search_input)

    return render_template("search_results_friends.html", user_search_results=user_search_results, friend_search_results=friend_search_results)


@app.route("/favorite.json", methods=["POST"])
def get_favorite():
    """Handle front-end request to return information about favorite meditation as JSON
    
    Create and store user's favorite in database.
    """

    # get the user id of user in session
    user_email = session.get("user_email")
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id

    # get the medtation id from the front-end
    meditation_id = request.json.get("meditation_id")
    print(meditation_id)

    # check to see if this specific meditation exists within the favorites table
    exists = crud.does_fav_meditation_exist(meditation_id)
    
    if exists == False:
        # create and store the user's new favorite into the database
        crud.create_favorite(meditation_id, user_id)
    
        # set liked meditations in session equal to an empty list
        session["liked_meditations"] = []
        # the liked meditations list variable is now equal to the session's liked meditations empty list
        liked_meditations_lst = session["liked_meditations"]
        # append liked meditation_id to the empty list
        liked_meditations_lst.append(meditation_id)
        # the liked meditation(s) in session is now equal to the appended list
        session["liked_meditations"] = liked_meditations_lst
        # flash("You have successfully added this meditation to your favorites!")

        return jsonify({"success": True, "status": "Your favorite has been stored", "list": session["liked_meditations"], "exist value": exists})
    
    return jsonify({"message": "This favorite already exists in the database"})


@app.route("/remove-favorite.json", methods=["POST"])
def remove_favorite():
    """Handle front-end request to return information about removed favorite meditation as JSON
    
    Handle front-end request. Return success message that favorite meditation has been removed
    
    Remove user's favorite from database.
    """

    # get the user id of user in session
    # user = session.get("user")
    user_email = session.get("user_email")
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id

    # get the medtation id from the front-end
    meditation_id = request.json.get("meditation_id")
    
    # check to see if this specific meditation exists within the favorites table
    exists = crud.does_fav_meditation_exist(meditation_id)
    
    if exists == True:
        # remove the user's favorite from the database
        crud.remove_favorite(meditation_id, user_id)

        # get the liked meditations in session
        liked_meditations_lst = session.get("liked_meditations")
    
        # check to see if the unhearted meditation id exists in the session's liked meditations list
        if meditation_id in liked_meditations_lst:
            # if yes, remove that specific meditation from the list
            liked_meditations_lst.remove(meditation_id)

        # return the updated session's liked meditations list
        # return liked_meditations_lst
        # flash("This meditation has been removed from your favorites.")

        return jsonify({"success": True, "status": "This meditation has been removed from your favorites", "list": liked_meditations_lst})
    
    return jsonify({"message": "This favorite has already been removed from the database"})
    
    
@app.route("/favorites")
def show_favorite_meditations():
    """Show a user's favorite meditations"""
    
    # get the user id of user in session
    user_email = session.get("user_email")
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id
    
    favs = crud.get_fav_meditations_by_user_id(user_id)
   
    fav_meditations = crud.get_fav_meditation_details()
    
    return render_template("favorites.html", fav_meditations=fav_meditations, favs=favs)


@app.route("/journal.json", methods=["POST"])
def get_journal_input():
    
    # get the user id of user in session
    user_email = session.get("user_email")
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id
    # get the journal input values from the front-end
    mood = request.json.get("mood")
    color = request.json.get("color")
    gratitude_1 = request.json.get("gratitude1")
    gratitude_2 = request.json.get("gratitude2")
    gratitude_3 = request.json.get("gratitude3")
    journal_input = request.json.get("journal")
    # get time stamp of when the server receives the fetch request after form submission
    time_stamp = datetime.now()
    # convert datetime.datetime object into a string
    time_stamp_str = time_stamp.strftime("%m/%d/%Y, %H:%M:%S")
    
    # create journal entry for user in session
    crud.create_journal_entry(mood=mood,
                              color=color,
                              gratitude_1=gratitude_1,
                              gratitude_2=gratitude_2,
                              gratitude_3=gratitude_3,
                              journal_input=journal_input,
                              time_stamp=time_stamp,
                              user_id=user_id)
    
    flash("Cheers! You have logged your journal entry. Keep up the self-reflection!")

    return jsonify({"mood": mood, "color": color, "gratitude_1": gratitude_1, "gratitude_2": gratitude_2, "gratitude_3": gratitude_3, "journal_input": journal_input, "time_stamp": time_stamp_str})



if __name__ == "__main__":
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # DebugToolbarExtension(app)
    # scheduler.add_job(id = "Scheduled Quote and Meditation Suggestion", func=schedule_task, trigger="interval", seconds=15)
    # 86400
    # scheduler.start()
    connect_to_db(app)
    app.run(host="localhost", debug=True)
    
    
    
    
    
    
# app.run(threaded=True, port=int(os.environ.get("PORT", os.environ.get("SPOTIPY_REDIRECT_URI", 8080).split(":")[-1])))