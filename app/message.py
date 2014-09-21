from twilio.rest import TwilioRestClient
import os

# put your own credentials here
ACCOUNT_SID = os.environ['TWILIO_SID']
AUTH_TOKEN = os.environ['TWILIO_TOKEN']

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)