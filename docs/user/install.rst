.. _install:

Installation
============

This part of the documentation explains you how to install Ubik.


Distribute & Pip
----------------

Installing ubik is simple with `pip <http://www.pip-installer.org/>`_::

    $ pip install ubik

or, with `easy_install <http://pypi.python.org/pypi/setuptools>`_::

    $ easy_install ubik

But, you really `shouldn't do that <http://www.pip-installer.org/en/latest/other-tools.html#pip-compared-to-easy-install>`_.


Cheeseshop Mirror
-----------------

If the Cheeseshop is down, you can also install Ubik from one of the
mirrors. `Crate.io <http://crate.io>`_ is one of them::

    $ pip install -i http://simple.crate.io/ ubik


From the Source
---------------

Ubik is developed on GitHub, where the code is
`always available <https://github.com/toxinu/ubik>`_.

You can either clone the public repository::

    git clone git://github.com/toxinu/ubik.git

Download the `tarball <https://github.com/toxinu/ubik/tarball/master>`_::

    $ curl -OL https://github.com/toxinu/ubik/tarball/master

Or, download the `zipball <https://github.com/toxinu/ubik/zipball/master>`_::

    $ curl -OL https://github.com/toxinu/ubik/zipball/master


Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily::

    $ python setup.py install
