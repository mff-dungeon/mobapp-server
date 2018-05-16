from .common_settings import *

ADMINS = [ ('Aearsis', 'aearsis@eideo.cz') ]
SERVER_EMAIL = 'app96614067@heroku.com'

EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '9ac984c2961df3'
EMAIL_HOST_PASSWORD = '97f40f167e74b6'
EMAIL_PORT = '2525'

# Configure Django App for Heroku.
import django_heroku
django_heroku.settings(locals())

