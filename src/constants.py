#!/usr/bin/python3

import sys

MODE_DECODE = 'DECODE'
MODE_ENCODE = 'ENCODE'

JSON_INDENT = 2

END_LINE = '\n'

if sys.platform == 'linux':
    SEPARATOR = '/'
    pass
else:
    SEPARATOR = '\\'
    pass
