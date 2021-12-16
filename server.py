"""Server for mindfulness app."""

from flask import Flask, render_template, request, flash, session, redirect
# from flask_login import login_required, current_user
from model import connect_to_db

import random
# random.choice([name_of_dict.keys()])
# to return random values from a dictionary
import crud
import json
import requests
# import vlc
# import time

import os
# from twilio.rest import Client

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

from jinja2 import StrictUndefined

app = Flask(__name__)
# Required to use Flask sessions
app.secret_key = "219567"
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

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
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
    else:
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
    
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    user_id = user.user_id
    
    if not user or user.password != password:
        flash("Email and Password do not match. Please enter a valid combination.")
        return redirect("/login")
    else:
        session["user_email"] = user.email
        user_in_session = session["user_email"]
        # return redirect(f"/profile/{user_id}")
        return render_template("profile.html", user=user)
      


@app.route("/logout")
def logout():
    """Log user out of session."""

    session.clear()
    flash("You are logged out.")
    return redirect("/login")


@app.route("/profile")
def show_profile():
    """Show profile page with user information"""

    # this route is also available when selected from the navigation bar
   
    return render_template("profile.html")


# @app.route("/profile/<user_id>")
# def show_profile(user_id):
#     """Show profile page with user information"""

#     user = crud.get_user_by_email(user_in_session)
#     user_id = user.user_id
#     # user = User.query.filter_by(email=session["user_email"]).first()
#     # user_id = user.user_id
#     # this route is also available when selected from the navigation bar
   
#     return render_template("profile.html", user_id=user_id, user=user)


@app.route("/meditation-catalog")
def list_meditations(): 
    """Return page showing a list of all available meditations"""

    # list browsable catalog of meditations
    # each meditation has a button
    # when clicked take to route "/meditation/<meditation_id>"

    # get all meditations's data
    meditations = crud.get_all_meditations()

    

    return render_template("all_meditations.html", meditations=meditations)



@app.route("/meditation/<meditation_id>")
def show_meditation(meditation_id):
    """Return page showing the details of a given meditation"""

    # add button that allows user to play the meditation on this page 
    
    # get each meditation by id
    meditation = crud.get_meditation_by_id(meditation_id)

    return render_template("meditation_details.html", display_meditation=meditation)  


@app.route("/journal")
def show_journal_prompt():
    """Show page with journaling prompt form"""

    return render_template("journal.html")


@app.route("/journal-submission", methods=["POST"])
def handle_journal_submission():
    """Show user they have successfully submitted their journal entry"""

    journal_input = request.form.get("journal-entry")
    # in my journal.html, is there a way to get multiple inputs submitted as one field entry
    time_stamp = request.form.get("time-stamp")
    print(time_stamp)
    category = request.form.get("mood")

    journal_entry = crud.create_journal_entry(journal_input, time_stamp, category)
   # get user by user email, then pass in the user id
    
    user = User.query.filter_by(email=session["user_email"]).first()
    user_id = user.user_id

    journal_count = crud.get_journal_count(user_id)
    
    if journal_count >= 1:
        flash("Cheers to you! You have logged another journal entry. Keep up the self-reflection!")
    else:
        flash("Congrats on your first journal entry! Every small motion makes a difference.")
    # return render_template("submitted_journal.html")
    # return redirect(f"/profile/{user_id}")
    return redirect("/meditation-catalog")


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

    # get track names and artist names that match the user's input string
    search_results = crud.get_meditation_by_search_input(search_input)

    return render_template("search_results.html", search_results=search_results)

# @app.route("/search-friends")
# def search_friends():
#     """Show search bar to find friends"""

      # user can search for users by first and/or last name
    #   user can search through their friend list
#     # get all friends
#     friends = crud.get_all_friends()

#     return render_template("search_by_friends.html", friends=friends)


@app.route("/friend-search-results", methods=["POST"])
def user_and_friend_search_results():
    """Return user and friend results from user's submitted keywords"""

    # get users's first and/or last names that match the user's input string
    user_search_results = crud.get_users_by_search_input(search_input)

    friend_search_results = crud.get_friends_by_search_input(search_input)

    # friend_search_results = crud.

    return render_template("search_results_friends.html", user_search_results=user_search_results, friend_search_results=friend_search_results)



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)






# util.prompt_for_user_token(username,
#                            scope,
#                            client_id="9f8b451b49ff48ac845dfcd07a984852",
#                            client_secret="bc2271d942604f7e9929c6ab5ba92212",
#                            redirect_uri="http://localhost:5000/callback/")

# birdy_uri = "spotify:playlist:9f8b451b49ff48ac845dfcd07a984852"
# spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# results = spotify.artist_albums(birdy_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = spotify.next(results)
#     albums.extend(results['items'])

# for album in albums:
#     print(album['name'])




# sound_file = vlc.MediaPLayer("file_path")
# sound_file.play()
# time.sleep(10)
# sound_file.stop()


    # base html template has 3 clickable navigation routes
    # homepage (logo) --> not clickable once logged in
    # search --> renders '/search' route
    # profile --> renders profile.html 


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

