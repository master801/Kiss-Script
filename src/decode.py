#!/usr/bin/python3

if not __debug__:
    from src import json_encode
    from src import constants
else:
    import json_encode
    import constants


def decode(input_file):
    print('Decoding input file {0}...'.format(input_file))

    read_input_data = read(input_file)

    input_file_name = input_file
    index = input_file_name.rindex(constants.SEPARATOR)
    if index is not -1:
        input_file_name = input_file_name[index + 1:]
        pass

    read_lines = read_input_data

    return json_encode.encode_to_json(input_file_name, read_lines)


def read(input_file):
    read_lines = []
    with open(input_file, 'r+t', encoding='shift-jis', newline='\r\n') as opened_file:
        line_number = 0
        for line in opened_file:
            line_number += 1

            trimmed_line = line

            if len(line) >= 2:
                end = line[len(line) - 2:]
                if end == '\r\n':
                    trimmed_line = line[0:len(line) - 2]
                    pass
                pass

            if line == '\r\n' and trimmed_line == '':
                print('Skipped EOF')
                continue
            elif trimmed_line == '' or trimmed_line[0] == ';':
                print('Skipped line:\r\n{0}'.format(trimmed_line))
                continue
            read_lines.append([line_number, trimmed_line])
            print('Appended line: {0}'.format(trimmed_line))
            continue
        opened_file.close()
        pass
    return read_lines
