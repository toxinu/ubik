.. _packager:

Package maker
=============

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