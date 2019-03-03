#!/usr/bin/python3

import json

if not __debug__:
    from src import constants
else:
    import constants


def encode_to_json(file_name, lines):
    script_lines = []

    for line in lines:
        encoded_line = encode_line(line)
        if encoded_line is None:
            continue
        script_lines.append(encoded_line)
        continue

    return json.dumps(
        {
            'file_name': file_name,
            'lines': script_lines
        },
        indent=constants.JSON_INDENT,
        ensure_ascii=False
    )


def encode_line(line):
    line_number = line[0]
    line_text = line[1]

    shift_start = 0
    shift_end = 0

    tmp_line = line_text

    while tmp_line.startswith('\t'):
        shift_start += 1
        tmp_line = tmp_line[1:]
        continue

    while tmp_line.endswith('\t'):
        shift_end += 1
        tmp_line = tmp_line[:len(tmp_line) - 1]
        continue

    if tmp_line == '':
        return None

    if tmp_line[0] == '@':
        encoded_line = encode_annotation(tmp_line)
        pass
    else:
        encoded_line = {
            'type': 'text',
            'value': tmp_line
        }
        pass

    dumped = {
        'line_number': line_number,
        'line': encoded_line,
        'shiftStart': shift_start,
        'shiftEnd': shift_end
    }
    return dumped


def encode_annotation(line):
    new_line = line[1:]
    split = new_line.split(' ')

    name = split[0]
    params = split[1:]

    encoded_params = []
    if len(params) > 0:
        for param in params:
            param_split = param.split('=')
            if len(param_split) >= 2:
                param_name = param_split[0]
                param_value = param_split[1]

                multiple = ',' in param_value
                if multiple:
                    param_value = param_value.split(',')
                    pass

                encoded_params.append(
                    {
                        'name': param_name,
                        'value': param_value
                    }
                )
                pass
            else:
                encoded_params.append(param_split[0])
                pass
            continue
        pass

    return {
        'type': 'annotation',
        'name': name,
        'params': encoded_params
    }
