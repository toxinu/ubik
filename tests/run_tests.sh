#!/bin/bash
#
#
# In order to run this tests you will need:
#
# 	- virtualenv
#	- pip
#	- Internet connection
#		

##################################################
# Checks
##################################################
set -e
if [ "${PWD##*/}" != "tests" ]; then
	echo "Must be in tests dir"
	exit 1
fi

if [ -z $(which virtualenv ) ]; then
	echo "I need virtualenv"
	exit 1
fi

##################################################
# Variables
##################################################
tests_dir=$(pwd)
env_name="tests-env"	# Used in .gitignore

##################################################
# Run tests
##################################################
if [ -e $tests_dir/$env_name ]; then
	echo " :: Clean old tests"
	rm -rf $tests_dir/$env_name
fi
echo " :: Create virtualenv"
virtualenv $env_name
cd $env_name
source bin/activate
pip install -e ../..
mkdir -p {etc,opt,var/log}
sed 's#%tests_dir%#'$(pwd)'#g' $tests_dir/ubik.conf > $tests_dir/$env_name/etc/ubik.conf
cp $tests_dir/tests_env.py .

# Database tests
echo " :: Run tests_database.py"
cp $tests_dir/tests_database.py .
python tests_database.py -v

# Package tests
echo " :: Run tests_package.py"
cp $tests_dir/tests_package.py .
python tests_package.py -v

echo " :: Done"