.. _api:

API
===

This page cover all the Ubik API with many examples.

Database
--------

Database object can be synchronized with remote repository.
Synchronization retrieve remote ``Packages.json`` file and merge it with local database.

::

    >>> import ubik.core as api
    >>> db = api.db
    >>> db.sync()
    >>> db.packages
    {u'mongodb': <ubik.package.Package object at 0x100965650>,
     u'nginx'  : <ubik.package.Package object at 0x100965c10>,
     u'python3': <ubik.package.Package object at 0x100976f10>,
     u'python2': <ubik.package.Package object at 0x100977c10>}
    >>> db.sync()

Package
-------

Objects:

- ``ubik.database.Database``
- ``ubik.package.Package``

There are many ways to get a ``Package`` object from ``Database`` with the ``get`` method. You can give to it ``string``, ``list`` or regexp.
This method will always return to you a ``list`` object.

::

    >>> db.get(['mongodb', 'nginx'])
    >>> db.get('python*')
    >>> db.get('python2', regexp = False)

After that, you will able to play with ``Package`` object.

::

    >>> package = db.get('python*')[0]
    >>> package.md5
    u'd41eaca692c35abd4d6bd68e914eef16'
    >>> package.requires
    [u'example_deps']

Installer
---------

The ``ubik.installer.Installer`` object do the complex install process for you. At this step, we consider you have your ``Database`` and all your ``Packages`` objects you want.

Steps:

- Give ``Packages`` to ``Installer`` to resolve dependencies
- Feed the ``Installer`` with all the ``Installer.resolved`` packages
- Take a look at which packages ``Installer`` want to install
- Download packages with ``Installer.download()`` method
- Install packages with ``Installer.install()`` method

::

    >>> from ubik.installer import Installer
    >>> db.sync()
    >>> installer = Installer()
    >>> installer.resolv(package)
    >>> installer.feed(installer.resolved)
    >>> installer.packages
    [<ubik.package.Package object at 0x1009bd950>,
     <ubik.package.Package object at 0x1009bdb10>]
    >>> installer.download()
    >>> installer.install()
    >>> db.get_installed()
    [<ubik.package.Package object at 0x1009bdb10>,
     <ubik.package.Package object at 0x1009bd950>]

More
----

For more information before full doc redaction you can take a look at
``ubik.cli.Cli`` object, it’s just an ``API`` client.

Configuration
-------------

Ubik conf is a simple ``ConfigParser`` object. More docs `here`_.

.. _here: http://docs.python.org/library/configparser.html