# -*- encoding: utf8 -*-
from __future__ import unicode_literals

import logging

__author__ = "Tamara Khalbashkeeva"
__license__ = "BSD"
__version__ = '0.0.1a'
__email__ = "infinityxxx@gmail.com"
__status__ = "Alpha"


class NullHandler(logging.Handler):
    def emit(self, record):
        pass

# Add a logging handler that does nothing to silence messages with no logger
# configured
logging.getLogger('sorl').addHandler(NullHandler())
