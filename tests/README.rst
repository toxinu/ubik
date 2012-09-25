# test_00_create_package

- Create as many package as different package resolution I want
- Test the ubik-package from ubik-toolbelt

# test_01_create_repo

- Create repo with previous packages
- Test the ubik-repo from ubik-toolbelt

# test_10_database

- Sync db with repo
- Check if no package installed
- Check different api methods
- Check simple package query
- Check package query with regex

# test_11_package_01_02

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

# test_12_package_03

- Same as previous but with package_03, which is available, good system and no dep


## Packages informations

Package Available:
    Good System:
      - with one dep(success)      -> package_01    X
      - without dep(success)       -> package_02    X
      - without dep(success)       -> package_03    X

    Any System:
      - with one dep(success)      -> package_04    X
      - without dep(success)       -> package_05    X
      - with itself in dep(fail)   -> package_06

    Other:
      - Bad arch(fail)             -> package_07
      - Bad dist(fail)             -> package_08
      - Bad vers(fail)             -> package_09
      - Unvailable dep(fail)       -> package_10
      - Dep in another arch(fail)  -> package_11
      - Dep in another dist(fail)  -> package_12
      - Dep in another vers(fail)  -> package_13