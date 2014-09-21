from app import db
from app import utility
from app import config
import random
import os
import message_options

class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_string = db.Column(db.String(25)) #International.
    creation_time = db.Column(db.DateTime)
    messages = db.relationship('Message', lazy='dynamic', backref='phone')

    def __init__(self, phone_string):
        self.phone_string = phone_string
        self.creation_time = utility.get_time()

def create_phone(phone_string, commit=True):
    phone = Phone(phone_string)
    if commit:
        db.session.add(phone)
        db.session.commit()
    return phone

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    selection = db.Column(db.Integer) # index of message in message_options
    creation_time = db.Column(db.Datetime)
    sent_time = db.Column(db.Datetime)
    phone_id = db.Column(db.Integer, db.ForeignKey('phone.id'))

    def __init__(self, selection):
        self.selection = selection
        self.creation_time = utility.get_time()

    def send(self):
        phone = Phone.query.get(self.phone_id)
        message = message_options.options[self.selection]['body']
        # send twilio msg to number:phone with body:message
        pass

def create_message(phone_id, selection=None, commit=True):
    phone = Phone.query.get(phone_id)
    if not phone:
        return
    selection = selection or get_selection(phone)
    message = Message(selection)
    if commit:
        db.session.add(message)
        db.session.commit()
    return message

def get_selection(phone):
    """
    Gets the next selection for the given phone
    If this is the 1st or 2nd message, gets a hopeful msg
    If this is the 3rd message, gets a death msg
    Tries to keep ~= the counts per message (for a given phone).
    """
    messages = phone.messages.query.all()
    options = message_options.options
    if len(messages) < 2: # first or second message
        options = [option for option in options if option['type'] == message_options.h]
    elif len(messages) == 2: # third message
        options = [option for option in options if option['type'] == message_options.d]

    counts = sorted([(index, messages.count(index)) for index,_ in enumerate(options)],
                    key = lambda message: message[1])
    return counts[0]
