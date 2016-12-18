import logging


class ClassPrefixAdapter(logging.LoggerAdapter):
    def __init__(self, prefix, logger, extra=None):
        super(ClassPrefixAdapter, self).__init__(logger, extra or {})
        self.prefix = prefix
    """
    Custom Adapter to insert class name to provide context
    """
    def process(self, msg, kwargs):
        return '[%s] %s' % (self.prefix, msg), kwargs
