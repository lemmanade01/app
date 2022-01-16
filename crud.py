"""CRUD operations."""

from model import db, User, Journal, Meditation, Notification, Message, Favorite, Quote, Tip, connect_to_db
import spotify
import os
from datetime import datetime
from sqlalchemy import delete, update, extract


def get_user_by_email(email):
    """Get and return user's email."""

    user = User.query.filter(User.email==email).first()

    return user


def get_user_by_fname(fname):
    """Get and return user's first name."""

    user = User.query.filter_by(fname=fname).first()

    return user


# def get_user_by_username(username):
#     """get and return user's username"""

#     user = User.query.filter_by(username=username).first()

#     return user


def get_user_by_password(password):
    """Get and return user's password."""

    password = User.query.filter_by(password=password).first()

    return password


def get_user_by_id(user_id):
    """Return a user by primary key."""
    
    user = User.query.get(user_id)
    
    return user


def create_user(fname, lname, email, phone_num, password, quote):
    """Create and return a new user."""

    user = User(
        fname=fname,
        lname=lname,
        email=email,
        phone_num=phone_num,
        password=password,
        quote=quote)

    db.session.add(user)
    db.session.commit()
 
    return user


def create_journal_entry(scale, mood, color, gratitude_1, gratitude_2, gratitude_3, journal_input, time_stamp, mnth, user_id):
    """Create and return a journal entry."""

    journal = Journal(scale=scale,
                      mood=mood,
                      color=color,
                      gratitude_1=gratitude_1,
                      gratitude_2=gratitude_2,
                      gratitude_3=gratitude_3,
                      journal_input=journal_input,
                      time_stamp=time_stamp,
                      mnth=mnth,
                      user_id=user_id)

    db.session.add(journal)
    db.session.commit()

    return journal


def get_journal_count(user_id):
    """Get journal count by user id."""

    # get journal count by user_id
    journal_entry = Journal.query.filter_by(user_id=user_id).count()

    return journal_entry


def get_all_journal_entries(user_id):
    """Get and return all journal entries for user in session"""

    journal_entries = Journal.query.filter(Journal.user_id==user_id).order_by(Journal.time_stamp.asc()).all()
    
    return journal_entries


def get_todays_journal_count(user_id):
    """Get and return a user's journal count for today"""
    
    # journal_count = Journal.query.filter(Journal.user_id==user_id, Journal.time_stamp==date).count()
    
    date = datetime.now()
    
    journal_count = Journal.query.filter(Journal.user_id==user_id, Journal.time_stamp==date).count()
    
    return journal_count
    

def get_journal_entries_ordered_by_date(user_id):
    """Get and return all journal entries for user in session
     
    Retrieve entries in chronological order.
    """

    journal_entries = Journal.query.filter(Journal.user_id==user_id).order_by(Journal.time_stamp.asc()).all()
    
    return journal_entries


def get_journal_by_search_input(date_object, user_id):
    """Order chronologically and return all journal entries that match user's search input
    
    User can retrieve entries by searching by date"""
    
    search_results = Journal.query.filter(func.date(Journal.time_stamp) == date_object).all()

    
    # search_results = Journal.query.filter(Journal.time_stamp.ilike(f"%{date_object}%"), Journal.user_id==user_id).all()
    
    # search_results = Journal.query.filter(Journal.mnth.ilike(f"%{search_input}%"), Journal.user_id==user_id).all()

    
    # search_results = Journal.query.filter(extract('month', Journal.time_stamp).ilike(f"%{search_input}%"), Journal.user_id==user_id).all()
            
    # search_results = Journal.query.filter(Journal.user_id==user_id, Journal.mnth.ilike(f"%{search_input}%"), Journal.time_stamp.day.ilike(f"%{search_input}%"), Journal.time_stamp.year.ilike(f"%{search_input}%")).order_by(Journal.time_stamp.asc()).all()
    
    # search_results = Journal.query.filter(Journal.mnth.ilike(f"{search_input}%"), Journal.user_id==user_id).all()
    
    # search_results = Journal.query.filter(Journal.time_stamp.month.ilike(f"%{search_input}%") | Journal.time_stamp.day.ilike(f"%{search_input}%") | Journal.time_stamp.year.ilike(f"%{search_input}%"), Journal.user_id==user_id).all()
    
    
    return search_results


# def get_journal_by_date(search_input):
    
#     date = Journal.query.filter(Journal.time_stamp.day==search_input)
    
#     return date

    
def create_meditations(user_id):
    """Create and return a new Spotify meditation track."""
    
    # for each meditation, create an object/instance with those arguments
    # spotify username and playlist id
    spotify_username = os.environ["SPOTIFY_USERNAME"]
    spotify_playlist = os.environ["SPOTIFY_PLAYLIST_ID"]

    # access function from spotiy.py to retrieve the data from my spotify playlist
    # pass through username and playlist_id
    results = spotify.get_playlist_tracks(spotify_username, spotify_playlist)
    print(results)
    
    # each result is a track_key
    for result in results:
        # values is a list of strings about track data
        values = results[result]
    
        # assign the proper string values to the corresponding variable name
        track_name = values[0]
        artist_name = values[1]
        image_url = values[2]
        spotify_url = values[3]
        preview_link = values[4]

        # create an instance of Meditation
        meditation = Meditation(track_name=track_name, artist_name=artist_name, image_url=image_url, spotify_url=spotify_url, preview_link=preview_link, user_id=user_id)
    
        # add this instance to the db
        db.session.add(meditation) 
    # commit the instance so it officially stores
    db.session.commit()

    return meditation


# def get_all_meditations():
#     """Get and return all meditations."""

#     # all_meditations = Meditation.query.all()
#     all_meditations = Meditation.query.order_by(Meditation.track_name.desc()).all()

#     return all_meditations
#     # not sure if this is right?
    
    
def get_all_meditations_by_user_id(user_id):
    """Get all meditations associated with user in session"""
    
    all_meditations = Meditation.query.filter(Meditation.user_id==user_id).order_by(Meditation.artist_name.asc()).all()
    
    return all_meditations


def get_all_meditations_an_asc(user_id):
    """Get all meditations associated with user in session"""
    
    all_meditations = Meditation.query.filter(Meditation.user_id==user_id).order_by(Meditation.artist_name.asc()).all()
    
    return all_meditations


def get_all_meditations_an_desc(user_id):
    """Get all meditations associated with user in session"""
    
    all_meditations = Meditation.query.filter(Meditation.user_id==user_id).order_by(Meditation.artist_name.desc()).all()
    
    return all_meditations


def get_all_meditations_tn_asc(user_id):
    """Get all meditations associated with user in session"""
    
    all_meditations = Meditation.query.filter(Meditation.user_id==user_id).order_by(Meditation.track_name.asc()).all()
    
    return all_meditations


def get_all_meditations_tn_desc(user_id):
    """Get all meditations associated with user in session"""
    
    all_meditations = Meditation.query.filter(Meditation.user_id==user_id).order_by(Meditation.track_name.desc()).all()
    
    return all_meditations


def get_all_meditations_an_desc(user_id):
    """Get all meditations associated with user in session"""
    
    all_meditations = Meditation.query.filter(Meditation.user_id==user_id).order_by(Meditation.track_name.desc()).all()
    
    return all_meditations

    
def get_meditation_by_id(meditation_id):
    """Return a meditation by primary key."""
    
    # single_meditation = Meditation.query.filter_by(meditation_id=meditation_id).one()
    single_meditation = Meditation.query.get(meditation_id)
    
    return single_meditation


def does_fav_meditation_exist(meditation_id):
    """Check to see if a meditation id currently exists in favorites"""
    
    exists = Favorite.query.filter_by(meditation_id=meditation_id).first() is not None
    
    return exists


def get_fav_meditation_by_id(meditation_id):
    """Check to see if a meditation id currently exists in favorites"""
    
    fav_meditation = Favorite.query.filter(Favorite.meditation_id==meditation_id).first()
    
    return fav_meditation


def get_fav_meditation_details():
    """Join Favorite table on Meditation table by meditation id"""
    
    fav_meditation_ids = Meditation.query.join(Favorite).filter(Favorite.meditation_id==Meditation.meditation_id).all()
    
    return fav_meditation_ids


def get_fav_meditations_by_user_id(user_id):
    """Get and return all favorite meditations."""
    
    fav_meditations = Favorite.query.all()
    
    return fav_meditations


def get_meditation_by_search_input(search_input):
    """Return all meditations that match user's search input."""
    
    search_results = Meditation.query.filter(Meditation.track_name.ilike(f"%{search_input}%") | Meditation.artist_name.ilike(f"%{search_input}%")).all()

    return search_results


# def add_a_friend(friend):
#     """Add and return a new friend"""

#     friend = Friend(friend=friend)

#     db.session.add(friend)
#     db.session.commit()

#     return friend
    # need to check if this is correct


# def get_all_friends():
#     """Return all friends"""

#     all_friends = Friend.query.all()

#     return all_friends


def get_users_by_search_input(search_input):
    """Return all app users that match user's input."""

    search_results = User.query.filter(User.fname.ilike(f"%{search_input}%") | User.lname.ilike(f"%{search_input}%")).all()

    return search_results


# def get_friends_by_search_input(search_input):
#     """Return all friends that match user's input."""

#     search_results = Friend.query.filter(User.fname.ilike(f"%{search_input}%") | User.lname.ilike(f"%{search_input}%")).all()

#     return search_results


def get_all_messages():
    """Get and return all pre-populated text messages"""

    messages = Message.query.all()

    return messages


def get_all_quotes():
    """Get and return all pre-populated quotes"""
    
    quotes = Quote.query.all()
    
    return quotes


# def create_calendar_event():
#     """Create and return a new calendar event"""

#     event = Notification(date=date,
#                          user_id=user_id,
#                          message_id=message_id)

#     db.session.add(event)
#     db.session.commit()

#     return event


# def update_calendar_event():
#     """Update and return existing calendar event"""

#     return updated_event


# def delete_calendar_event():
#     """Delete existing calednar event"""

#     return deleted_event


def create_reminder(date, reminder_type, description, user_id, message_id):
    """Create and return a scheduled calendar notification."""

    notification = Notification(date=date,
                                reminder_type=reminder_type,
                                description=description,
                                user_id=user_id,
                                message_id=message_id)

    db.session.add(notification)
    db.session.commit()

    return notification


def remove_reminder(notification_id, user_id):
    """Remove existing reminder notification"""

    reminder = Notification.query.filter(Notification.notification_id==notification_id, Notification.user_id==user_id).first()

    db.session.delete(reminder)
    db.session.commit()
    
    return reminder


def get_all_reminders(user_id):
    """Get user's reminders"""

    all_reminders = Notification.query.filter(Notification.user_id==user_id).order_by(Notification.date.asc()).all()
    
    return all_reminders


# def get_all_reminders_dates(user_id):
#     """Get all dates for scheudled reminders"""
    
#     reminder_dates = Notification.query.filter(Notifiation.user_id==user_id)


def get_uptodate_reminders(user_id, time_stamp):
    """Get and return reminders that are current"""
    
    reminders = Notification.query.filter(Notification.user_id==user_id, Notification.date >= time_stamp).order_by(Notification.date.asc()).all()
    
    return reminders


def remove_outofdate_reminders(user_id, time_stamp):
    """Get and return reminders that are past the current date"""

    old_reminders = Notification.query.filter(Notification.user_id==user_id, Notification.date < time_stamp).order_by(Notification.date.asc()).all()
    
    for old_reminder in old_reminders:
        db.session.delete(old_reminder)
        db.session.commit()
        
    return old_reminders


def get_most_recent_reminder(user_id):
    """Get user's most recently created reminder"""
    
    reminder = Notification.query.filter(Notification.user_id==user_id).order_by(Notification.notification_id.desc()).first()
    
    return reminder


def get_messages_by_type(reminder_type):
    """Get all messages associated with the same reminder type"""
    
    messages = Message.query.filter(Message.reminder_type==reminder_type).all()
    
    return messages

# def get_random_message_id(random_message):
#     """Get the message id associated with the randomly selected reminder message"""
    
#     message_id = Message.query.get(rand)

def update_notification(user_id):
    """Get notification by date
    
    Update and return existing calendar notification
    """
    
    notification = Notification.query.filter(Notification.date, Notification.user_id).first()    
    
    return updated_notification


# def send_notification():

def create_favorite(meditation_id, user_id):
    """Create and return a user's favorite meditation"""

    fav = Favorite(meditation_id=meditation_id,
                   user_id=user_id)
    
    db.session.add(fav)
    db.session.commit()

    return fav


def remove_favorite(meditation_id, user_id):
    """Remove a user's favorite meditation"""

    removed_fav = Favorite.query.filter_by(meditation_id=meditation_id, user_id=user_id).first()

    db.session.delete(removed_fav)
    db.session.commit()

    return removed_fav


def create_quote(quote_id, inspo_quote, author):
    """Create and return inspo quote"""
    
    quote = Quote(quote_id=quote_id,
                  inspo_quote=inspo_quote,
                  author=author)
    
    db.session.add(quote)
    db.session.commit()
    
    return quote


def create_txt_message(message_id, txt_message, reminder_type):
    """Create and return a text message"""
    
    message = Message(message_id=message_id,
                      txt_message=txt_message,
                      reminder_type=reminder_type)
    
    db.session.add(message)
    db.session.commit()
    
    return message


def create_wellness_tip(tip_id, wellness_tip, source):
    """Create and return a wellness tip"""
    
    tip = Tip(tip_id=tip_id, 
              wellness_tip=wellness_tip,
              source=source)
    
    db.session.add(tip)
    db.session.commit()
    
    return tip


def get_wellness_tips():
    """Get and return all wellness tips"""
    
    tips = Tip.query.all()
    
    return tips




if __name__ == '__main__':
    from server import app
    connect_to_db(app)
