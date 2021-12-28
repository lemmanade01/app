from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import flash
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mssql import INTEGER, VARCHAR  # Assuming SQL Server
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()
Base = declarative_base()

# class UserFriend(db.Model):
#     """Association table between User and Friend"""

#     __tablename__ = "users_friends"

#     user_friend_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
#     friend_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)


# usersfriends = Table(
#     'UsersFriends',
#     Base.metadata,
#     Column('users_friend_id', INTEGER, primary_key=True),
#     Column('user_id', INTEGER, ForeignKey('Users.user_id')),
#     Column('friend_id', INTEGER, ForeignKey('User.user_id'))
#     )
# association_table = Table('association', Base.metadata,
#     Column('left_id', ForeignKey('left.id'), primary_key=True),
#     Column('right_id', ForeignKey('right.id'), primary_key=True)
# )

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
    meditation_id = db.Column(db.Integer, db.ForeignKey("meditations.meditation_id"), nullable=False)
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
    journal_input = db.Column(db.Text, nullable=False)
    time_stamp = db.Column(db.DateTime)
    category = db.Column(db.String)
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


# the cloned repo had this class commented out
class Friend(db.Model):
    """A user's friend"""

    __tablename__ = "friends"

    friend_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    friend = db.Column(db.Integer)

    # user
    # (db.relatiionship("Friend", secondary="users_friends", backref="user") on User model)

    def __repr__(self):
        return f"<Friend friend_id={self.friend_id}>"


class Notification(db.Model):
    """A scheduled reminder"""

    __tablename__ = "notifications"

    notification_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    date = db.Column(db.DateTime, nullable=True)
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
                           autoincrement=True,
                           primary_key=True)
    txt_message = db.Column(db.Text, nullable=False)

    notifications = db.relationship("Notification", backref="message")
    # a message can have many notifications, but a notifcation can't have many messages

    def __repr__(self):
        return f"<Message message_id={self.message_id} txt_message={self.txt_message}>"


class Quote(db.Model):
    """A pre-populated set of quotes"""

    __tablename__ = "quotes"

    quote_id = db.Column(db.Integer,
                         autoincrement=True,
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