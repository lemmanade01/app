"""Server for mindfulness app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db
from datetime import datetime
from jinja2 import StrictUndefined
from dotenv import load_dotenv

import helpers
import random
import crud
import json
import requests
import os


load_dotenv()
PORT_NUMBER = 8000
SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
# Set an attribute of the Jinja environment that throws 
# an error for undefined variables
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
    password = request.form.get("password")
    quote = request.form.get("quote")
    
    # Get that user's id
    user = crud.get_user_by_email(email)

    if user:
        flash("A user already exists with that email.")
        return redirect("/create-account")
    
   
    
    # Create a user
    crud.create_user(fname, lname, email, phone_num, password, quote)

    new_user = crud.get_user_by_email(email)
    user_id = new_user.user_id
    
    # Populate the database with meditations when a user creates an account
    crud.create_meditations(user_id)
        
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
    # Get the user's email and lowercase all letters
    email = request.form.get("email").lower()
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    
    # Check to see if the email and password match
    if not user or user.password != password:
        flash("Email and Password do not match. Please enter a valid combination.")
        return redirect("/login")
    else:
        user_id = user.user_id
        
        session["user_email"] = user.email
        user_in_session = session["user_email"]
        
        return redirect("/quote")
    
    
@app.route("/quote")
def display_quote():
    """Display entry quote upon login"""
         
    # Get a random quote from database
    quotes = crud.get_all_quotes()
    random_quote = random.choice(quotes)
    
    return render_template("quote.html", random_quote=random_quote)


@app.route("/suggested-meditation")
def display_suggested_meditation():
    """Display suggest meditation"""
    
    # Get user in session
    user_id = helpers.get_user_in_session()
    
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
    fname = user.fname.lower()
   
    return redirect(f"/profile/{fname}")


@app.route("/profile/<user_id>")
def show_profile(user_id):
    """Show profile page with user information"""
    
    # Get user in session
    user_id = helpers.get_user_in_session()
    
    # Get total count of journal entries by user id
    journal_count = crud.get_journal_count(user_id)
   
    return render_template("profile.html", user_id=user_id, user=user, journal_count=journal_count)


@app.route("/logout")
def logout():
    """Log user out of session."""

    session.clear()
    flash("You are logged out.")
    return redirect("/login")


@app.route("/meditation-catalog")
def list_meditations(): 
    """Return page showing a list of all available meditations"""

    # Get user id of user in session
    user_id = helpers.get_user_in_session()
    
    # Favorite meditations defaults to an empty list
    fav_meditations = []
     
    # Get all meditations by user id
    meditations = crud.get_all_meditations_by_user_id(user_id)
    
    # Get all of user's favorite meditations
    all_favs = crud.get_fav_meditations_by_user_id(user_id)
   
    # If favorites exist
    if all_favs:
        # Loop through the favorites
        for fav_meditation in all_favs:
            # Add each favorite's meditation id to the list
            fav_meditations.append(fav_meditation.meditation_id)
    
    return render_template("all_meditations.html", meditations=meditations, fav_meditations=fav_meditations)
    

@app.route("/meditation-search-results", methods=["POST"])
def meditation_search_results():
    """Return meditation results from user's submitted keywords"""

    # Get the user id of user in session
    user_id = helpers.get_user_in_session()
    
    # Get user's search input
    search_input = request.form.get("search-input")

    # Get track names and artist names that match the user's input string
    search_results = crud.get_meditation_by_search_input(search_input)
    
    # Get all of user's favorite meditations
    fav_meditations = crud.get_fav_meditations_by_user_id(user_id)
    if not fav_meditations:
        fav_meditations = []

    return render_template("search_results_meditations.html", search_results=search_results, fav_meditations=fav_meditations)


@app.route("/meditation/<meditation_id>")
def show_meditation(meditation_id):
    """Return page showing the details of a given meditation"""
    
    # Get each meditation by id
    meditation = crud.get_meditation_by_id(meditation_id)
    
    # Query favorites to see if selected meditation exists as a favorite
    exists = crud.does_fav_meditation_exist(meditation_id)
    
    # Get all welness tips
    tips = crud.get_wellness_tips()
    
    random_tip = random.choice(tips)

    return render_template("meditation_details.html",display_meditation=meditation, exists=exists, random_tip=random_tip)


@app.route("/add-favorite.json", methods=["POST"])
def add_favorite():
    """Handle front-end request to return information about favorite meditation as JSON
    
    Create and store user's favorite in database.
    """

    # Get the user id of user in session
    user_id = helpers.get_user_in_session()

    # Get the medtation id from the front-end
    meditation_id = request.json.get("meditation_id")

    # Check to see if this specific meditation exists within the favorites table
    exists = crud.does_fav_meditation_exist(meditation_id)
    
    if exists == False:
        # Create and store the user's new favorite into the database
        crud.create_favorite(meditation_id, user_id)
    
        # Set liked meditations in session equal to an empty list
        session["liked_meditations"] = []
        # The liked meditations list variable is now equal to the session's liked meditations empty list
        liked_meditations_lst = session["liked_meditations"]
        # Append liked meditation_id to the empty list
        liked_meditations_lst.append(meditation_id)
        # The liked meditation(s) in session is now equal to the appended list
        session["liked_meditations"] = liked_meditations_lst
        # flash("You have successfully added this meditation to your favorites!")

        return jsonify({"success": True, "status": "Your favorite has been stored", "list": session["liked_meditations"], "exist value": exists})
    
    return jsonify({"message": "This favorite already exists in the database"})


@app.route("/remove-favorite.json", methods=["POST"])
def remove_favorite():
    """Handle front-end request to return information about removed favorite meditation as JSON
    
    Remove user's favorite from database
    
    Return success message that favorite meditation has been removed
    """

    # Get the user id of user in session
    user_id = helpers.get_user_in_session()

    # Get the medtation id from the front-end
    meditation_id = request.json.get("meditation_id")
    
    # Check to see if this specific meditation exists within the favorites table
    exists = crud.does_fav_meditation_exist(meditation_id)
    
    if exists == True:
        # Remove the user's favorite from the database
        crud.remove_favorite(meditation_id, user_id)

        # Get the liked meditations in session
        liked_meditations_lst = session.get("liked_meditations")
    
        # Check to see if the unhearted meditation id exists in the session's liked meditations list
        if meditation_id in liked_meditations_lst:
            # If yes, remove that specific meditation from the list
            liked_meditations_lst.remove(meditation_id)

        return jsonify({"success": True, "status": "This meditation has been removed from your favorites", "list": liked_meditations_lst})
    
    return jsonify({"message": "This favorite has already been removed from the database"})
    
    
@app.route("/favorites")
def show_favorite_meditations():
    """Show a user's favorite meditations"""
    
    # Get the user id of user in session
    user_id = helpers.get_user_in_session()
    
    # Get logged in user's favorite meditations
    favs = crud.get_fav_meditations_by_user_id(user_id)
   
    # Cross check favorites table with meditations table
    fav_meditations = crud.get_fav_meditation_details()
    
    return render_template("favorites.html", fav_meditations=fav_meditations, favs=favs)


@app.route("/journal")
def show_journal_prompt():
    """Show page with journaling prompt"""
         
    return render_template("journal_entry.html")


@app.route("/journal-check.json")
def check_entry_count():
    """Check to see if user has already submitted a journal entry for today
    
    Limit one entry per day"""
    
    # Get user in session
    user_id = helpers.get_user_in_session()
    
    # THIS QUERY IS INCORRECT -- FIX!
    entry = crud.get_todays_journal_count(user_id)
    
    return jsonify({"count": entry})
    

@app.route("/journal.json", methods=["POST"])
def get_journal_input():
    """Get and return user's journal input and create a journal entry in the database"""
    
    # Get the user id of user in session
    user_id = helpers.get_user_in_session()
    
    # Get the journal input values from the front-end
    scale = request.json.get("scale")
    mood = request.json.get("mood")
    color = request.json.get("color")
    gratitude_1 = request.json.get("gratitude1")
    gratitude_2 = request.json.get("gratitude2")
    gratitude_3 = request.json.get("gratitude3")
    journal_input = request.json.get("journal")
    # Get time stamp of when the server receives the fetch request after form submission
    time_stamp = datetime.now()
   
    # Convert datetime.datetime object into a string
    time_str = time_stamp.strftime("%m/%d/%Y, %H:%M:%S")

    # Slice string to retrieve individual date attributes
    # mth is numerical (but a string)
    mth = time_str[:2]
    
    # Account for user input where months are written out instead of numbers
    # Reassign variables with numerical string values to alphabetical months
    if mth == "01":
        mnth = "January"
    elif mth == "02":
        mnth = "February"
    elif mth == "03":
        mnth = "March"
    elif mth == "04":
        mnth = "April"
    elif mth == "05":
        mnth = "May"
    elif mth == "06":
        mnth = "June"
    elif mth == "07":
        mnth = "July"
    elif mth == "08":
        mnth = "August"
    elif mth == "09":
        mnth = "September"
    elif mth == "10":
        mnth = "October"
    elif mth == "11":
        mnth = "November"
    elif mth == "12":
        mnth = "December"
    
    # Create journal entry for user in session
    crud.create_journal_entry(scale=scale,
                              mood=mood,
                              color=color,
                              gratitude_1=gratitude_1,
                              gratitude_2=gratitude_2,
                              gratitude_3=gratitude_3,
                              journal_input=journal_input,
                              time_stamp=time_stamp,
                              mnth=mnth,
                              user_id=user_id)

    return jsonify({"scale": scale, "mood": mood, "color": color, "gratitude_1": gratitude_1, "gratitude_2": gratitude_2, "gratitude_3": gratitude_3, "journal_input": journal_input, "time_stamp": time_stamp, "time_stamp_str": time_str, "month": mnth})


@app.route("/journal-data.json")
def get_journal_data():
    """Get and return all journal entries in JSON for a user in session"""
    
    # Get user in session
    user_id = helpers.get_user_in_session()
    
    # Get all journal entries
    journal_entries = crud.get_all_journal_entries(user_id)
   
    # If a journal entry exists
    if journal_entries:
        
        # Create an open dictionary
        journal_entries_dict = {}

        # For each journal entry object in the list of journal entry objects
        for journal_entry in journal_entries:
            
            # Get each journal's journal id
            journal_id = journal_entry.journal_id
                
            # Create a nested dictionary where journal id is the key to a dictionary containing that journal's attributes through key/value pairs
            journal_entries_dict[journal_id] = {
                "scale": journal_entry.scale,
                "mood": journal_entry.mood,
                "color": journal_entry.color,
                "gratitude_1": journal_entry.gratitude_1,
                "gratitude_2": journal_entry.gratitude_2,
                "gratitude_3": journal_entry.gratitude_3,
                "journal_input": journal_entry.journal_input,
                "time_stamp": journal_entry.time_stamp,
                "mnth": journal_entry.mnth
            }
            # Mnth without the O represents the month spelled with letters
            # .month is a datetime attribute that represents the month by integer
    
        # Return a jsonified form of this nested dictionary
        return jsonify(journal_entries_dict)
    
    else:
        return jsonify({"results": "none"})


@app.route("/journal-success")
def show_submission_success():
    """Show user they have successfully submitted a journal entry
    
    Flash their total journal count
    """
    
    # Get user in session
    user_id = helpers.get_user_in_session()
    
    count = crud.get_journal_count(user_id)
    # time.sleep(5)
    
    return render_template("journal_success.html", count=count)


@app.route("/journal-date-results.json", methods=["POST"])
def display_journal_date_results():
    
    # Get user in session
    user_id = helpers.get_user_in_session()
    
    jrnl_input_date = request.json.get("date")
    
    # Get all journal entries
    jrnl_results = crud.get_all_journal_entries(user_id)
    
    if jrnl_results:
        journal_search_data = {}
         
        for journal_entry in jrnl_results:
            jrnl_date = journal_entry.time_stamp
            date = jrnl_date.strftime("%Y-%m-%d")
    
            if date == jrnl_input_date:
                 
                # Get each journal's journal id
                journal_id = journal_entry.journal_id
                    
                # Create a nested dictionary where journal id is the key to a dictionary containing that journal's attributes through key/value pairs
                journal_search_data[journal_id] = {
                    "scale": journal_entry.scale,
                    "mood": journal_entry.mood,
                    "color": journal_entry.color,
                    "gratitude_1": journal_entry.gratitude_1,
                    "gratitude_2": journal_entry.gratitude_2,
                    "gratitude_3": journal_entry.gratitude_3,
                    "journal_input": journal_entry.journal_input,
                    "time_stamp": journal_entry.time_stamp,
                    "mnth": journal_entry.mnth
                }
                # Mnth without the O represents the month spelled with letters
                # .month is a datetime attribute that represents the month by integer

        # Return a jsonified form of this nested dictionary
        return jsonify(journal_search_data)
                    
    else:
        return jsonify({"results": "none"})


@app.route("/reminders")
def show_reminders():
    """Return page that allows user's to schedule their meditation reminders"""
    
    # Get user by user email, then pass in the user id
    user_id = helpers.get_user_in_session()
    
    # Get current time and date
    time_stamp = datetime.now()
    
    # Get user's reminders that are for today and future dates
    reminders = crud.get_uptodate_reminders(user_id, time_stamp)
    
    # Delete reminders that are past today's date and time
    old_reminders = crud.remove_outofdate_reminders(user_id, time_stamp)

    return render_template("reminders.html", reminders=reminders)


@app.route("/schedule-reminder.json", methods=["POST"])
def scheudle_reminder():
    
    # Get user by user email, then pass in the user id
    user_id = helpers.get_user_in_session()
    
    # Get user's reminder input
    date = request.json.get("date")
 
    reminder_type = request.json.get("type")
    description = request.json.get("description")
    
    # Get messages related to user's selected reminder type
    # Choose one random message from those messages
    # Get that specific message's message id 
    if reminder_type == "Meditate":
        message = crud.get_messages_by_type(reminder_type)
        random_message = random.choice(message)
        message_id = random_message.message_id
        
    elif reminder_type == "Journal":
        message = crud.get_messages_by_type(reminder_type)
        random_message = random.choice(message)
        message_id = random_message.message_id
        
    elif reminder_type == "Meditate and Journal":
        message = crud.get_messages_by_type(reminder_type)
        random_message = random.choice(message)
        message_id = random_message.message_id
        
    elif reminder_type == "Inspirational Message":
        message = crud.get_messages_by_type(reminder_type)
        random_message = random.choice(message)
        message_id = random_message.message_id
    
    # Create reminder for user in session
    crud.create_reminder(date=date,
                         reminder_type=reminder_type,
                         description=description,
                         user_id=user_id,
                         message_id=message_id)
    
    reminder = crud.get_most_recent_reminder(user_id)
    reminder_id = reminder.notification_id
    
    return jsonify({"Success": "Here is your reminder information", "description": description, "type": reminder_type, "date": date, "ID": reminder_id})


@app.route("/remove-reminder.json", methods=["POST"])
def remove_reminder():
    """Remove a user's reminder from database"""
    
    # Get user's id
    user_id = helpers.get_user_in_session()
    
    # Get reminder from frontend
    notification_id = request.json.get("reminder_id")
    
    # Get reminder by reminder id
    reminder = crud.remove_reminder(notification_id, user_id)
    
    # # Get user's most recently created reminder
    # reminder = crud.get_most_recent_reminder(user_id, reminder_id)
    
    return jsonify({"Success!": "Your reminder has been deleted"})


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="localhost", debug=True)
