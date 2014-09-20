import os
CSRF_ENABLED = True
SECRET_KEY = os.environ.get('DEATH_SECRET_KEY')
basedir = os.path.abspath(os.path.dirname(__file__))
baseurl = os.environ.get('DEATH_BASE_URL', None)
SQLALCHEMY_DATABASE_URI = os.environ.get('DEATH_DATABASE_URL', None)
