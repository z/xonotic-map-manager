import configparser
import os
import sys
import time
import hashlib
from shutil import copyfile


def file_is_empty(path):
    return os.stat(path).st_size == 0


def convert_size(num):
    for x in ['B', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            string = "%3.1d%s" % (num, x)
            return string.strip()
        num /= 1024.0
    string = "%3.1f%s" % (num, 'TB')
    return string.strip()


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


def replace_last(s, old, new):
    return s[::-1].replace(old[::-1], new[::-1], 1)[::-1]


def hash_file(filename):
    """This function returns the SHA-1 hash
    of the file passed into it"""

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filename, 'rb') as file:

        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


# http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
