"""Server for mindfulness app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify, url_for
# from flask_login import login_required, current_user
from model import connect_to_db
from dotenv import load_dotenv
from datetime import datetime

import random
# random.choice([name_of_dict.keys()])
# to return random values from a dictionary
import crud
import json
import requests
import re
import uuid
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
# import vlc
# import time

import os
# from twilio.rest import Client

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

from jinja2 import StrictUndefined

# load environment variables from .env.
load_dotenv()  

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
app.jinja_env.undefined = StrictUndefined


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
        
        # if 'credentials' not in session:
        #     return redirect('/authorize')

        # # Load credentials from the session.
        # credentials = google.oauth2.credentials.Credentials(
        #     session['credentials'])

        # drive = googleapiclient.discovery.build(
        #     API_SERVICE_NAME, API_VERSION, credentials=credentials)

        # files = drive.files().list().execute()

        # # Save credentials back to session in case access token was refreshed.
        # # ACTION ITEM: In a production app, you likely want to save these
        # #              credentials in a persistent database instead.
        # session['credentials'] = credentials_to_dict(credentials)
        
        # return jsonify(**files)
        return redirect(f"/profile/{user_id}")
        # return render_template("profile.html", user=user)
        # return render_template("spotify_authorization.html")
        
        
# @app.route("/authorize")
# def authorize_google_account():
#     # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
#     flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#         CLIENT_SECRETS_FILE, scopes=SCOPES)

#     # The URI created here must exactly match one of the authorized redirect URIs
#     # for the OAuth 2.0 client, which you configured in the API Console. If this
#     # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
#     # error.
#     flow.redirect_uri = url_for('oauth2callback', _external=True)

#     authorization_url, state = flow.authorization_url(
#         # Enable offline access so that you can refresh an access token without
#         # re-prompting the user for permission. Recommended for web server apps.
#         access_type='offline',
#         # Enable incremental authorization. Recommended as a best practice.
#         include_granted_scopes='true')

#     # Store the state so the callback can verify the auth server response.
#     session['state'] = state

#     return redirect(authorization_url)
        
        
# @app.route('/oauth2callback')
# def oauth2callback():
#     # Specify the state when creating the flow in the callback so that it can
#     # verified in the authorization server response.
#     state = session['state']

#     flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#         CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
#     flow.redirect_uri = url_for('oauth2callback', _external=True)

#     # Use the authorization server's response to fetch the OAuth 2.0 tokens.
#     authorization_response = request.url
#     flow.fetch_token(authorization_response=authorization_response)

#     # Store credentials in the session.
#     # ACTION ITEM: In a production app, you likely want to save these
#     #              credentials in a persistent database instead.
#     credentials = flow.credentials
#     session['credentials'] = credentials_to_dict(credentials)

#     return redirect(url_for('test_api_request'))
    
    
# @app.route('/revoke')
# def revoke():
#     if 'credentials' not in session:
#         return ('You need to <a href="/authorize">authorize</a> before ' +
#                 'testing the code to revoke credentials.')

#     credentials = google.oauth2.credentials.Credentials(
#         session['credentials'])

#     revoke = requests.post('https://oauth2.googleapis.com/revoke',
#         params={'token': credentials.token},
#         headers = {'content-type': 'application/x-www-form-urlencoded'})

#     status_code = getattr(revoke, 'status_code')
#     if status_code == 200:
#         return('Credentials successfully revoked.')
#     else:
#         return('An error occurred.')


# @app.route('/clear')
# def clear_credentials():
#     if 'credentials' in session:
#         del session['credentials']
    
#     return ('Credentials have been cleared.<br><br>')
    
    
# def credentials_to_dict(credentials):
#       return {'token': credentials.token,
#           'refresh_token': credentials.refresh_token,
#           'token_uri': credentials.token_uri,
#           'client_id': credentials.client_id,
#           'client_secret': credentials.client_secret,
#           'scopes': credentials.scopes}
      

@app.route("/logout")
def logout():
    """Log user out of session."""

    session.clear()
    flash("You are logged out.")
    return redirect("/login")


@app.route("/profile")
def redirect_to_show_profile():
    """Show profile page with user information"""

    # this route is also available when selected from the navigation bar
    
    user_email = session.get("user_email")
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id
   
    return redirect(f"/profile/{user_id}")


@app.route("/profile/<user_id>")
def show_profile(user_id):
    """Show profile page with user information"""
    
    user_email = session.get("user_email")
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id
   
    # this route is also available when selected from the navigation bar
    
    meditations = crud.get_all_meditations()
    # should this be a crud funtions?
    random_meditation = random.choice(meditations)
    # store random meditation in session
    # session["random_meditation"] = random_meditation
    
    quotes = crud.get_all_quotes()
    random_quote = random.choice(quotes)
    # session["random_quote"] = random_quote
   
    return render_template("profile.html", user_id=user_id, user=user, random_meditation=random_meditation, random_quote=random_quote)


@app.route("/meditation-catalog")
def list_meditations(): 
    """Return page showing a list of all available meditations"""

    # list browsable catalog of meditations
    # each meditation has a button
    # when clicked take to route "/meditation/<meditation_id>"

    # get all meditations's data
    meditations = crud.get_all_meditations()
    
    # get all of user's favorite meditations
    fav_meditations = crud.get_fav_meditations()

    return render_template("all_meditations.html", meditations=meditations, fav_meditations=fav_meditations)


@app.route("/meditation/<meditation_id>")
def show_meditation(meditation_id):
    """Return page showing the details of a given meditation"""

    # add button that allows user to play the meditation on this page 
    
    # get each meditation by id
    meditation = crud.get_meditation_by_id(meditation_id)
    
    # query favorites to see if selected meditation exists as a favorite    
    exists = crud.does_fav_meditation_exist(meditation_id)

    return render_template("meditation_details.html", display_meditation=meditation, exists=exists)  


@app.route("/journal")
def show_journal_prompt():
    """Show page with journaling prompt form"""

    return render_template("journal.html")


@app.route("/journal-submission")
def handle_journal_submission():
    """Show user they have successfully submitted their journal entry"""
   
    # get user by user email, then pass in the user id
    email = session["user_email"]
    user = crud.get_user_by_email(email)
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


@app.route("/schedule-reminders")
def schedule_reminders():
    """Return page that allows user's to schedule their meditation reminders"""

    return render_template("calendar.html")


@app.route("/search-meditations")
def search():
    """Show search bar to find specific meditations"""
    
    # user can search for meditation by title or artist name

    # get all meditations
    meditations = crud.get_all_meditations()

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
    user_email = session["user_email"]
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id

    # get the medtation id from the front-end
    meditation_id = request.json.get("meditation_id")

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
    user_email = session["user_email"]
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
    favs = crud.get_fav_meditations()
   
    fav_meditations = crud.get_fav_meditation_details()
    
    return render_template("favorites.html", fav_meditations=fav_meditations, favs=favs)


@app.route("/journal.json", methods=["POST"])
def get_journal_input():
    
    # get the user id of user in session
    user_email = session["user_email"]
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id

    # get the journal input values from the front-end
    mood = request.json.get("mood")
    color = request.json.get("color")
    gratitude_1 = request.json.get("gratitude1")
    gratitude_2 = request.json.get("gratitude2")
    gratitude_3 = request.json.get("gratitude3")
    time_stamp = request.json.get("time")
    # dt_object = datetime.fromtimestamp(time)
    journal = request.json.get("journal")
    
    
    # create journal entry for user in session
    crud.create_journal_entry(mood=mood,
                              color=color,
                              gratitude_1=gratitude_1,
                              gratitude_2=gratitude_2,
                              gratitude_3=gratitude_3,
                              journal_input=journal,
                              time_stamp=time_stamp,
                              user_id=user_id)
    
    flash("Cheers! You have logged your journal entry. Keep up the self-reflection!")

    return jsonify({mood: mood, color: color, gratitude_1: gratitude_1, gratitude_2: gratitude_2, gratitude_3: gratitude_3, journal: journal, time_stamp: dt_object})

# @app.route("/journal.json", methods=["POST"])
# def get_journal_input():
    
#     # get the user id of user in session
#     user_email = session["user_email"]
#     user = crud.get_user_by_email(user_email)
#     user_id = user.user_id

#     # get the journal input values from the front-end
#     mood = request.json.get("mood")
#     color = request.json.get("color")


#     return jsonify({mood: mood, color: color})

# @app.route("/journal-submission")
# def handle_journal_submission():
    
#     # create journal entry for user in session
#     journal_entry = crud.create_journal_entry(mood=mood,
#                                               color=color,
#                                               journal_input=journal,
#                                               time_stamp=date)
    
#     date = request.form.get("time-stamp")
#     journal = request.form.get("journal-entry")

#     flash("Cheers! You have logged your journal entry. Keep up the self-reflection!")


if __name__ == "__main__":
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="localhost", debug=True)
    
    
    
    
    
    
# app.run(threaded=True, port=int(os.environ.get("PORT", os.environ.get("SPOTIPY_REDIRECT_URI", 8080).split(":")[-1])))

# PSEUDOCODE
# @app.route("/")
# def index(): 
    # render homepage.html template

# in homepage.html there are two buttons: actions = "/create account" or "/login" -- both POST methods
    # "create-account" button --> takes you to '/create-account' route
        # form action='/create-account"
    # "login" button --> takes you to '/login' route
        # form action="/login"

# @app.route("/create-account") 
# def create_account():
    # an input form --> login data gets stored into database in the User table 
        # keywords: first-name" "last-name" "email" "phone-number" "username" "password"
    # set conditions:
        # login info must meet certain criteria
        # if conditions are met --> render profile.html template    

# @app.route("/login", methods=["POST"]) 
# def process_login():
    # check to see if user already exists once user submits login info
        # if yes, redender profile.html template
        # if no, generate text saying: username and password do not match
            # allow user to reenter login info

# in profile.html
    # 3 buttons: actions = "/meditation-catalog" "/journaling" "/friends"

# @app.route("/meditation-catalog")
# def list_meditations(): 
    # list browsable catalog of meditations
    # each meditation has a button
    # when clicked take to route '/meditation' 

# @app.route('/meditation/<meditation_id>')
# def show_meditation(melon_id):
    # returns page "meditation_details.html" showing details of a given meditation
    # button that allows user to play the meditation on this page   

# @app.route("/journaling")
# def show_journal_prompt():
    # returns page (journal.html) showing journal prompt with a text field form


# @app.route("/friends")
# def show_friends():
    # returns page (friends.html)
    # shows user a list of their current friends
        # can engage with user by sending them a text
    # user can invite friends, search users by username and add them as a friend, unfollow friend

# @app.route("/search")
# def search():
    # renders search page
    # user can search for users by username
    # user can search for meditation by title

# @app.route("/search-results")
# def search_results():
    # lists all users == the submitted username
    # lists all meditations matching submitted keyword(s)

