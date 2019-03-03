#!/usr/bin/python3

import argparse
import glob
import os
import configparser

if not __debug__:
    from src import constants
    from src import decode
    from src import encode
else:
    import constants
    import decode
    import encode


def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='input_dir', required=True, nargs=1, type=str, help='Input dir')
    parser.add_argument('--output', dest='output_dir', required=True, nargs=1, type=str, help='Output dir')
    parser.add_argument('--mode', dest='mode', required=True, choices=[constants.MODE_ENCODE, constants.MODE_DECODE])
    args = parser.parse_args()

    input_dir = args.input_dir[0]
    output_dir = args.output_dir[0]
    mode = args.mode.upper()

    files = find_files(mode, input_dir)

    print('Found {} files'.format(len(files)))

    if mode == constants.MODE_DECODE:
        for ks_file in files:
            decoded = decode.decode(ks_file)

            write_file(output_dir, ks_file, mode, decoded)
            continue
        return
    elif mode == constants.MODE_ENCODE:
        for ks_json_file in files:
            encoded = encode.encode(ks_json_file)

            write_file(output_dir, ks_json_file, mode, encoded)
            continue
        return
    return


def find_files(mode, _dir):
    if mode == constants.MODE_DECODE:
        ks_files = []
        for root_dir, subdirs, files in os.walk(_dir):
            if len(files) < 1:  # Skip dirs with no files
                continue
            for ks in glob.iglob(root_dir + constants.SEPARATOR + '*.ks'):
                ks_files.append(ks)
                continue
        return ks_files
    elif mode == constants.MODE_ENCODE:
        json_files = []
        for root_dir, subdirs, files in os.walk(_dir):
            if len(files) < 1:  # Skip dirs with no files
                continue
            for ks_json in glob.iglob(root_dir + constants.SEPARATOR + '*.ks.json'):
                json_files.append(ks_json)
                continue
        return json_files


def write_file(output_dir, file_to_write, mode, data):
    out_file_name = file_to_write
    index = file_to_write.rindex(constants.SEPARATOR)
    if index is not -1:
        out_file_name = file_to_write[index + 1:]
        pass

    if mode == constants.MODE_DECODE:
        out_file_name += '.json'
        pass
    elif mode == constants.MODE_ENCODE:
        out_file_name = data['file_name']
        pass

    out_file_path = output_dir + constants.SEPARATOR + out_file_name
    wtf_dir = out_file_path[:out_file_path.rindex(constants.SEPARATOR)]

    try:
        os.makedirs(wtf_dir)
        pass
    except FileExistsError:
        pass

    if mode == constants.MODE_DECODE:
        out_file = open(out_file_path, 'w+t', encoding='utf8')
        pass
    elif mode == constants.MODE_ENCODE:
        out_file = open(out_file_path, 'w+t', encoding='shift-jis')
        pass
    else:
        print('Unknown mode selected?!')
        breakpoint()
        return None

    if mode == constants.MODE_DECODE:
        out_file.write(data)
        pass
    elif mode == constants.MODE_ENCODE:
        if data is not None:
            out_file.writelines(data['decoded_lines'])
            pass
        pass
    out_file.close()

    print('Wrote {0} file \"{1}\"\n'.format(mode.lower(), out_file_name))
    return


if __name__ == '__main__':
    __main__()
