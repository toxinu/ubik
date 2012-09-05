Api
===

Some examples of Ubik api, still work in progress.

Database
--------

::

    >>> import ubik.core as api
    >>> db = api.db
    >>> db.packages
    {u'hello_hell': <ubik.package.Package object at 0x100965650>, u'test_deps': <ubik.package.Package object at 0x100965c10>, u'hello_world': <ubik.package.Package object at 0x100976f10>}
    >>> db.sync()

Package
-------

There are many ways to get a package from database.

::

    >>> db.get(['test_deps', 'hello_world'])
    >>> db['test_deps']
    >>> db.get('hello*')
    >>> db.get('hello', regexp = False)

::

    >>> package = db.get('test_deps')[0]
    >>> package.md5
    u'd41eaca692c35abd4d6bd68e914eef16'
    >>> package.requires
    [u'hello_world']

Installer
---------

::

    >>> from ubik.installer import Installer
    >>> db.sync()
    >>> installer = Installer()
    >>> installer.resolv(package)
    >>> installer.feed(installer.resolved)
    >>> installer.packages
    [<ubik.package.Package object at 0x1009bd950>, <ubik.package.Package object at 0x1009bdb10>]
    >>> installer.download()
    >>> installer.install()
    >>> db.get_installed()
    [<ubik.package.Package object at 0x1009bdb10>, <ubik.package.Package object at 0x1009bd950>]

More
----

For more information before full doc redaction you can take a look at
``Cli`` object, it’s just an ``api`` client.

Configuration
-------------

Ubik conf is a simple ``ConfigParser`` object. More docs `here`_.

.. _here: http://docs.python.org/library/configparser.html