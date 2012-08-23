#!/usr/bin/env python
# coding: utf-8
import os

from ubik.conf import get_conf

###################
# conf            #
###################
conf_file = os.environ.get('UBIK_CONF', '/etc/ubik.conf')
if not os.path.exists(conf_file):
	print(' :: Configuration file not found (%s)' % conf_file)
	print(' :: You can set UBIK_CONF env variable')
	exit(1)
conf = get_conf(conf_file)

###################
# Init env        #
###################
try:
	os.makedirs(conf.get('settings', 'var_path'))
	os.makedirs(conf.get('settings', 'cache'))
except:
	pass

###################
# Loggers         #
###################
from ubik.logger import logger

###################
# Database        #
###################
from ubik.database import Database
if not os.path.exists(conf.get('paths', 'local_db')):
	logger.warning('No packages.db found, is it normal ?')
	open(conf.get('paths', 'local_db'), 'w').close()
db = Database(open(conf.get('paths', 'local_db')).readlines())
