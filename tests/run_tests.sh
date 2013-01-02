#!/bin/bash
#
#
# In order to run this tests you will need:
#
# 	- virtualenv
#	- pip
#	- Internet connection
#		
start_time=$(date +%s)
##################################################
# Checks
##################################################
set -e
set -u

trap clean EXIT

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

clean () {
	echo " :: Clean before exit"
	if [ -f $tests_dir/$env_name/.webpid ]; then
		kill -9 $(cat $tests_dir/$env_name/.webpid) > /dev/null 2>&1
	fi
}

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

pip install http://pypi.python.org/packages/source/r/requests/requests-1.0.4.tar.gz
pip install http://pypi.python.org/packages/source/i/isit/isit-0.2.3.tar.gz

pip install -e $tests_dir/..
mkdir -p $tests_dir/$env_name/{etc,opt,var}
mkdir -p $tests_dir/$env_name/var/log
sed 's#%tests_dir%#'$tests_dir/$env_name'#g' $tests_dir/ubik.conf > $tests_dir/$env_name/etc/ubik.conf
cp $tests_dir/tests/env.py $tests_dir/$env_name
pip uninstall ubik-toolbelt > /dev/null 2>&1 || true
pip install git+http://github.com/socketubs/ubik-toolbelt.git

# Pre-Tests
echo " :: Create packages"
bash $tests_dir/tests/test_00_create_package.sh "$tests_dir/$env_name"
echo " :: Create repo"
bash $tests_dir/tests/test_01_create_repo.sh "$tests_dir/$env_name"

unset http_proxy
TESTS=$(cd $tests_dir/tests && ls -1 . | grep test_ | grep .py)
for TEST in $TESTS; do
	echo " :: Run $TEST"
	python $tests_dir/tests/$TEST -v
	if [ $? -ne 0 ]; then exit 1; fi
done

# Stop webserver
echo " :: Stop webserver"
WEBPID=$(cat $tests_dir/$env_name/.webpid)
kill -9 $WEBPID

finish_time=$(date +%s)
echo " :: Time duration: $((finish_time - start_time)) secs."
echo " :: Finised"
