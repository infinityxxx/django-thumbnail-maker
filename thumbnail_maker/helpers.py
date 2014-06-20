"""
Helper functions
"""
from sorl.thumbnail.conf import settings
from sorl.thumbnail.default import backend as sorl_backend


def get_thumbnail_options(file_, thumb_options=None):
    """
    Get all options of thumbnail, including default ones.
    """
    options = thumb_options.copy() if thumb_options else {}

    if settings.THUMBNAIL_PRESERVE_FORMAT:
        options.setdefault('format', sorl_backend._get_format(file_))

    for key, value in sorl_backend.default_options.items():
        options.setdefault(key, value)

    return options
