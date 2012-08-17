API
===

Some examples of Ubik api, still work in progress.

Database
--------

```
>>> import ubik
>>> db = ubik.core.db
>>> db.packages
{'hello_world': <ubik.package.Package object at 0x9688e6c>}
>>> db.sync()
```

Package
-------

```
>>> package = db.packages['hello_world']
>>> package = db.get('hello_world')
>>> packages = db.get(['hello_world', 'another_package'])
>>> package.md5
'34025837699c48233ba94dba3722f523'
>>> package.name
'hello_world'
>>> package.deps
[]
>>> package.arch
'noarch'
...
```

Installer
---------

```
>>> from ubik.installer import Installer
>>> from ubik.installer import DepsResolver as InstallerResolver
>>> db.sync()
>>> installer = Installer()
>>> resolver = InstallerResolver(package)
>>> resolver.resolv()
>>> installer.feed(resolver.resolved)
>>> installer.packages
[<ubik.package.Package object at 0x9688e6c>]
>>> installer.download()
>>> installer.install()
```

Configuration
-------------

Ubik conf is a simple ``ConfigParser`` object. More docs [here][1].

[1]: http://docs.python.org/library/configparser.html
