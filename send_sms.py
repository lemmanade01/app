"""Send an sms using Twilio"""

# Download the helper library from https://www.twilio.com/docs/python/install
import os
import random
import crud
from model import User, Message, Notification
from twilio.rest import Client
from datetime import datetime

# This code creates a new instance of the Message resource and sends an HTTP POST to the Message resource URI.

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
phone = os.environ["TWILIO_PHONE_NUM"]
client = Client(account_sid, auth_token)

# Get all messages
messages = crud.get_all_messages()

# Twilio Text Test
message = client.messages \
                    .create(
                        body=f"Thanks for signing up for notifications from Mindful Moments. YOU are always a priority :)",
                        from_=f"{phone}",
                        to="+1" # Fill in your number
                    )

print(message.sid)


# UNCOMMENT BEFORE DEPLOYMENT
# def scheduled_reminders():
#     """Send user their scheduled reminder via text
    
#     Reminders can be sent even when a user is not looged into flask session
#     """
#     ids = crud.get_all_user_ids()
#     two_hours = 60 * 60 * 2000;
#     now = datetime.now()
    
#     for user_id in ids:
#         reminders = crud.get_all_reminders(user_id)
        
#         for reminder in reminders:
#             if reminder.date - two_hours == now:
#                 reminder_type = reminder.reminder_type
#                 messages_one_type = crud.get_messages_by_type(reminder_type)
#                 message = random.choice(messages_one_type)
                
#                 this_user_id = reminder.user_id
#                 user = crud.get_user_by_id(this_user_id)
#                 phone_num = user.phone_num
                
#                 message = client.messages \
#                                 .create(
#                                     body=f"{message}",
#                                     # send the scheduled reminder at the right time, with the right message to the right user
#                                     from_=f"{phone}",
#                                     to=f"+1{phone_num}"
#                                 )

#     print(message.sid)
    
# scheduled_reminders()



# randomly select message to send in body
# def txt_notifications():
#     """Send user a randomized text message notification"""

#     message = client.messages \
#                     .create(
#                         body=f"{random.choice(messages.txt_message)}",
#                         # to=f"{random_txt_message}
#                         from_=f"{phone}",
#                         to=f"+1{User.phone_num}"
#                     )

    # print(message.sid)