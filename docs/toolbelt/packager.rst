.. _packager:

Package maker
=============

You can see how to create ``wget`` package in ``docs/examples`` dir.

Go to your ``/usr/local/src`` and run ``ubik-package create my_package``.

::

    cd /usr/local/src
    ubik-package create my_package
    cd my_package

If you directly work in the repository I advise you to rename you package directory to ``my_package.source``.

Now you have to put your sources in ``source``:

::

    mkdir -p source/usr/bin
    vim source/usr/bin/hello.sh
    # Edit your control.py
    vim control.py

The ``build`` operation will run ``build`` method in ``control.py``.
It's recommended that this method must just work in ``source`` directory.

After that, the ``package`` method must do the ``installation``, ``source`` to ``build``.


::

    ubik-package build
    ubik-package package
    ubik-package archive

And you have your ``my_package.tar``.

Examples
========

This is an example repository_ with different packages and their sources.

.. _repository: https://github.com/socketubs/ubik-repo