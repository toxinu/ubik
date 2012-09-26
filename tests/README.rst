# Tests

Tests are executed in virtualenv, test_00 create different package, test_01 create local repo and another bunch of tests do the job.

Test machine is forced to be a DEBIAN 6 i386 with ubik configuration file.

## test_00_create_package

- Create as many package as different package resolution I want
- Test the ubik-package from ubik-toolbelt

## test_01_create_repo

- Create repo with previous packages
- Test the ubik-repo from ubik-toolbelt

## test_10_database

- Sync db with repo
- Check if no package installed
- Check different api methods
- Check simple package query
- Check package query with regex

## test_11_package_01_02

- Package 01 is available and good system with package_02 as dep
- Package 02 is available and good system with no dep

- Database search
- Package objects content
- Installer object
- Dependencies resolver object
- Some api methods
- Bin script from package_01 and package_2
- Remove packages
- Check pacakge content files are removed
- Some api methods

## test_12_package_03

- Same as previous but with package_03, which is available, good system and no dep

## test_13_package_04_05

- Same as test_11_package_01_02 but packages are (noarch/nodist/novers)

## test_14_package_06

- Try to install noarch/nodist/novers package with itself in deps but must fail

### Packages informations

Package Available:
    Good System (i386/debian/6):
      + with package_02 dep(success)     -> package_01
      + without dep(success)             -> package_02
      + without dep(success)             -> package_03
      - without dep, symlinks in package -> package_14

    Any System (noarch/nodist/novers):
      + with package_05 dep(success)     -> package_04
      + without dep(success)             -> package_05
      + with itself in dep(fail)         -> package_06

    Other:
      - Bad arch (x86_64)(fail)                 -> package_07
      - Bad dist (ubuntu)(fail)                 -> package_08
      - Bad vers (5)(fail)                      -> package_09
      - Unvailable dep (jambon)(fail)           -> package_10
      - Dep in another arch (package_07)(fail)  -> package_11
      - Dep in another dist (package_08)(fail)  -> package_12
      - Dep in another vers (package_09)(fail)  -> package_13

Legend:

- "-" not done
- "+" already done
