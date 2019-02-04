#!/usr/bin/python3

import argparse
import glob
import os

from src import constants
from src import decode


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

    if mode == constants.MODE_DECODE:
        for ks_file in files:
            decoded = decode.decode(ks_file)

            write_file(output_dir, ks_file, mode, decoded)
            continue
        return
    elif mode == constants.MODE_ENCODE:
        # TODO
        print()
        return
    return


def find_files(mode, _dir):
    if mode == constants.MODE_DECODE:
        ks_files = []
        for root_dir, subdirs, files in os.walk(_dir):
            if len(files) < 1:  # Skip dirs with no files
                continue
            for ks in glob.iglob(root_dir + '\\' + '*.ks'):
                ks_files.append(ks)
        return ks_files
    elif mode == constants.MODE_ENCODE:
        json_files = []
        for root_dir, subdirs, files in os.walk(_dir):
            if len(files) < 1:  # Skip dirs with no files
                continue
            for ks_json in glob.iglob(root_dir + '\\' + '*.ks.json'):
                json_files.append(ks_json)
        return json_files


def write_file(output_dir, file_to_write, mode, decoded):
    out_file_name = file_to_write
    if file_to_write.index('\\') is not -1:
        out_file_name = file_to_write[file_to_write.index('\\') + 1:]
        pass

    if mode == constants.MODE_DECODE:
        out_file_name += '.json'
        pass

    out_file = open(output_dir + '\\' + out_file_name, 'w+t', encoding='utf-8')

    if mode == constants.MODE_DECODE:
        out_file.write(decoded)
    elif mode == constants.MODE_ENCODE:
        # TODO
        pass
    out_file.close()

    print('Wrote {0} file \"{1}\"'.format(mode.lower(), out_file_name))

    return


if __name__ is '__main__':
    __main__()
