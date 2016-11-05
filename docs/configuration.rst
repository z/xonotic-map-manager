Configuration
=============

The defaults should work out of the box, if you want to make changes, edit the ``~/.xmm.cfg`` file.

.. code-block:: ini

    # This file is read from ~/.xmm.cfg, make sure that's where you are editing it
    [default]

    # Where should xmm manage maps?
    map_dir = ~/.xonotic/data/

    # You don't need to change these unless you're running your own repo
    repo_url = http://dl.xonotic.co/
    api_data = ~/.xmm/maps.json
    api_data_url = http://xonotic.co/resources/data/maps.json

    # This is only preference
    use_curl = False

    # local tracking of installed packages
    package_store = ~/.xmm/packages.db

    # (optional) configuration of servers to use with multiple servers
    servers = ~/.xmm/servers.json


**xmm** can facilitate the management of multiple servers with a ``~/.xmm/servers.json`` file to configure their settings, example below:

.. code-block:: json

    {
      "myserver1": {
        "target_dir": "~/.xonotic/data/myserver1/",
        "package_db": "~/.xmm/packages-myserver1.db"
      },
      "myserver2": {
        "target_dir": "~/.xonotic/data/myserver2/",
        "package_db": "~/.xmm/packages-myserver2.db"
      }
    }

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
