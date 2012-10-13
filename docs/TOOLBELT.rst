Ubik Toolbelt
=============

Description
-----------

Ubik toolbelt is a set of tools for `Ubik`_ management.  
It's built-in ``Ubik``.

Features
--------

- Easy to use
- Control file for package are Python objects
- Post/Pre Install/Remove/Upgrade controls
- Python

Create package
--------------

You can see how to create ``wget`` package in ``docs/examples`` dir.

::

    cd /usr/local/src
    ubik-package create my_package
    cd my_package
    mkdir -p source/usr/bin
    vim source/usr/bin/hello.sh
    # Edit your control.py
    vim control.py
    ubik-package build
    ubik-package package
    ubik-package archive

And you have your ``my_package.tar``.

Create repositorie
------------------

This is a repositorie structure:

::

    my_repo
    ├── .repo_root
    └── stable
        ├── Packages.json
        ├── noarch
        │   └── nodist
        │       └── novers
        │           ├── hello_hell.tar
        │           ├── hello_world.tar
        │           └── test_deps.tar
        └── x86_64
            └── debian
                └── 6
                    ├── hello_hell2.tar
                    ├── hello_world2.tar
                    └── test_deps2.tar

And this how to create your own repositorie:

::

    ubik-repo create my_repo
     :: Create repositorie structure
     :: Create default "stable" branch and two examples

And you have just to put your packages into the good Branch/Arch/Dist/Vers and run ``ubik-repo generate`` in your repositorie root.

Thanks
------

Thanks to `Docopt`_ to be awesome tool.

License
-------

License is `AGPL3`_.
See `LICENSE`_.

.. _Ubik: https://github.com/socketubs/Ubik
.. _LICENSE: https://raw.github.com/Socketubs/ubik/master/LICENSE
.. _AGPL3: http://www.gnu.org/licenses/agpl.html
.. _Docopt: https://github.com/docopt/docopt
