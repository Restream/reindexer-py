# -*- coding: utf-8 -*-
import logging
import os
from datetime import *


class OneLineExceptionFormatter(logging.Formatter):
    """ One line log output
    https://docs.python.org/2/howto/logging-cookbook.html#logging-cookbook
    """
    def formatException(self, exc_info):
        result = super(OneLineExceptionFormatter, self).formatException(exc_info)
        return repr(result) # or format into one line however you want to

    def format(self, record):
        result = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            result = result.replace('\n', '') + '|'
        return result


# Create logger
log_operation = logging.getLogger('OPERATION')
log_fixture = logging.getLogger('FIXTURE')
log_error = logging.getLogger('ERROR')

log_operation.setLevel(logging.INFO)
log_fixture.setLevel(logging.INFO)
log_error.setLevel(logging.ERROR)

# Log format
formatter = OneLineExceptionFormatter('%(levelname)-5s [%(asctime)s] [%(name)s]: %(message)s')

# Save log to file
log_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs/')
if not os.path.exists(log_folder):
            os.makedirs(log_folder)
log_filename = os.path.join(os.path.dirname(log_folder), 'test_run_%s.txt' % (datetime.now().strftime('%d%b-%H:%M:%S')))

file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
log_operation.addHandler(file_handler)
log_fixture.addHandler(file_handler)
