#!/usr/bin/python3

import json

if not __debug__:
    from src import json_decode
    from src.log import Log
else:
    import json_decode
    from log import Log


def encode(input_file):
    Log.log_to_file(True, 'Encoding input file {}...'.format(input_file))
    read_json_file = read(input_file)
    decoded_json_file = json_decode.decode_from_json(read_json_file)
    return decoded_json_file


def read(input_file):
    opened_input_file = open(input_file, 'r+t', encoding='utf8')
    input_json_file = json.load(opened_input_file)
    opened_input_file.close()
    return input_json_file
