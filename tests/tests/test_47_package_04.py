#!/usr/bin/env python
# coding: utf-8
import os
import stat

import env
import unittest

import ubik.core as api

from ubik.installer import Installer
from ubik.reinstaller import Reinstaller
from ubik.remover import Remover

from ubik.tools import clean

from subprocess import Popen, PIPE, STDOUT

"""
Reinstall package_04 which have a bad md5 on repo
"""

class TestPackage_04(unittest.TestCase):

    def setUp(self):
        self.db = api.db
        self.package = self.db.packages['package_04']

    def test_100_install_package(self):
        clean()
        # Invalid local archive package
        os.system('echo "jambon" >> %s/var/lib/ubik/packages/package_04.tar' % api.conf.get('settings', 'packages'))
        self.db.sync()
        installer = Installer()
        installer.resolve(self.package)
        installer.feed(installer.get_resolved())
        self.assertEqual(len(installer.packages), 2)

        try:
            installer.download()
            raise Exception('Downloader must failed')
        except:
            pass

        try:
            self.db.get_installed()['package_04']
            raise Exception('Package_04 must not be installed')
        except:
            pass
        self.assertEqual(self.db.count_installed(), 3)

if __name__ == '__main__':
    unittest.main()
