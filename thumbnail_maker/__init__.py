# -*- encoding: utf8 -*-
"""
Thumbnail-maker module
"""
from __future__ import unicode_literals

import logging

__author__ = "Tamara Khalbashkeeva"
__license__ = "BSD"
__version__ = '0.0.3'
__email__ = "infinityxxx@gmail.com"


class NullHandler(logging.Handler):
    """
    Dummy log handler
    """
    def emit(self, record):
        pass

# Add a logging handler that does nothing to silence messages
# with no logger configured
logging.getLogger('sorl').addHandler(NullHandler())
