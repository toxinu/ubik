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

from subprocess import Popen, PIPE, STDOUT

"""
Remove and check is still present package_03
"""

class Test_Database_Package_03(unittest.TestCase):

    def setUp(self):
        self.db = api.db
        self.package = self.db.packages['package_03']

    def test_100_remove_package_03(self):
        self.db.sync()
        remover = Remover()
        remover.feed(self.package)
        self.assertEqual(len(remover.packages), 1)
        self.assertEqual(remover.packages[0].name, 'package_03')

        remover.remove()
        self.assertEqual(self.db.count_installed(), 3)

    def test_202_remove_file_removed(self):
        path = "%s/bin/package_03" % api.conf.get('settings', 'packages')
        self.assertFalse(os.path.exists(path))

    def test_301_check_package_03_here(self):
        # Package_03 have been removed from repositorie, so check if still present
        # Must not be
        self.db.sync()
        self.assertFalse(self.db.get('package_03'), msg='Package_03 still available')
        try:
            self.db.packages['package_03']
            raise Exception('Package_03 still available')
        except:
            pass

if __name__ == '__main__':
    unittest.main()
