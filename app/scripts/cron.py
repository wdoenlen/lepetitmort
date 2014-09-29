import app
from app.models import Message
import random
import datetime
from sqlalchemy.sql import func

min_msg_days = 7 # min num days since last message
max_msg_days = 14 # max num days since last message

def greet():
    app.flask_app.logger.debug('Cron: Hi')

def run(min_days=None, max_days=None, test=False):
    min_days = min_days or min_msg_days
    max_days = max_days or max_msg_days

    messages = []
    phones = get_phones_on_tap(min_days, max_days)
    app.flask_app.logger.debug('Cron: Creating %d Messages' % len(phones))
    for phone_id in phones:
        try:
            msg = app.models.create_message(phone_id, commit=False)
            app.db.session.add(msg)
            app.flask_app.logger.debug('Loaded up message with selection %d for phone %d' % (msg.selection, phone_id))
            messages.append((phone_id, msg))
        except Exception, e:
            app.flask_app.logger.debug('Failed to load message for phone %d' % phone_id)
            app.flask_app.logger.debug(e)
    app.flask_app.logger.debug('Cron: Finished Creating Messages')

    if not test:
        app.flask_app.logger.debug('Cron: Committing')
        app.db.session.commit()

    app.flask_app.logger.debug('Cron: Sending Messages')
    for phone_id, message in messages:
        try:
            if test:
                app.flask_app.logger.debug(message.get_body())
            else:
                message.send(app.models.Phone.query.get(phone_id))
                app.db.session.commit()
        except Exception, e:
            app.flask_app.logger.debug('Failed to send message with selection %d for phone %d' % (message.selection, phone_id))
            app.flask_app.logger.debug(e)
    app.flask_app.logger.debug('Cron: Sent Messages')

def get_phones_on_tap(min_days, max_days):
    ret = []
    today = datetime.datetime.now()
    delta_min = datetime.timedelta(min_days)
    delta_max = datetime.timedelta(max_days)
    for phone_id, time in app.db.session.query(Message.phone_id, func.max(Message.sent_time)).group_by(Message.phone_id):
        if not phone_id or not time:
            # Likely a bad phone number which then didn't send an intro message
            continue
        delta = today - time
        if delta < delta_min:
            continue
        elif delta >= delta_max or 1.0 * delta.seconds / day_to_secs(max_days - min_days) > random.random():
            ret.append(phone_id)
    return ret

def day_to_secs(day):
    if day == None or day < 0:
        return None
    return day * 24 * 60 * 60
