import app
import os
from flask import send_from_directory, make_response, request, redirect
from sqlalchemy.sql.expression import func, select
from flask.ext.mobility.decorators import mobile_template
import twilio.twiml
import random

# special file handlers and error handlers
@app.flask_app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.flask_app.root_path, 'static'), 'img/favicon.ico')

@app.flask_app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

# routing for basic pages (pass routing onto the Angular app)
@app.flask_app.route('/')
@app.flask_app.route('/about')
def basic_pages():
    return make_response(open('app/public/template/index.html').read())

@app.flask_app.route('/twilio_receiver')
def twilio_receiver():
    from_number = request.values.get('From', None)
    body = request.values.get('Body', None)
    resp = twilio.twiml.Response()
    if body != 'HOPE':
        resp.message("Sorry, we didn't recognize your message.")
        try:
            app.flask_app.logger.debug('Message from %s: %s' % (from_number, body))
        except Exception, e:
            pass
    elif app.models.delete_phone(from_number):
        resp.message("We're awfully sorry to see you go, but we understand that sometimes hope isn't what we need. If that changes, don't be a stranger - we're here for you.")
    else:
        resp.message("Apologies, there seems to have been a mistake. Please try again.")
    return str(resp)

@app.flask_app.route('/save-phone', methods=['POST'])
def save_phone():
    try:
        phone = None
        phone_string = request.form['phone']
        if phone_string and len(phone_string) == 10:
            has_phone, phone = app.models.get_or_create_phone(phone_string)
        else:
            return app.utility.xhr_response({'success':False, 'msg':"Please submit a complete phone number."}, 200)

        if has_phone and phone.deleted:
            return app.utility.xhr_response({'success':False, 'msg':"Thanks for re-trying to connect with us. If you really are ready for more inspiration, email us at cinjon.resnick@gmail.com."}, 200)
        elif has_phone:
            return app.utility.xhr_response({'success':False, 'msg':'Thanks, but we already have this number. Hope is coming.'}, 200)
        else:
            phone.send_intro()
            return app.utility.xhr_response({'success':True, 'msg':'Thanks. Hope is on the way.'}, 200)
    except Exception, e:
        app.flask_app.logger.debug(e)
        return app.utility.xhr_response({'success':False, 'msg':'Apologies. We misheard you. Please submit again.'}, 200)

# @app.flask_app.route('/google34d3fe92d155a2aa.html')
# def google_verification(**kwargs):
#     return make_response(open('app/public/template/google34d3fe92d155a2aa.html').read())
