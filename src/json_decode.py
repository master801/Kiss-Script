#!/usr/bin/python3

if not __debug__:
    from src import constants
    from src import config
    from src.log import Log
else:
    import constants
    import config
    from log import Log


def decode_from_json(json_file):
    if json_file is None:
        Log.log_to_file(True, 'No json file given?!')
        return None

    file_name = json_file['file_name']
    lines = json_file['lines']

    decoded_lines = []
    for i in range(len(lines)):
        line = lines[i]
        line_number = line['line_number']

        while len(decoded_lines) + 1 < line_number:
            decoded_lines.append(constants.END_LINE)
            continue

        line_data = line['line']
        shift_start = line['shiftStart']
        shift_end = line['shiftEnd']
        index_start = line['indexStart']
        index_end = line['indexEnd']

        line_type = line_data['type']

        if line_type == 'annotation':
            params = line_data['params']

            current_line = config.get_script_config().annotation_prefix  # Apply prefix
            current_line += line_data['name']  # Name

            # Params
            param_args = []
            for param in params:
                if isinstance(param, dict):
                    param_name = param['name']
                    param_value = param['value']

                    if isinstance(param_value, list):
                        concat = ''
                        for pv in param_value:
                            concat += (pv + ',')
                            continue
                        concat = concat[:-1]

                        param_value = concat
                        pass
                    elif isinstance(param_value, str):
                        # NOOP
                        pass
                    else:
                        Log.log_to_file(True, 'Unexpected param!!')
                        breakpoint()
                        pass

                    param_args.append(param_name + '=' + param_value)
                    pass
                elif isinstance(param, str):
                    param_args.append(param)
                    pass
                else:
                    Log.log_to_file(True, 'Unexpected param!!')
                    breakpoint()
                    pass
                continue

            for param_arg in param_args:
                current_line += (' ' + param_arg)
                continue

            # Apply suffix
            current_line += config.get_script_config().annotation_suffix
        elif line_type == 'text':
            current_line = line_data['value']
            pass
        else:
            Log.log_to_file(True, 'Unexpected type found!')
            return None

        if shift_start > 0:
            i = 0
            while i < shift_start:
                current_line = '\t' + current_line
                i += 1
                continue
            pass

        if shift_end > 0:
            i = 0
            while i < shift_end:
                current_line += '\t'
                i += 1
                continue
            pass

        current_line += constants.END_LINE

        if len(lines) > 1 and line_number == lines[i - 1]['line_number']:
            prev_line = decoded_lines[len(decoded_lines) - 1]  # Get prev line
            prev_line = prev_line[:-1]  # Remove EOL
            prev_line += current_line  # Add 2nd annotation
            decoded_lines[len(decoded_lines) - 1] = prev_line  # Set 2nd annotation
            continue
        else:
            decoded_lines.append(current_line)
            continue

    return {
        'file_name': file_name,
        'decoded_lines': decoded_lines
    }
