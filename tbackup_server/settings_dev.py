import os.path
from settings import BASE_DIR

DEBUG = True

SECRET_KEY      = 'q@a8bm)&z^m6^^@@yn$#a4s6r3-eoa225g_u+6*5)ato(lmxz@'
R_SIGNATURE_KEY = 'ae+c5l(^@653f-hp_e8s*@l)knb30&s4a#$n&^6^@-o25_*)tz'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}