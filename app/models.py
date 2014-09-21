from app import db
from app import utility
from app import config
import random
import os
import datetime
from sqlalchemy.sql import func
from twilio.rest import TwilioRestClient
import message_options
from crontab import CronTab
from flask.ext.script import Command

class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_string = db.Column(db.String(25)) #International.
    creation_time = db.Column(db.DateTime)
    messages = db.relationship('Message', lazy='dynamic', backref='phone')
    deleted = db.Column(db.Boolean)
    sent_intro = db.Column(db.Boolean)

    def __init__(self, phone_string):
        self.phone_string = phone_string
        self.creation_time = utility.get_time()
        self.deleted = False
        self.sent_intro = False

    def delete(self):
        self.deleted = True
        app.db.session.commit()

    def send_intro(self):
        selection = get_selection(self, message_options.i)
        message = create_message(self.id, selection)
        if message and message.send(self):
            self.sent_intro = True
            app.db.session.commit()
        else:
            app.flask_app.logger.debug('Phone %s had intro send fail' % self.phone_string)

def create_phone(phone_string, commit=True):
    if Phone.query.filter(Phone.phone_string == phone_string).count() > 0:
        app.flask_app.logger.debug('Phone already exists: %s' % phone_string)
        return None
    phone = Phone(phone_string)
    if commit:
        db.session.add(phone)
        db.session.commit()
    return phone

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    selection = db.Column(db.Integer) # index of message in message_options
    creation_time = db.Column(db.DateTime)
    sent_time = db.Column(db.DateTime)
    phone_id = db.Column(db.Integer, db.ForeignKey('phone.id'))

    def __init__(self, selection):
        self.selection = selection
        self.creation_time = utility.get_time()

    def send(self, phone=None):
        phone = phone or Phone.query.get(self.phone_id)
        body = message_options.options[self.selection]['body']
        if send_by_twilio(phone, body):
            self.sent_time = utility.get_time()
            db.session.commit()
            return True
        return False

def create_message(phone_id, selection=None, commit=True):
    phone = Phone.query.get(phone_id)
    if not phone or phone.deleted:
        return
    selection = selection or get_selection(phone)
    message = Message(selection)
    if commit:
        db.session.add(message)
        db.session.commit()
    return message

def filter_options(ty):
    return [option for option in options if option['type'] == ty]

def get_selection(phone, option_type=None):
    """
    Gets the next selection for the given phone
    If this is the 1st or 2nd message, gets a hopeful msg
    If this is the 3rd message, gets a death msg
    Tries to keep ~= the counts per message (for a given phone).
    """
    messages = phone.messages.query.all() or []
    options = message_options.options
    if option_type:
        options = filter_options(option_type)
    elif len(messages) < 3: # first or second message (first is an intro msg)
        options = filter_options(message_options.h)
    elif len(messages) == 3: # third message
        options = filter_options(message_options.d)

    counts = sorted([(index, messages.count(index)) for index,_ in enumerate(options)],
                    key = lambda message: message[1])
    return counts[0]

from_phone="+14158010048"
ACCOUNT_SID = os.environ['LEPETITMORT_TWILIO_SID']
AUTH_TOKEN = os.environ['LEPETITMORT_TWILIO_TOKEN']
twilio_client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
def send_by_twilio(to_phone, message):
    try:
        twilio_client.messages.create(
            to=to_phone,
            from_=from_phone,
            body=message,
            status_callback='/twilio_callback'
        )
        return True
    except:
        return False

class Cron(Command):
    # TODO: Incomplete
    """Runs cron for sending messages"""
    def __init__(self, days_since_msg=7, avg_msg_days=14, max_msg_days=21):
        self.days_since_msg = days_since_msg # num days since last message
        self.avg_msg_days = avg_msg_days # avg num of days since last message for any user
        self.max_msg_days = max_msg_days # max num of days since last message for any user

    def run(self):
        cron = CronTab()

        try:
            messages = []
            for phone in self.get_phones():
                msg = create_message(phone.id, commit=False)
                app.db.session.add(message)
                messages.append((phone, msg))
            app.db.session.commit()

            for phone, message in messages:
                message.send(phone)
        except Exception, e:
            app.flask_app.logger.debug('Cron failed: %s.' % e)
            return

    def get_phones(self):
        today = datetime.datetime.now()
        latest_msg_by_phone = Message.query(Message.phone_id, func.max(Message.sent_time)).group_by(Message.phone_id)
        return []
