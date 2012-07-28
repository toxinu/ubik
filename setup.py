#!/usr/bin/env python
# coding: utf-8

import sys
import os
import shutil

from pwd import getpwnam  
from grp import getgrnam
from ConfigParser import SafeConfigParser

debug = False
#debug = True

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
description	= open('README.md').read()
version 	= '0.0.1'
license		= open("LICENSE").read()
author		= 'Geoffrey Lehee'
email		= 'geoffrey@lehee.name'

# Check dependencies
try:
	import requests
except Exception as err:
	print('  -> Please install requests package (%s)' % err)
	sys.exit(1)

try:
	from docopt import docopt
except Exception as err:
	print('  -> Please install docopt package (%s)' % err)
	sys.exit(1)

# Docs
doc = """Pkgmgr installer.
 
Usage:
  setup.py install [--prefix=<path>] [--symlink] [--user-owner=<user>] [--group-owner=<group>] [--canopsis]
  setup.py description
  setup.py license
  setup.py -h | --help
  setup.py --version

Options:
  --symlink                    Create symlink into /usr/local/bin
  --canopsis                   Canopsis installation (use default canopsis settings)
  --prefix=<path>              Installation prefix path [default: /usr/local/pkgmgr]
  --user-owner=<user>          User owner [default: root]
  --group-owner=<group>        Group owner [default: root]

"""

def install():
	if args.get('--canopsis', False):
		if args['--user-owner'] == 'root':
			args['--user-owner'] = 'canopsis'
		if args['--group-owner'] == 'root':
			args['--group-owner'] = 'canopsis'
		if args['--prefix'] == '/usr/local/pkgmgr':
			args['--prefix'] = '/opt/canopsis'

	prefix = args['--prefix']

	# Check user exist
	print (' :: Check user and group')
	user_owner = args['--user-owner']
	group_owner = args['--group-owner']
	try:
		user_id = getpwnam(user_owner).pw_uid
		print('    | User %s found (%s)' % (user_owner, user_id))
	except Exception as err:
		print('Error: %s user not exit.\nTraceback: %s' % (user_owner, err))
		sys.exit(1)
	try:
		group_id = getgrnam(group_owner).gr_gid
		print('    | Group %s found (%s)' % (group_owner, group_id))
	except Exception as err:
		print('Error: %s group not exist.\nTraceback: %s' % (group_owner, err))
		sys.exit(1)

	print(' :: Copy files into %s' % prefix)

	# Lib
	print('    | Libraries')
	root_src_dir = 'pkgmgr/lib'
	root_dst_dir = '%s/lib' % prefix

	for src_dir, dirs, files in os.walk(root_src_dir):
		dst_dir = src_dir.replace(root_src_dir, root_dst_dir)
    	if not os.path.exists(dst_dir):
        	os.mkdir(dst_dir)
        	os.chown(dst_dir, user_id, group_id)
        	os.chmod(dst_dir, 0755)
    	for file_ in files:
			src_file = os.path.join(src_dir, file_)
			dst_file = os.path.join(dst_dir, file_)
			if os.path.exists(dst_file):
				os.remove(dst_file)
			shutil.copy(src_file, dst_dir)
			os.chown(dst_file, user_id, group_id)
			os.chmod(dst_file, 0755)

    # Bin
	print('    | Binaries')
	root_src_dir = 'pkgmgr/bin'
	root_dst_dir = '%s/bin' % prefix

	for src_dir, dirs, files in os.walk(root_src_dir):
		dst_dir = src_dir.replace(root_src_dir, root_dst_dir)
    	if not os.path.exists(dst_dir):
        	os.mkdir(dst_dir)
        	os.chown(dst_dir, user_id, group_id)
        	os.chmod(dst_dir, 0755)
    	for file_ in files:
			src_file = os.path.join(src_dir, file_)
			dst_file = os.path.join(dst_dir, file_)
			if os.path.exists(dst_file):
				os.remove(dst_file)
			shutil.copy(src_file, dst_dir)
			os.chown(dst_file, user_id, group_id)
			os.chmod(dst_file, 0755)

    # Etc
	print('    | Configuration files')
	
	root_src_dir = 'pkgmgr/etc'
	root_dst_dir = '%s/etc' % prefix

	dst_dir = root_dst_dir
	src_dir = root_src_dir
	if not os.path.exists(dst_dir):
		os.mkdir(dst_dir)
	os.chown(dst_dir, user_id, group_id)
	os.chmod(dst_dir, 0755)

	if args.get('--canopsis', False):
		src_file = os.path.join(src_dir, 'pkgmgr.conf.canopsis')
	else:
		src_file = os.path.join(src_dir, 'pkgmgr.conf')

	dst_file = os.path.join(dst_dir, 'pkgmgr.conf')
	
	if os.path.exists(dst_file):
		os.remove(dst_file)
	
	shutil.copy(src_file, dst_file)
	os.chown(dst_file, user_id, group_id)
	os.chmod(dst_file, 0755)

	print(' :: Set prefix path')

	# Set binarie
	f = open('pkgmgr/bin/pkgmgr', 'r').read()
	_f = open('%s/bin/pkgmgr' % prefix, 'w')
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
	if args.get('--canopsis', False):
		f = open('pkgmgr/etc/pkgmgr.conf.canopsis', 'r').read()
	else:
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
		os.chown(os.path.split(log_file)[0], user_id, group_id)
		os.chmod(os.path.split(log_file)[0], 0755)
	if not os.path.exists(log_file):
		open(log_file, 'w').close()
		os.chown(log_file, user_id, group_id)
		os.chmod(log_file, 0755)

	if args.get('--symlink', False):
		print(' :: Create symlink')
		try:
			os.symlink('%s/bin/pkgmgr' % prefix, '/usr/local/bin/pkgmgr')
		except:
			pass
		os.chmod('%s/bin/pkgmgr' % prefix, 0755)

if __name__ == "__main__":
	args = docopt(doc, version=version)
	if debug:
		print(args)
	
	if args['description']:
		print('\n%s (%s) - %s\n\n%s\n%s (%s).' % (name, version, info, description,  author, email))
		sys.exit(0)
	elif args['license']:
		print('\n%s' % license)
		sys.exit(0)
	elif args['install']:
		install()