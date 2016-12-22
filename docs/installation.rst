Installation
============

Requirements
------------

* Python 3

Debian/Ubuntu
^^^^^^^^^^^^^

If you do not already have **pip** and **setuptools** for Python3::

    sudo apt install python3-pip python3-setuptools


Install
-------

Install using pip::

    pip3 install xmm --user

If you get an error trying to run ``xmm``, you probably need ``$HOME/.local/bin`` in your path, put the following in your ``~/.bashrc`` or ``~/.zshrc`` etc::

    export PATH=$PATH:$HOME/.local/bin

Alternatively, install the development version manually with setuptools::

   git clone https://github.com:z/xonotic-map-manager.git
   cd xonotic-map-manager
   python3 setup.py install


* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`