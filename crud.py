"""CRUD operations."""

from model import db, User, Journal, Meditation, Notification, Message, Friend, Favorite, connect_to_db
import spotify
import os

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
   # username=username,
    return user


def create_journal_entry(journal_input, time_stamp, category):
    """Create and return a journal entry."""

    journal = Journal(journal_input=journal_input,
                      time_stamp=time_stamp,
                      category=category)

    db.session.add(journal)
    db.session.commit()

    return journal


def get_journal_count(user_id):
    """Get journal count by user id."""

    # get journal count by user_id
    return Journal.query.filter_by(user_id=user_id).count()

    
    # check if this query is correct
    # i want to get the count of a logged in user's journal entries
    # to check and see if it is the user's first submission
    # so i can assign a specific flash message to their first entry
    return journal_entry


def create_meditations(track_name, artist_name, image_url, spotify_url, preview_link, user_id):
    """Create and return a new Spotify meditation track."""
    # overview of this function
    # for each meditation, create an object/instance with those arguments
    # add those to session

    spotify_username = os.environ["SPOTIFY_USERNAME"]
    spotify_playlist = os.environ["SPOTIFY_PLAYLIST_ID"]

    # access function from spotiy.py to retrieve the data from my spotify playlist
    # pass through username and playlist_id
    results = spotify.get_playlist_tracks(spotify_username, spotify_playlist)
    
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


def get_all_meditations():
    """Get and return all meditations."""

    # all_meditations = Meditation.query.all()
    all_meditations = Meditation.query.order_by(Meditation.track_name.desc()).all()

    return all_meditations
    # not sure if this is right?
    

def get_meditation_by_id(meditation_id):
    """Return a meditation by primary key."""
    
    # single_meditation = Meditation.query.filter_by(meditation_id=meditation_id).one()
    single_meditation = Meditation.query.get(meditation_id)
    
    return single_meditation


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


def get_friends_by_search_input(search_input):
    """Return all friends that match user's input."""

    search_results = Friend.query.filter(User.fname.ilike(f"%{search_input}%") | User.lname.ilike(f"%{search_input}%")).all()

    return search_results


def get_all_messages():
    """Get and return all pre-populated text messages"""

    messages = Message.query.all()

    return messages


def create_notification(date):
    """Create and return a scheduled notification."""

    notification = Notification(date=date)

    db.session.add(notification)
    db.session.commit()

    return notification

# def send_notification():

def create_favorite(meditation_id, user_id):
    """Create and return a user's favorite meditation."""

    fav = Favorite(meditation_id=meditation_id,
                        user_id=user_id)
    
    db.session.add(fav)
    db.session.commit()

    return fav


def remove_favorite(meditation_id, user_id):
    """Remove a user's favorite meditation."""

    removed_fav = Favorite.query.filter(Favorite.meditation_id, Favorite.user_id).first()

    db.session.delete(removed_fav)
    db.session.commit()

    return removed_fav





if __name__ == '__main__':
    from server import app
    connect_to_db(app)
