"""Send an sms using Twilio"""

# Download the helper library from https://www.twilio.com/docs/python/install
import os
from model import User, Message
from twilio.rest import Client
from dotenv import load_dotenv

# load environment variables from .env.
load_dotenv()  

# This code creates a new instance of the Message resource and sends an HTTP POST to the Message resource URI.

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# import random
# randomly select message to send in body
def txt_notifications():
    message = client.messages \
                    .create(
                        body="Thanks for signing up for notifications from Mindful Moments. YOU are always a priority :)",
                        # to=f"{random_txt_message}
                        from_='+14752588323',
                        to='+14803858041'
                        # to=f"{User.phone_num}"
                    )

    print(message.sid)

def scheduled_reminders():
    message = client.messages \
                    .create(
                        body="Thanks for signing up for notifications from Mindful Moments. YOU are always a priority :)",
                        # to=f"{random_txt_message}
                        from_='+14752588323',
                        to='+14803858041'
                        # to=f"{User.phone_num}"
                    )

    print(message.sid)


