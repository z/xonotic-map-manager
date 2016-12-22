.. _configuration:

Configuration
=============

Core
----

The defaults should work out of the box, if you want to make changes, edit the ``~/.xmm.ini`` file.

.. code-block:: ini

    # This file is read from ~/.xmm.ini, make sure that's where you are editing it
    [xmm]

    # Where should xmm manage maps?
    target_dir = ~/.xonotic/data/

    # Default repo if no sources specified
    download_url = http://dl.xonotic.co/
    api_data_url = http://xonotic.co/resources/data/maps.json
    api_data_file = ~/.xmm/maps.json

    # This is only preference
    use_curl = False

    # configuration of servers to use with multiple servers
    servers_config = ~/.xmm/servers.json

    # configuration of repositories
    sources_config = ~/.xmm/sources.json

Logging
-------

Logging can be configured in ``~/.xmm/xmm.logging.ini``, again, the defaults should be sufficient.

.. code-block:: ini

    # ~/.xmm/xmm.logging.ini
    [loggers]
    keys = root

    [logger_root]
    level    = NOTSET
    handlers = stream, info

    [handlers]
    keys = stream, info

    [handler_stream]
    class = StreamHandler
    args = (sys.stdout,)
    level = ERROR
    formatter = generic

    [handler_debug]
    class = handlers.RotatingFileHandler
    formatter = generic
    level = DEBUG
    args = ('%(log_filename)s', 'a', 50000000, 5)

    [handler_info]
    class = handlers.RotatingFileHandler
    formatter = generic
    level = INFO
    args = ('%(log_filename)s', 'a', 50000000, 5)

    [formatters]
    keys = generic

    [formatter_generic]
    format = %(asctime)s %(levelname)-5.5s [%(name)s] [%(threadName)s] %(message)s
    datefmt = %Y-%m-%d %H:%M:%S
    class = logging.Formatter

.. _multi-server:

Multi-Server
------------

**xmm** can facilitate the management of multiple servers with ``~/.xmm/servers.json`` which defines the configure of settings, example below:

.. code-block:: json

    {
      "myserver1": {
        "target_dir": "~/.xonotic/myserver1/data/",
        "library": "~/.xmm/myserver1/library.json",
        "sources": "~/.xmm/sources.json"
      },
      "myserver2": {
        "target_dir": "~/.xonotic/myserver2/data/",
        "library": "~/.xmm/myserver2/library.json",
        "sources": "~/.xmm/myserver2/sources.json"
      }
    }

.. _multi-repository:

Multi-repo
----------

**xmm** can use multiple repositories, edit the ``~/.xmm/sources.json`` file to configure them, example below:

.. code-block:: json

    {
      "default": {
        "download_url": "http://dl.xonotic.co/",
        "api_data_file": "~/.xmm/maps.json",
        "api_data_url": "http://xonotic.co/resources/data/maps.json"
      }
    }

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
