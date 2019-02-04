#!/usr/bin/python3

import json

from src import constants


def encode_to_json(file_name, lines):
    json_lines = []

    if_lines = []
    is_in_if = False
    is_in_elseif = False
    shift_amnt = 0
    for line in lines:
        encoded_line = encode_line(line, is_in_if, is_in_elseif, shift_amnt)

        if is_in_if:
            if_lines.append(encoded_line)
            pass
        else:
            json_lines.append(encoded_line)
            pass
        continue

    return json.dumps(
        {
            'file_name': file_name,
            'lines': json_lines
        },
        indent=constants.JSON_INDENT
    )


def encode_line(line, is_in_if, is_in_elseif, shift_amnt):
    line_number = line[0]
    line_text = line[1]

    encoded_line = line_text
    if line_text[0] == '@':
        encoded_line = encode_annotation(line_text)
        pass

    shift_start = 0
    shift_end = 0

    # TODO

    dumped = {
        'line_number': line_number,
        'line': encoded_line,
        'shiftStart': shift_start,
        'shiftEnd': shift_end
    }
    return {

    }


def encode_annotation_no_(line):
    new_line = line[1:]
    split = new_line.split(' ')

    if split[0] == 'if':  # Handle if statement
        return

    params = split[1:]

    encoded_params = []
    if len(params) > 0:
        for param in params:
            param_split = param.split('=')
            if len(param_split) >= 2:
                encoded_params.append(
                    {
                        'name': param_split[0],
                        'value': param_split[1]
                    }
                )
            else:
                encoded_params.append(
                    param_split[0]
                )
            continue
        pass

    dumped = {
        'type': 'annotation',
        'name': split[0],
        'params': encoded_params
    }

    return {
        'is_if': False,
        'is_else_if': False,
        'line': dumped
    }


def encode_if(line):
    return None
