import configparser
import os
import sys
import json
import time
import hashlib
import subprocess
import urllib.request
from datetime import datetime
from shutil import copyfile


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


def download_file(filename_with_path, url, use_curl=False):
    """
    downloads a file from any URL

    :param filename_with_path:
        filename with path to download file to
    :type filename_with_path: ``str``

    :param url:
        URL to download map from
    :type url: ``str``

    :param use_curl:
        Whether or not to use curl to download the file, default ``False``
    :type use_curl: ``bool``
    """
    if not os.path.exists(filename_with_path):

        if not use_curl:
            urllib.request.urlretrieve(url, os.path.expanduser(filename_with_path), reporthook)
        else:
            subprocess.call(['curl', '-o', filename_with_path, url])

        print(bcolors.OKBLUE + 'Done.' + bcolors.ENDC)

    else:
        print(bcolors.FAIL + 'file already exists, please remove first.' + bcolors.ENDC)
        return False


def parse_config(config_file):

    if not os.path.isfile(config_file):
        print(bcolors.WARNING + config_file + ' not found, please create one.' + bcolors.ENDC)
        raise SystemExit

    conf = configparser.ConfigParser()
    conf.read(config_file)

    return conf['default']


def check_if_not_create(file, template):
    """
    Checks for a file, if it doesn't exist, it will be created from a template.

    :param file:
        filename with path to file
    :type file: ``str``

    :param template:
        filename with path to template file
    :type template: ``str``
    """
    if not os.path.isfile(file):
        os.makedirs(os.path.dirname(file), exist_ok=True)
        copyfile(template, file)


def create_if_not_exists(file, contents):
    """
    Checks for a file, if it doesn't exist, it will be created from a template.

    :param file:
        filename with path to file
    :type file: ``str``

    :param contents:
        string contents of the file being created
    :type contents: ``str``
    """
    if not os.path.isfile(file):
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, 'w') as f:
            f.write(contents)


def file_is_empty(filename):
    """
    Checks to see if a file is empty

    :param filename:
        string filename
    :type filename: ``str``

    :returns: ``bool``
    """
    return os.stat(filename).st_size == 0


def replace_last(s, old, new):
    return s[::-1].replace(old[::-1], new[::-1], 1)[::-1]


def hash_file(filename):
    """
    This function returns the SHA-1 hash
    of the file passed into it
    """

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
    """
    Ask a yes/no question via raw_input() and return their answer.

    :param question:
        a string that is presented to the user.
    :type question: ``str``

    :param default:
        is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
    :type default: ``str``

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


# http://stackoverflow.com/a/24030569
class ObjectEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that leverages an object's `__json__()` method,
    if available, to obtain its default JSON representation.
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if hasattr(obj, '__json__'):
            return obj.__json__()

        return json.JSONEncoder.default(self, obj)
