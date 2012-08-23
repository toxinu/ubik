Ubik
====

Description
-----------

Ubik is a minimal package manager inspired by the ``pkgmgr`` of [Canopsis][1] but rewritten in Python (from bash).

Not as sexy as [Homebrew][8] for ``OsX`` but available for every ``Unix`` environment.

![Ubik screenshot01](http://dl.dropbox.com/u/79447684/Github/Ubik/screenshot_01.png "Ubik Screenshot01")
![Ubik screenshot02](http://dl.dropbox.com/u/79447684/Github/Ubik/screenshot_02.png "Ubik Screenshot02")

Features
--------

 * Install/Remove/Upgrade/Reinstall
 * Deps resolver for installation
 * Cache
 * Md5 checker
 * Control file for package
 * Post/Pre Install/Remove/Upgrade controls
 * Python

Installation
------------

```
pip install git+http://github.com/Socketubs/Ubik.git
```

What about packages and repositories management ?
-------------------------------------------------

Take a look at [Ubik toolbelt][2].

Thanks
------

Thanks to [Requests][5], [Docopt][6] and [ProgressBar][7] to be awesome tools.

For information:
```
Canopsis is a hypervisor, built on top of all open source monitoring solutions
to agregate, correlate and ponderate events flowing from them.
```

License
-------

License is [AGPL3][4], it fully compatible with ``Canopsis``.
See [LICENSE][3].

[1]: https://github.com/capensis/canopsis
[2]: https://github.com/Socketubs/Ubik-toolbelt
[3]: https://raw.github.com/Socketubs/ubik/master/LICENSE
[4]: http://www.gnu.org/licenses/agpl.html
[5]: https://github.com/kennethreitz/requests
[6]: https://github.com/docopt/docopt
[7]: http://code.google.com/p/python-progressbar/
[8]: http://mxcl.github.com/homebrew/
