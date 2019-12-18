#!/usr/bin/python3

import os.path


class Log:
    actual_log_path: str  # Config file path
    open_log_file = None  # Stream

    should_not_log: bool = True  # If should log (write to file)
    silent: bool = False  # If should not log (print to console)

    @staticmethod
    def find_next_log_file_path():
        if Log.should_not_log:
            return

        log_index = 0
        log_path = 'log_index_{0}.log'.format(log_index)
        while os.path.exists(log_path):
            log_index = log_index + 1
            log_path = 'log_index_{0}.log'.format(log_index)
            pass
        Log.actual_log_path = log_path
        return

    @staticmethod
    def log_to_file(should_print: bool, msg: str):
        if should_print and not Log.silent:
            print(msg)
            pass

        if Log.should_not_log:
            return

        if Log.open_log_file is None:
            Log.open_log_file = open(Log.actual_log_path, mode='x', encoding='utf8')
            pass
        Log.open_log_file.write(msg + '\n')
        return

    @staticmethod
    def close_log_file():
        if not Log.should_not_log:
            return
        if Log.open_log_file is not None:
            Log.open_log_file.close()
            pass
        return
