#!/usr/bin/python3

if not __debug__:
    from src import constants
    from src import json_encode
    from src import config
    from src.log import Log
else:
    import constants
    import json_encode
    import config
    from log import Log


def decode(input_file):
    Log.log_to_file(True, 'Decoding input file \"{0}\"...'.format(input_file))

    read_input_data = read(input_file)

    input_file_name = input_file
    index = input_file_name.rindex(constants.SEPARATOR)
    if index is not -1:
        input_file_name = input_file_name[index + 1:]
        pass

    read_lines = read_input_data

    if read_lines is None:
        return None

    return json_encode.encode_to_json(input_file_name, read_lines)


def read(input_file: str):
    read_lines: list = []
    try:
        with open(input_file, 'r+t', encoding='shift-jis', newline='\r\n') as opened_file:
            line_number: int = 0
            for line in opened_file:
                line_number += 1

                trimmed_line: str = line

                if len(line) >= 2:
                    end = line[len(line) - 2:]
                    if end == '\r\n':
                        trimmed_line = line[0:len(line) - 2]
                        pass
                    pass

                if line == '\r\n' and trimmed_line == '':  # EOL
                    Log.log_to_file(True, 'Skipped EOL')
                    continue
                elif trimmed_line == '':  # Blank
                    Log.log_to_file(True, 'Skipped line ({0}):\r\n{1}'.format(line_number, trimmed_line))
                    continue
                elif len(config.get_script_config().comment) <= len(trimmed_line) and trimmed_line[:len(config.get_script_config().comment)] == config.get_script_config().comment:  # Comment
                    Log.log_to_file(True, 'Skipped comment line ({0}):\r\n{1}'.format(line_number, trimmed_line))
                    continue

                # Check to ignore certain lines
                if len(config.get_script_config().ignore) > 0:
                    should_ignore = False
                    for i in range(0, len(config.get_script_config().ignore)):
                        ignore = config.get_script_config().ignore[i]
                        if len(ignore) <= len(trimmed_line):  # Add len check in case of len issues
                            if trimmed_line[:len(ignore)] == ignore:
                                should_ignore = True
                                break
                            pass
                        continue
                    if should_ignore:
                        Log.log_to_file(True, 'Ignored line ({0}):\r\n{1}'.format(line_number, trimmed_line))
                        continue
                    pass

                read_lines.append([line_number, trimmed_line])
                Log.log_to_file(True, 'Appended line ({0}): {1}'.format(line_number, trimmed_line))
                continue
            opened_file.close()
            pass
    except UnicodeDecodeError:
        Log.log_to_file(True, 'Failed to decode input file {0}!'.format(input_file))
        return None
    return read_lines
