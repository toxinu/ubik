#!/usr/bin/env python
# coding: utf-8

import os
import sys
import re

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

def get_version():
    VERSIONFILE="ubik/__init__.py"
    initfile_lines = open(VERSIONFILE, "rt").readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

if sys.argv[-1] == 'publish':
	os.system('python setup.py sdist upload')
	sys.exit()

setup(
	name = 'ubik',
	version = get_version(),
	description = 'Minimal packages manager',
	long_description =	open('README.rst').read() + '\n\n' +
						open('API.rst').read() + '\n\n' +
						open('HISTORY.rst').read(),
	license = open("LICENSE").read(),
	author = "Geoffrey Lehee",
	author_email = "geoffrey@lehee.name",
	url = 'https://github.com/socketubs/Ubik/',
	keywords = "ubik package linux",
	packages = ['ubik'],
	scripts = ['scripts/ubik','scripts/echo_ubik_conf'],
	install_requires = ['progressbar==2.3', 'requests==1.1.0', 'docopt==0.5.0', 'isit==0.2.4'],
	classifiers = [
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7']
)
