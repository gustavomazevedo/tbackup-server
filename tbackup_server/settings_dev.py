import os.path
from settings import BASE_DIR

DEBUG = True

SECRET_KEY = 'q@a8bm)&z^m6^^@@yn$#a4s6r3-eoa225g_u+6*5)ato(lmxz@'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}