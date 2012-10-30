.. Ubik documentation master file, created by
   sphinx-quickstart on Tue Oct 30 13:22:50 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ubik: Package Manager for Unix
==============================

Release v\ |version|. (:ref:`Installation <install>`)

Ubik is AGPL3_ Licensed, written in Python and is safe when used as directed.

What's Ubik ?
-------------

Ubik is lightweight, elegant, no-external web service linked and easy to use package manager.
Inspired by the elegant Homebrew_ for OSX.

But Ubik is flexible, so you can easily provide binaries instead of source. Because compile every software or new updates is just painful.

This package manager have a very easy to use toolbelt for repository management and package creation.

User Guide
----------

.. toctree::
   :maxdepth: 2

   user/install

Toolbelt Guide
--------------

.. toctree::
   :maxdepth: 2

   toolbelt/repository
   toolbelt/packager


API Documentation
-----------------

If you are looking for information on a specific function, class or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api

Feature Support
---------------

Ubik can be use on every Unix.

- Install, Remove, Upgrade, Reinstall actions
- Dependecies resolver for Installation
- Package cache managment
- Package integrity check via Md5
- Web UI for package managment
- Package control file are Python objects
- Ubik is full Python

.. _Homebrew: http://mxcl.github.com/homebrew/
.. _AGPL3: http://www.gnu.org/licenses/agpl.html