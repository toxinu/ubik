Description
===========

Minimal package manager inspired by the ``pkgmgr`` of [Canopsis][1] pkgmgr but rewritten in Python (from bash).  

For information:
```
Canopsis is a hypervisor, built on top of all open source monitoring solutions
to agregate, correlate and ponderate events flowing from them.
```


![pkgmgr screenshot01](http://dl.dropbox.com/u/79447684/Github/Pkgmgr/screenshot_01.png "Pkgmgr Screenshot01")
![pkgmgr screenshot02](http://dl.dropbox.com/u/79447684/Github/Pkgmgr/screenshot_02.png "Pkgmgr Screenshot02")

Features
========

 * Install/Remove/Upgrade/Reinstall
 * Deps resolver for installation
 * Cache
 * Md5 checker
 * Control file for package
 * Post/Pre Install/Remove/Upgrade controls
 * Python

Installation
============

```
pip install git+http://github.com/Socketubs/Pkgmgr.git
```

For canopsis:
```
pip install --install-option="--prefix=/opt/canopsis"`git+http://github.com/Socketubs/Pkgmgr.git`
```

Create package
==============

You can see how to create ````wget``` package with __Pkgmgr__ in ```examples``` dir.

```
cd /usr/local/src
pkgmgr-create my_package
cd my_package
mkdir -p src/usr/bin
vim src/usr/bin/hello.sh		# Create your bash hello world
vim make.sh
...
function install(){
    cd $SRC
    tar xvf wget-1.13.tar.gz
    cd wget-1.13
    ./configure --prefix=$DST --without-ssl
    make
    make install
}
...
./make.sh install
./make.sh package
```

Thanks
======

Thanks to [Requests][5], [Docopt][6] and [ProgressBar][7] to be awesome tools.

License
=======

License is [AGPL3][4], it fully compatible with ``Canopsis``.
See [LICENSE][3].

[1]: https://github.com/capensis/canopsis
[2]: http://gist.io/3193620
[3]: https://raw.github.com/Socketubs/pkgmgr/master/LICENSE
[4]: http://www.gnu.org/licenses/agpl.html
[5]: https://github.com/kennethreitz/requests
[6]: https://github.com/docopt/docopt
[7]: http://code.google.com/p/python-progressbar/
