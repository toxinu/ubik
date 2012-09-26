Ubik
====

Description
-----------

Ubik is a minimal package manager inspired by the ``pkgmgr`` of
`Canopsis`_ but rewritten in Python (from bash).

.. image:: http://dl.dropbox.com/u/79447684/Github/Ubik/screenshot_01.png
.. image:: http://dl.dropbox.com/u/79447684/Github/Ubik/screenshot_02.png

Features
--------

-  Install/Remove/Upgrade/Reinstall
-  Deps resolver for installation
-  Cache
-  Md5 checker
-  Control file for package
-  Post/Pre Install/Remove/Upgrade controls
-  Python

Installation
------------

::

    pip install ubik

What about packages and repositories management ?
-------------------------------------------------

Take a look at `Ubik toolbelt`_.

Tests
-----

You can run tests with ``tests/run_tests.sh`` script.

Thanks
------

Thanks to `Requests`_, `Docopt`_ and `ProgressBar`_ to be awesome tools.

For information:

``Canopsis is a hypervisor, built on top of all open source monitoring solutions to agregate, correlate and ponderate events flowing from them.``

License
-------

License is `AGPL3`_, it fully compatible with ``Canopsis``. See
`LICENSE`_.

.. _Canopsis: https://github.com/capensis/canopsis
.. _Ubik toolbelt: https://github.com/Socketubs/Ubik-toolbelt
.. _Requests: https://github.com/kennethreitz/requests
.. _Docopt: https://github.com/docopt/docopt
.. _ProgressBar: http://code.google.com/p/python-progressbar/
.. _AGPL3: http://www.gnu.org/licenses/agpl.html
.. _LICENSE: https://raw.github.com/Socketubs/ubik/master/LICENSE
