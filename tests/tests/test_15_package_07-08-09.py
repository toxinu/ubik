#!/usr/bin/env python
# coding: utf-8
import os

import env
import unittest

import ubik.core as api

"""
Package Available:
    Bad arch:
      - package_07 have bad arch (x86_64)
    Bad dist:
      - package_08 have bad dist (ubuntu)
    Bad vers:
      - package_09 have bad vers (5)
"""

class TestPackage_07_08_09(unittest.TestCase):

    def test_01_get_packages(self):
        self.db = api.db
	try:
	        self.package_07 = self.db.packages['package_07']
		raise Exception('Package_07 must be unvailable')
	except KeyError:
		pass
	try:
	        self.package_08 = self.db.packages['package_08']
		raise Exception('Package_08 must be unvailable')
	except KeyError:
		pass
	try:
	        self.package_09 = self.db.packages['package_09']
		raise Exception('Package_09 must be unvailable')
	except KeyError:
		pass

if __name__ == '__main__':
    unittest.main()
