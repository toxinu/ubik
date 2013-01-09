.. _usage:

Usage
=====

This part of the documentation explains you how to use Ubik.
It will explain to you the basic usage of Ubik.

Before everything, you have to setup your configuration file.

Configuration
-------------

For example, you can save your personal configuration file in your home: ::

    $ echo_ubik_conf > ~/.ubik.conf

And set an environment variable which give to Ubik the path to this file: ::

    $ export UBIK_CONF="~/.ubik.conf"

Database
--------

Synchronize your local database with your remote repository, this is the first thing to do: ::

    $ ubik update
     :: Update
        | Get http://ubik-repo.herokuapp.com:80//public/Packages.json

And now list all packages::

    $ ubik list

     System : Osx 10.8.2 x86_64
     Repo   : http://ubik-repo.herokuapp.com:80//public
     Last Update : Thu Nov 22 16:00:45 2012

    Name                      Version                   Status              
    ------------------------- ------------------------- --------------------
    htop                      [0.8.2.1-4]               Not installed       
    spilleliste               [0.1.0-0]                 Not installed       
    wget                      [1.14-0]                  Not installed               


Operations
----------

Install a package: ::

    $ ubik install wget
     :: Update
        | Get http://ubik-repo.herokuapp.com:80//public/Packages.json
     :: Resolving dependencies
     :: Following dependencies will be installed:
        - wget
    Confirm [y|N]: y
     :: Download
        | wget already in cache
     :: Install
        - wget
          | Unarchive
          | Pre Install
          | Unpack
          | Post Install
          | Clean
          | Update database

I think you will easily find all other operations by yourself.

::

    Ubik is a minimal package manager for Unix.

    Usage:
      ubik (list|update|clean|stats|conf)
      ubik install <package>... [--force-yes] [--ignore-errors]
      ubik reinstall <package>... [--force-yes] [--with-deps] [--ignore-errors]
      ubik upgrade [--force-yes] [--ignore-errors]
      ubik upgrade <package>... [--force-yes] [--ignore-errors]
      ubik remove <package>... [--force-yes] [--ignore-errors]
      ubik -h | --help
      ubik -v | --version

    Options:
      --force-yes      Force confirmation questions
      --with-deps      Reinstall deps too
      --ignore-errors  Ignore control commands errors
      -h --help        Show help
      -v --version     Show version

    Ubik is safe when used as directed.
