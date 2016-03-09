import configparser
import os
import sys
import time
from shutil import copyfile

def file_is_empty(path):
    return os.stat(path).st_size == 0


def convert_size(num):
    for x in ['B', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1d%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


def reporthook(count, block_size, total_size):

    global start_time

    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed. " %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


def parse_config(config_file):

    if not os.path.isfile(config_file):
        print(bcolors.WARNING + config_file + ' not found, please create one.' + bcolors.ENDC)
        raise SystemExit

    conf = configparser.ConfigParser()
    conf.read(config_file)

    return conf['default']


def check_if_not_create(file, template):
    if not os.path.isfile(file):
        os.makedirs(os.path.dirname(file), exist_ok=True)
        copyfile(template, file)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'