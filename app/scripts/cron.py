import app
from app.models import Message
import random
import datetime
from sqlalchemy.sql import func

min_msg_days = 7 # num days since last message
max_msg_days = 14 # max num of days since last message for any user

def test():
    app.flask_app.logger.debug('Hi in test')

def run(min_days=None, max_days=None, test=False):
    min_days = min_days or min_msg_days
    max_days = max_days or max_msg_days

    messages = []
    for phone_id in get_phones_on_tap(min_days, max_days):
        try:
            msg = app.models.create_message(phone_id, commit=False)
            app.db.session.add(msg)
            app.flask_app.logger.debug('Loaded up message with selection %d for phone %d' % (msg.selection, phone_id))
            messages.append((phone_id, msg))
        except Exception, e:
            app.flask_app.logger.debug('Failed to load message for phone %d' % phone_id)
            app.flask_app.logger.debug(e)

    if not test:
        app.db.session.commit()

    for phone_id, message in messages:
        try:
            if test:
                app.flask_app.logger.debug(message.get_body())
            else:
                message.send(app.models.Phone.query.get(phone_id))
        except Exception, e:
            app.flask_app.logger.debug('Failed to send message with selection %d for phone %d' % (message.selection, phone_id))
            app.flask_app.logger.debug(e)

    if not test:
        app.db.session.commit()

def get_phones_on_tap(min_days, max_days):
    ret = []
    today = datetime.datetime.now()
    delta_min = datetime.timedelta(min_days)
    delta_max = datetime.timedelta(max_days)
    for phone_id, time in app.db.session.query(Message.phone_id, func.max(Message.sent_time)).group_by(Message.phone_id):
        if not phone_id or not time:
            app.flask_app.logger.warn('WARN get_phones_on_tap had no value on phone_id ' + phone_id + ' or time ' + time)
            continue
        delta = today - time
        if delta < delta_min:
            continue
        elif delta >= delta_max or 1.0 * delta.days / (max_days - min_days) > random.random():
            ret.append(phone_id)
    return ret
