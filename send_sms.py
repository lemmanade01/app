"""Send an sms using Twilio"""

# Download the helper library from https://www.twilio.com/docs/python/install
import os
import random
import crud
from model import User, Message, Notification
from twilio.rest import Client
from dotenv import load_dotenv

# load environment variables from .env.
load_dotenv()  

# This code creates a new instance of the Message resource and sends an HTTP POST to the Message resource URI.

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

# is this okay i have global variables???
messages = crud.get_all_messages()
phone = os.environ["TWILIO_PHONE_NUM"]


# randomly select message to send in body
def txt_notifications():
    """Send user a randomized text message notification"""

    message = client.messages \
                    .create(
                        body=f"{random.choice(messages.txt_message)}",
                        # to=f"{random_txt_message}
                        from_=f"{phone}",
                        to=f"+1{User.phone_num}"
                    )

    print(message.sid)
    # make this the initial message
    # "Thanks for signing up for notifications from Mindful Moments. YOU are always a priority :)"


def scheduled_reminders():
    """Send user their scheduled reminder via text"""

    message = client.messages \
                    .create(
                        body=" ",
                        # send the scheduled reminder at the right time, with the right message to the right user
                        from_=f"{phone}",
                        to=f"+1{User.phone_num}"
                    )

    print(message.sid)