import os
from twilio.rest import Client

account_sid="AC961eb8256addcabce6da96cf3ebd2b54"
auth_token="3e36d406612d56c2a1e31a69e7fb217b"
client=Client(account_sid,auth_token)
def send_sms(user_code,phone_number):
    message=client.messages.create(
        body=f" Hi! your verification code is {user_code}",
        from_= "+12678634571",
        to=f"+880{phone_number}"
    )
    print(message.sid)


