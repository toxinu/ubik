#!/usr/bin/env python
# coding: utf-8

import sys
import os
import shutil

from ConfigParser import SafeConfigParser

#debug = True
debug = False

# Change path
pathname = os.path.dirname(sys.argv[0])
if debug:
	print 'sys.argv[0] =', sys.argv[0]
	print 'path =', pathname
	print 'full path =', os.path.abspath(pathname)
os.chdir(os.path.abspath(pathname))

# Settings
name		= 'pkgmgr'
info		= 'Minimal package manager'
description	= open('README.rst').read()
version 	= '0.0.1'
license		= open("LICENSE").read()
author		= 'Geoffrey Lehee'
email		= 'geoffrey@lehee.name'

# Check dependencies
try:
	import clint
except Exception as err:
	print('  -> Please install clint package (%s)' % err)
	sys.exit(1)

try:
	from docopt import docopt
except Exception as err:
	print('  -> Please install docopt package (%s)' % err)
	sys.exit(1)

# Docs
doc = """Pkgmgr installer.
 
Usage:
  setup.py install [--prefix=<path>] [--symlink]
  setup.py reinstall [--prefix=<path>] [--symlink]
  setup.py description
  setup.py license
  setup.py -h | --help
  setup.py --version

Options:
  --prefix=<path>   Installation prefix path [default: /usr/local/pkgmgr]
  --symlink         Create symlink into /usr/local/bin

"""

def install():
	print(' :: Install')
	print(' :: Create prefix (%s)' % prefix)
	shutil.copytree('pkgmgr/lib', '%s/lib' % prefix)
	shutil.copytree('pkgmgr/bin', '%s/bin' % prefix)
	shutil.copytree('pkgmgr/etc', '%s/etc' % prefix)

	# Set binarie
	f = open('pkgmgr/bin/pkgmgr2', 'r').read()
	_f = open('%s/bin/pkgmgr2' % prefix, 'w')
	f = f.replace('<prefix>', '%s' % prefix)
	_f.write(f)
	_f.close()

	# Set core
	f = open('pkgmgr/lib/pkgmgr/core.py', 'r').read()
	_f = open('%s/lib/pkgmgr/core.py' % prefix, 'w')
	f = f.replace('<prefix>', '%s' % prefix)
	_f.write(f)
	_f.close()

	# Set config file
	f = open('pkgmgr/etc/pkgmgr.conf', 'r').read()
	_f = open('%s/etc/pkgmgr.conf' % prefix, 'w')
	f = f.replace('<prefix>', '%s' % prefix)
	_f.write(f)
	_f.close()

	# Create log file
	parser = SafeConfigParser()
	parser.read('%s/etc/pkgmgr.conf' % prefix)
	log_file = parser.get('settings', 'log_file')
	if not os.path.exists(os.path.split(log_file)[0]):
		os.makedirs(os.path.split(log_file)[0])
	if not os.path.exists(log_file):
		open(log_file, 'w').close()

	if args.get('--symlink', False):
		try:
			os.symlink('%s/bin/pkgmgr2' % prefix, '/usr/local/bin/pkgmgr2')
		except:
			pass
		os.chmod('%s/bin/pkgmgr2' % prefix, 0755)

if __name__ == "__main__":
	args = docopt(doc, version=version)
	if debug:
		print(args)
	
	prefix = args.get('--prefix', False)
	if not prefix:
		prefix = '/usr/local/pkgmgr'

	if args['description']:
		print('\n%s (%s) - %s\n\n%s\n%s (%s).' % (name, version, info, description,  author, email))
		sys.exit(0)
	elif args['license']:
		print('\n%s' % license)
		sys.exit(0)
	elif args['install']:
		if not os.path.exists(prefix):
			install()
		else:
			print(' :: Pkgmgr already installed')
			sys.exit(1)

	elif args['reinstall']:
		print(' :: Remove old installation')
		try:
			shutil.rmtree(prefix)
			os.remove('/usr/local/bin/pkgmgr2')
		except:
			pass
		install()
