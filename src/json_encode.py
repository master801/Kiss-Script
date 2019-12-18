#!/usr/bin/python3

import json

if not __debug__:
    from src import constants
    from src import config
else:
    import constants
    import config


def encode_to_json(file_name, lines):
    script_lines = []

    for line in lines:
        encoded_line = encode_line(line)

        if len(encoded_line) < 1:
            continue

        script_lines.extend(encoded_line)
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
    dumped = []

    line_number = line[0]
    line_text: str = line[1]

    shift_start = 0
    shift_end = 0
    index_start = 0
    index_end = 0

    tmp_line: str = line_text

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

    encoded_second = None
    if tmp_line.startswith(config.get_script_config().annotation_prefix):
        if config.get_script_config().annotation_suffix != '' and tmp_line.endswith(config.get_script_config().annotation_suffix):  # Detect multiple annotations
            first_index_suffix = tmp_line.index(config.get_script_config().annotation_suffix)
            second_index_suffix = tmp_line.rindex(config.get_script_config().annotation_suffix)

            if second_index_suffix != -1 and first_index_suffix != second_index_suffix:
                encoded_line = encode_annotation(tmp_line[:first_index_suffix])
                index_start += tmp_line.index(config.get_script_config().annotation_prefix)
                index_end += tmp_line.index(config.get_script_config().annotation_suffix) + 1

                encoded_line_second = encode_annotation(tmp_line[first_index_suffix + 1:-1])
                encoded_second = {
                    'line_number': line_number,
                    'line': encoded_line_second,
                    'shiftStart': shift_start,
                    'shiftEnd': shift_end,
                    'indexStart': index_start + tmp_line.rindex(config.get_script_config().annotation_prefix) + 1,
                    'indexEnd': index_end + tmp_line.rindex(config.get_script_config().annotation_suffix) + 1
                }
                pass
            else:
                encoded_line = encode_annotation(tmp_line[:-1])
                pass
            pass
        else:
            encoded_line = encode_annotation(tmp_line)
            pass
        pass
    else:
        encoded_line = {
            'type': 'text',
            'value': tmp_line
        }
        pass

    dumped.append(
        {
            'line_number': line_number,
            'line': encoded_line,
            'shiftStart': shift_start,
            'shiftEnd': shift_end,
            'indexStart': index_start,
            'indexEnd': index_end
        }
    )

    if encoded_second is not None:
        dumped.append(encoded_second)
        pass

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

                multiple_case_0 = ',' in param_value
                multiple_case_1 = param_name == 'voice' and '/' in param_value

                if multiple_case_0:
                    param_value = param_value.split(',')
                    pass
                elif multiple_case_1:
                    param_value = param_value.split('/')
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
