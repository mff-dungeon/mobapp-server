"""
Django settings for server project. Debug mode.
"""

from .common_settings import *

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

DEBUG = True

SECRET_KEY = 'ri$+ha8m13fts%w@iekz17lr!74r%7ctun#*%!&quwedc_q%+g'
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'local.db',
    }
}
