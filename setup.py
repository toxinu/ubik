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
	name='ubik',
	version='0.1.2',
	description='Minimal packages manager',
	long_description=	open('README.rst').read() + '\n\n' +
						open('API.rst').read() + '\n\n' +
						open('HISTORY.rst').read(), 
	license=open("LICENSE").read(),
	author="Geoffrey Lehee",
	author_email="geoffrey@lehee.name",
	url='https://github.com/socketubs/Ubik/',
	keywords="ubik package linux",
	packages = ['ubik'],
	scripts=['scripts/ubik','scripts/echo_ubik_conf'],
	install_requires=['progressbar==2.3', 'requests', 'docopt==0.5.0', 'isit==0.1.3'],
	classifiers=(
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7')
)
