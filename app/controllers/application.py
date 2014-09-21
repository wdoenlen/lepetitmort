import app
import os
from flask import send_from_directory, make_response, request, redirect
from  sqlalchemy.sql.expression import func, select
from flask.ext.mobility.decorators import mobile_template
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

@app.flask_app.route('/twilio_callback')
def twilio_receiver():
    print request.form['SmsStatus']

@app.flask_app.route('/save-phone', methods=['POST'])
def save_phone():
    try:
        phone = None
        phone_string = request.form['phone']
        if phone_string and len(phone_string) == 10:
            phone = app.models.create_phone(phone_string)
        if phone:
            phone.send_intro()
            return app.utility.xhr_response({'success':True, 'msg':'Thanks. Hope is on the way.'}, 200)
        else:
            return app.utility.xhr_response({'success':False, 'msg':'Thanks, but we already have this number. Hope is coming.'}, 200)
    except Exception, e:
        return app.utility.xhr_response({'success':False, 'msg':'Apologies. We misheard you. Please submit again.'}, 200)


# @app.flask_app.route('/google34d3fe92d155a2aa.html')
# def google_verification(**kwargs):
#     return make_response(open('app/public/template/google34d3fe92d155a2aa.html').read())
