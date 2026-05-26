from .base import *

DEBUG = True
ALLOWED_HOST = ['*']

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : 'sjd_db',
        'USER' : 'root',
        'PASSWORD' : 'zinobegildany12',
        'HOST' : '127.0.0.1',
        'PORT' : '3306'
    }
}