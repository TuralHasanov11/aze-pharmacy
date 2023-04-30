from django.conf import settings
from django.shortcuts import render
from twilio.rest import Client

account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)


conversation = client.conversations \
                     .v1 \
                     .conversations \
                     .create(friendly_name='My First Conversation')

conversation = client.conversations \
                     .v1 \
                     .conversations('CHXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX') \
                     .fetch()

print(conversation.chat_service_sid)