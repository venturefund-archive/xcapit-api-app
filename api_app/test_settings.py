from api_app.settings import *

SECRET_KEY = 'asdasd'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TIME_ZONE': 'UTC',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

CLIENT_ID_1 = 'client_test'
CLIENT_ID_2 = 'client_test'
CLIENT_ID_3 = 'client_test'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SOUTH_TESTS_MIGRATE = False
