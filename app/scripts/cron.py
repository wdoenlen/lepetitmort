import app

days_since_msg = 7 # num days since last message
avg_msg_days   = 14  # avg num of days since last message for any user
max_msg_days   = 17 # max num of days since last message for any user

def run(days=None, avg_days=None, max_days=None):
    days = days or days_since_msg
    avg_days = avg_days or avg_msg_days
    max_days = max_days or max_msg_days

    try:
        messages = []
        for phone in get_phones_on_tap(days, avg_days, max_days):
            msg = create_message(phone.id, commit=False)
            app.db.session.add(message)
            app.flask_app.logger.debug('Loaded up message %d for phone %s' % (msg.id, phone.phone_string))
            messages.append((phone, msg))
        app.db.session.commit()

        for phone, message in messages:
            message.send(phone)
    except Exception, e:
        app.flask_app.logger.debug('Cron failed: %s' % e)

def get_phones_on_tap(days, avg_days, max_days):
    # TODO
    today = datetime.datetime.now()
    latest_msg_by_phone = Message.query(Message.phone_id, func.max(Message.sent_time)).group_by(Message.phone_id)
    return []
