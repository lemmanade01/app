from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import flash
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()
# Base = declarative_base()

# creating relationship from user to users --> their friends
# doing that with many-to-many relationship (line 35, friend end)
# association table (line 13)
# your user id a bunch of times and then other friends ids

user_to_user = db.Table("user_to_user", db.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("users.user_id"), primary_key=True),
    db.Column("friend_id", db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
)

class User(db.Model):

    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone_num = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    quote = db.Column(db.String(200))

    # decide if i want the user to have a username
    # username = db.Column(db.String(20), unique=True, nullable=False)

    friend = db.relationship("User",
                        secondary="user_to_user",
                        primaryjoin="User.user_id==user_to_user.c.user_id",
                        secondaryjoin="User.user_id==user_to_user.c.friend_id",
                        backref="friends"
                        )
    # creating two different ends of the same relationship -- friend --> friends
    
    # we have friends
    # and we are a friend to many other users

    # a user is a friend of and friends with
    
    journals = db.relationship("Journal", backref="user")
    # a user can have many journals, but a journal can't have many users
    meditations = db.relationship("Meditation", backref="user")
    # a user can have many meditations, but a meditation can't have many users
    notifications = db.relationship("Notification", backref="user")
    # a user can have many notifications, but a notifcation can't have many users
    favorites = db.relationship("Favorite", backref="user")
    # a user can have many favorites, but a favorite can't have many users

    # friends = db.relationship("Friend", secondary="users_friends", backref="users")
    # Friend and User have a many-to-many relationship 
    # friend = db.relationship("User", 
    #                         secondary=usersfriends,
    #                         primaryjoin=user_id == usersfriends.c.friend_id,
    #                         secondaryjoin=user_id == usersfriends.c.user_id,
    #                         backref="friends") 
      
    def __repr__(self):
        return f"<User fname={self.fname} lname={self.lname} email={self.email}>"


class Meditation(db.Model):
    """A meditation"""

    __tablename__ = "meditations"

    meditation_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    track_name = db.Column(db.String(100), nullable=False)
    artist_name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String)
    spotify_url = db.Column(db.String, nullable=False)
    preview_link = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    favorites = db.relationship("Favorite", backref="meditation")
    # journal
    # (db.relationship("Meditation", secondary="meditations_journals", backref="journal") on Journal model)


class Favorite(db.Model):
    """A user's saved meditation"""

    __tablename__ = "favorites"

    fav_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    meditation_id = db.Column(db.Integer, db.ForeignKey("meditations.meditation_id"), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    # user
    # (db.realtionship("Favorite", backref="user") on User model)

    # meditation
    # (db.relationship("Favorite", backref="meditation") on Meditation model)

    def __repr__(self):
        f"<Favorite fav_id={self.fav_id} meditation_id={self.meditation_id} user_id={self.user_id}>"


class Journal(db.Model):
    """A journal entry"""

    __tablename__ = "journals"

    journal_id = db.Column(db.Integer, 
                           autoincrement=True,
                           primary_key=True)
    mood = db.Column(db.String(25), nullable=False)
    color = db.Column(db.String(7), nullable=False)
    gratitude_1 =db.Column(db.String(200), nullable=False)
    gratitude_2 =db.Column(db.String(200), nullable=False)
    gratitude_3 =db.Column(db.String(200), nullable=False)
    journal_input = db.Column(db.Text, nullable=False)
    time_stamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    
    # user
    # (db.relationship("Journal", backref="user") on User model)
    meditations = db.relationship("Meditation", secondary="meditations_journals", backref="journals")
    # Journal and Meditation have a many-to-many relationship    
    
    def __repr__(self):
        return f"<Journal journal_id={self.journal_id} user_id={self.user_id} time_stamp={self.time_stamp}>"
    

class MeditationJournal(db.Model):
    """An association table for Meditation and Journal"""

    __tablename__ = "meditations_journals"

    meditation_journal_id = db.Column(db.Integer, 
                                      autoincrement=True,
                                      primary_key=True)
    meditation_id = db.Column(db.Integer, db.ForeignKey("meditations.meditation_id"), nullable=False)
    journal_id = db.Column(db.Integer, db.ForeignKey("journals.journal_id"), nullable=False)
    
    # user
    # (db.relationship("Meditation", backref="user") on User model)

    def __repr__(self):
        return f"<Media meditation_id={self.media_id} title={self.title}>"


class Notification(db.Model):
    """A scheduled calendar reminder"""

    __tablename__ = "notifications"

    notification_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    date = db.Column(db.DateTime, nullable=True)
    reminder_type = db.Column(db.String(25), nullable=True) 
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey("messages.message_id"), nullable=False)

    # user
    # (db.relationship("Notification", backref="user") on User model)
    # message
    # (db.relationship("Notification", backref="message") on Message model)
   
    def __repr__(self):
        return f"<Notification notification_id={self.notification_id} date={self.date} user_id={self.user_id}>"


class Message(db.Model):
    """A pre-populated set of messages"""

    __tablename__ = "messages"

    message_id = db.Column(db.Integer,
                           primary_key=True)
    txt_message = db.Column(db.Text, nullable=False)
    reminder_type = db.Column(db.String(25), nullable=False)

    notifications = db.relationship("Notification", backref="message")
    # a message can have many notifications, but a notifcation can't have many messages

    def __repr__(self):
        return f"<Message message_id={self.message_id} txt_message={self.txt_message}>"


class Quote(db.Model):
    """A pre-populated set of quotes"""

    __tablename__ = "quotes"

    quote_id = db.Column(db.Integer,
                         primary_key=True)
    inspo_quote = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100))

    def __repr__(self):
        return f"<Quote inspo_qute={self.inspo_quote} author={self.author}>"


class Tip(db.Model):
    """A pre-populated set of wellness tips"""

    __tablename__ = "tips"

    tip_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    wellness_tip = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(150))
   
    def __repr__(self):
        return f"<Tip tip_id={self.tip_id} wellness_tip={self.wellness_tip}>"


def connect_to_db(flask_app, db_uri="postgresql:///meditations", echo=True):
#///<meditations> should be the db_name
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)