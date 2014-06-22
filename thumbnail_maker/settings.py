"""
Settings
"""
from django.conf import settings


THUMBNAIL_MAKER_FORMATS = getattr(settings, 'THUMBNAIL_MAKER_FORMATS', ())
