Tests
=====

Tests are executed in virtualenv, ``test_00`` create different package, ``test_01`` create local repo and another bunch of tests do the job.

Test machine is forced to be a ``debian 6 i386`` with ubik configuration file.

Packages informations
---------------------

============  ======  ======  ======  ==========  ======  ========================
Name          Arch    Dist    Vers    Requires    Status  Description
============  ======  ======  ======  ==========  ======  ========================
package_01    i386    debian  6       package_02    OK    version=0.2
package_02    i386    debian  6                     OK    release=2
package_03    i386    debian  6                     OK
package_04    noarch  nodist  novers  package_05    OK
package_05    noarch  nodist  novers                OK
package_06    noarch  nodist  novers  package_06    KO
package_07    x86_64  debian  6                     KO
package_08    i386    ubuntu  12.04                 KO
package_09    i386    debian  5                     KO
package_10    i386    debian  6       jambon        KO  
package_11    i386    debian  6       package_07    KO
package_12    i386    debian  6       package_08    KO
package_13    i386    debian  6       package_09    KO
package_14    i386    debian  6                     OK    Test symlink
package_15    i386    debian  6                     OK    Test permissions
package_16    i386    debian  6                     OK    With configuration file
package_17    i386    debian  6                     OK    With configuration file
package_18    i386    debian  6                     OK    With configuration file
============  ======  ======  ======  ==========  ======  ========================

test_00_create_package
######################

- Create as many package as different package resolution I want
- Test the ``ubik-package`` from ``ubik-toolbelt``

test_01_create_repo
###################

- Create repo with previous packages
- Test the ``ubik-repo`` from ``ubik-toolbelt``

test_10_database
################

- Sync db with repo
- Check if no package installed
- Check different api methods
- Check simple package query
- Check package query with regex

test_11_package_01_02
#####################

- Package 01 is available and good system with ``package_02`` as dep
- Package 02 is available and good system with no dep

- Database search
- Package objects content
- Installer object
- Dependencies resolver object
- Some api methods
- Bin script from ``package_01`` and ``package_2``
- Remove packages
- Check pacakge content files are removed
- Some api methods

test_12_package_03
##################

- Same as previous but with ``package_03``, which is available, good system and no dep

test_13_package_04_05
#####################

- Same as ``test_11_package_01_02`` but packages are (noarch/nodist/novers)

test_14_package_06
##################

- Try to install noarch/nodist/novers package with itself in deps but must fail

test_15_package_07_08_09
########################

- Try to get these packages from db object and must fail
  + ``package_07`` bad arch
  + ``package_08`` bad dist
  + ``package_09`` bad vers

test_16_package_10
##################

- Try to resolv with Installer object and must faild with unvailable ``jambon`` dep

test_17_package_11_12_13
########################

- Try to install package with dep which have wrong arch (``package_11``, ``package_07``)
- Try to install package with dep which have wrong arch (``package_12``, ``package_08``)
- Try to install package with dep which have wrong arch (``package_13``, ``package_09``)

test_18_package_14
##################

- Install package with symlink and check it's ok after install

test_19_package_15
##################

- Install package with bin file in ``777`` permissions and check it's ok after install

test_20_package_16-17-18
########################

- Install two packages with ``/etc/package_.conf`` files in order to check ``safe_conf`` option later.

test_40_update_packages
#######################

- ``package_01`` downgrade from ``0.2`` to ``0.1``
- ``package_02`` downgrade release ``2`` to ``1``
- ``package_14`` upgrade release ``0`` to ``1`` and version ``0.1`` to ``0.2``
- ``package_15`` upgrade release ``0`` to ``1``
- ``package_16`` upgrade version ``0.1`` to ``0.2``
- ``package_03`` removed
- ``package_04`` bad md5 on repositorie

Regenerate repositorie Packages.db

test_41_database
################

- ``package_03`` already installed but removed from repositorie, so check if always here
- sync database

test_45_package_05
##################

- reinstall ``package_05``
- remove file from ``package_05`` and reinstall it
- check if correct reinstalled

test_46_database
################

- sync database
- remove ``package_03``

TODO

- sync database and check if package_03 still available


Todo
----

- Test md5 checksum
- Test package version upgrade
- test package release upgrade
- Test reinstall
- Check safe_conf option (issue #36)
