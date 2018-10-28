from __future__ import unicode_literals
import os
import os.path


PROJ_ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_ROOT = os.path.join(PROJ_ROOT, 'data')

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db'
    }
}

INSTALLED_APPS = (
    'django.contrib.contenttypes',

    'sorl.thumbnail',
    'thumbnail_maker',

    'testapp',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
)

SITE_ID = 1

MEDIA_ROOT = os.path.join(PROJ_ROOT, 'media')
MEDIA_URL = '/media/'

#ROOT_URLCONF = 'testapp.urls'

# Required for Django 1.4+
STATIC_URL = '/static/'

# Required for Django 1.5+
SECRET_KEY = 'abc123'

# Required for Django 1.7
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

THUMBNAIL_MAKER_FORMATS = {
    'big':    ('500x400', {'crop': 'center', 'quality': 100}),
    'medium': ('200x150', {'crop': 'center'}),
    'small':  ('80x80',   {'crop': 'center'}),
}

#TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'
