Configuration
=============

The defaults should work out of the box, if you want to make changes, edit the ``~/.xmm.cfg`` file.

.. code-block:: ini

    # This file is read from ~/.xmm.cfg, make sure that's where you are editing it
    [default]

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
