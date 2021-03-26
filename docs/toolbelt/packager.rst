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

I heavily advise you to every time set ``--prefix`` option at ``/usr/local/ubik`` for your ``./configure`` process in order
to provide clean package.
If you give package with custom prefix, links will be broken on user system.
You can find examples belove.

The ``build`` operation will run ``build`` method in ``control.py``.
It's recommended that this method must just work in ``source`` directory.

After that, the ``package`` method must do the ``installation``, ``source`` to ``build``.
It's important to understand that ubik will recursivly copy every files in ``build`` to Ubik packages root.

::

    ubik-package build
    ubik-package package
    ubik-package archive

And you have your ``my_package.tar``.

Ubik install process
====================

This is the Ubik install process in chronologic order:

* Download archive package
* Extract it
* Run ``pre_install`` method
* Extract ``files.bz2`` archive which is your ``build`` directory to Ubik packages root
* Run ``post_install`` method

Examples
========

This is an example repository_ with different packages and their sources.

.. _repository: https://github.com/toxinu/ubik

You can find more packages examples here:

* pyhn_ (Hacker news python client)
* python3_
* flask_ (Python web framework)
* urwid_ (Python lib)
* wget_
* htop_

.. _pyhn: 
.. _python3:
.. _flask:
.. _urwid:
.. _wget:
.. _htop:

FAQ
===

* How do I package python egg ?

Let's see an example_ together, ``pyhn``.

.. _example: https://github.com/toxinu/ubik/tree/master/public/noarch/nodist/novers/pyhn.source

It's more easy to leave ``setuptools`` do it's job, so just put your ``.tar.gz`` in ``sources``,
Set your ``build`` method to copy it in your ``/tmp/ubik/pyhn-0.1.8.tar.gz``.

And the installation will be done by ``post_install`` method, take a loot at source_.

.. _source: https://github.com/toxinu/ubik/blob/master/public/noarch/nodist/novers/pyhn.source/control.py
