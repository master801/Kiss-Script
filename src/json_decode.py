#!/usr/bin/python3

if not __debug__:
    from src import constants
else:
    import constants


def decode_from_json(json_file):
    if json_file is None:
        return None

    if 'name' in json_file:
        print('Found deprecated key \"{}\"'.format('name'))
        file_name = json_file['name']
        pass
    else:
        file_name = json_file['file_name']
        pass

    lines = json_file['lines']

    decoded_lines = []
    for line in lines:
        line_number = line['line_number']

        while len(decoded_lines) + 1 < line_number:
            decoded_lines.append(constants.END_LINE)
            continue

        line_data = line['line']
        shift_start = line['shiftStart']
        shift_end = line['shiftEnd']

        line_type = line_data['type']

        if line_type == 'annotation':
            params = line_data['params']

            current_line = '@' + line_data['name']

            param_args = []
            for param in params:
                if isinstance(param, dict):
                    param_name = param['name']
                    param_value = param['value']

                    if isinstance(param_value, list):
                        concat = ''
                        for i in param_value:
                            concat += (i + ',')
                            continue
                        concat = concat[:-1]

                        param_value = concat
                        pass
                    elif isinstance(param_value, str):
                        # NOOP
                        pass
                    else:
                        print('Unexpected param!!')
                        breakpoint()
                        pass

                    param_args.append(param_name + '=' + param_value)
                    pass
                elif isinstance(param, str):
                    param_args.append(param)
                    pass
                else:
                    print('Unexpected param!!')
                    breakpoint()
                    pass
                continue

            for param_arg in param_args:
                current_line += (' ' + param_arg)
                continue
        elif line_type == 'text':
            current_line = line_data['value']
            pass
        else:
            print('Unexpected type found!')
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

        decoded_lines.append(current_line)
        continue

    return {
        'file_name': file_name,
        'decoded_lines': decoded_lines
    }
