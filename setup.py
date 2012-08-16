#!/usr/bin/env python
# coding: utf-8

import os
import sys

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

if sys.argv[-1] == 'publish':
	os.system('python setup.py sdist upload')
	sys.exit()

setup(
	name='pkgmgr',
	version='0.1',
	description='Minimal packages manager',
	long_description=open('README.md').read(), 
	license=open("LICENSE").read(),
	author="Geoffrey Lehee",
	author_email="geoffrey@lehee.name",
	url='https://github.com/socketubs/Pkgmgr/',
	keywords="pkgmgr package linux",
	packages = ['pkgmgr'],
	scripts=['bin/pkgmgr','bin/pkgmgr-postinstall','bin/pkgmgr-create'],
	install_requires=['progressbar', 'requests', 'docopt']
)
