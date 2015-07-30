from app import db
from app import utility
from app import config
from app import flask_app as fapp
import random
import os
import datetime
from twilio.rest import TwilioRestClient
import message_options
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
        db.session.commit()

    def send_intro(self):
        selection = get_selection(self, message_options.i)
        message = create_message(self.id, selection=selection)

        if message and message.send(self):
            self.sent_intro = True
            db.session.commit()
        else:
            fapp.logger.debug('Phone %s had intro send fail' % self.phone_string)

    def send_growth(self):
        selection = get_selection(self, message_options.g)
        message = create_message(self.id, selection=selection)
        if not message.send(self):
            fapp.logger.debug('Phone %s had growth send fail.' % self.phone_string)

    def send_reintro(self):
        selection = get_selection(self, message_options.r)
        message = create_message(self.id, selection=selection)
        if not message.send(self):
            fapp.logger.debug('Phone %s had re-intro send fail' % self.phone_string)

def delete_phone(numstr):
    if not numstr:
        return False
    if len(numstr) == 12 and numstr[:2] == '+1':
        phone = Phone.query.filter(Phone.phone_string == numstr[2:]).first()
        if not phone:
            return False
        phone.deleted = True
        db.session.commit()
        return True
    else: # intl #
        return False

def get_or_create_phone(phone_string, commit=True):
    if Phone.query.filter(Phone.phone_string == phone_string).count() > 0:
        return True, Phone.query.filter(Phone.phone_string == phone_string).first()
    return False, create_phone(phone_string, commit)

def create_phone(phone_string, commit=True):
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

    def get_body(self, signature=True):
        body = message_options.options[self.selection]['body']
        if signature:
            body += '\n- Hint Of Hope'
        return body

    def send(self, phone=None):
        phone = phone or Phone.query.get(self.phone_id)
        body = self.get_body()
        if send_by_twilio(phone.phone_string, body):
            self.sent_time = utility.get_time()
            db.session.commit()
            return True
        return False

def create_message(phone_id, selection=None, commit=True):
    phone = Phone.query.get(phone_id)
    if not phone or phone.deleted:
        return
    if selection == None:
        selection = get_selection(phone)
    message = Message(selection)
    phone.messages.append(message)
    if commit:
        db.session.add(message)
        db.session.commit()
    return message

def filter_options(ty):
    return [option for option in message_options.options if option['type'] == ty]

first_d_message = 4 # first death msg
def get_option_type(messages):
    if len(messages) < first_d_message:
        return message_options.h
    elif len(messages) == first_d_message:
        return message_options.d
    return None

def get_selection(phone, option_type=None):
    """
    Gets the next selection for the given phone
    If this is the 1st, 2nd, or 3rd message, gets a hopeful msg
    If this is the 4th message, gets a death msg
    Tries to keep ~= the counts per message (for a given phone).
    """
    def check_selection(option_type, selection_type):
        if option_type == None:
            return selection_type != message_options.i and \
                   selection_type != message_options.r and \
                   selection_type != message_options.g
        return selection_type == option_type

    messages = phone.messages.all() or []
    message_selections = [m.selection for m in messages]
    if not option_type:
        option_type = get_option_type(messages)
    counts = sorted(
        [{'index':index, 'count':message_selections.count(index)} for index, option in enumerate(message_options.options) if check_selection(option_type, option['type'])],
        key = lambda message: message.get('count'))
    counts = [c for c in counts if c['count'] == counts[0]['count']]
    random.shuffle(counts)
    return counts[0]['index']

from_phone="+14158010048"
twilio_client = TwilioRestClient(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
def send_by_twilio(to_phone, message):
    try:
        twilio_client.messages.create(
            to=to_phone,
            from_=from_phone,
            body=message,
            # status_callback=config.baseurl+'/twilio_callback'
        )
        return True
    except Exception, e:
        fapp.logger.debug(e)
        return False
