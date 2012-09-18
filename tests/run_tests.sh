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
set -u

trap clean EXIT

clean () {
	echo " :: Clean before exit"
	if [ -n "$WEBCODE" ]; then
		kill -9 $WEBCODE > /dev/null 2>&1
	fi
}

: ${WEBCODE:=""}

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
env_name="venv"	# Used in .gitignore

##################################################
# Run tests
##################################################
if [ -e $tests_dir/$env_name ]; then
	echo " :: Clean old tests"
	rm -rf $tests_dir/$env_name
fi

echo " :: Create virtualenv"
virtualenv $tests_dir/$env_name
cd $tests_dir/$env_name
set +u
source $tests_dir/$env_name/bin/activate
set -u
pip install -e $tests_dir/..
mkdir -p $tests_dir/$env_name/{etc,opt,var}
mkdir -p $tests_dir/$env_name/var/log
sed 's#%tests_dir%#'$tests_dir/$env_name'#g' $tests_dir/ubik.conf > $tests_dir/$env_name/etc/ubik.conf
cp $tests_dir/tests/env.py $tests_dir/$env_name
pip install git+http://github.com/Socketubs/Ubik-toolbelt.git

# Pre-Tests
echo " :: Create packages"
bash $tests_dir/tests/test_00_create_package.sh "$tests_dir/$env_name"
echo " :: Create repo"
bash $tests_dir/tests/test_01_create_repo.sh "$tests_dir/$env_name"

# Run webserver
echo " :: Run webserver"
python -m SimpleHTTPServer 8080 &
WEBCODE="$?"
WEBPID="$!"
if [ $WEBCODE -gt 0 ]; then
	echo " :: Failed to start webserver"
	exit 1
fi
echo "    + $WEBPID"

TESTS=$(cd $tests_dir/tests && ls -1 . | grep test_ | grep .py)
for TEST in $TESTS; do
	echo " :: Run $TEST"
	python $tests_dir/tests/$TEST -v
done

# Stop webserver
echo " :: Stop webserver"
kill -9 $WEB_PID

echo " :: Finised"
