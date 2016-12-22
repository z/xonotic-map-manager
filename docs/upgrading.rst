Upgrading
=========

0.7.0 -> 0.8.0
--------------

Configuration Updates
^^^^^^^^^^^^^^^^^^^^^

xmm.cfg -> xmm.ini
""""""""""""""""""

* Renamed section: ``[default]`` to ``[xmm]``

* Renamed keys:

    * ``map_dir`` -> ``target_dir``
    * ``repo_url`` -> ``download_url``
    * ``api_data`` -> ``api_data_file``
    * ``servers`` -> ``servers_config``

* New keys:

    * ``servers_config`` with default ``~/.xmm/servers.json``

servers.json
""""""""""""

The ``package_db`` key has been dropped, ``library`` and ``sources`` have been added.

Pickle is no longer used for serialization, data is now stored as JSON:

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


sources.json *[NEW]*
""""""""""""""""""""

This is a new feature that enables support for more than one repository:

.. code-block:: json

    {
      "default": {
        "download_url": "http://dl.xonotic.co/",
        "api_data_file": "~/.xmm/maps.json",
        "api_data_url": "http://xonotic.co/resources/data/maps.json"
      }
    }

For more information please see the :ref:`configuration` page.

xmm.logging.ini *[NEW]*
"""""""""""""""""""""""

Logging is now configurable through ``~/.xmm/xmm.logging.ini``.

For more information please see the :ref:`configuration` page.

Migrating Your Library
^^^^^^^^^^^^^^^^^^^^^^

The easiest way to migrate your library is with::

    xmm discover --add

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
