# -*- coding: utf-8 -*-
import logging
import os
import sys
from datetime import *


class OneLineExceptionFormatter(logging.Formatter):
    """ One line log output
    https://docs.python.org/2/howto/logging-cookbook.html#logging-cookbook
    """

    def formatException(self, exc_info):
        result = super(OneLineExceptionFormatter, self).formatException(exc_info)
        return repr(result)

    def format(self, record):
        result = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            result = result.replace('\n', '') + '|'
        return result


# Create logger
log_api = logging.getLogger('API')
log_fixture = logging.getLogger('FIXTURE')
log_error = logging.getLogger('ERROR')

log_api.setLevel(logging.INFO)
log_fixture.setLevel(logging.INFO)
log_error.setLevel(logging.ERROR)

# Log format
formatter = OneLineExceptionFormatter('%(levelname)-5s [%(asctime)s] [%(name)s]: %(message)s')

# Log to console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
log_api.addHandler(console_handler)
log_fixture.addHandler(console_handler)

# Save log to file
log_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs/')
if not os.path.exists(log_folder):
    os.makedirs(log_folder)
log_filename = os.path.join(os.path.dirname(log_folder), 'test_run_%s.txt' % (datetime.now().strftime('%d%b-%H:%M:%S')))

file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
log_api.addHandler(file_handler)
log_fixture.addHandler(file_handler)
