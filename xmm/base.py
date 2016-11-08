from xmm.logger import logger
from xmm.config import conf


class Base(object):

    def __init__(self):
        self.conf = conf
        self.logger = logger
