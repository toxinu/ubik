#!/bin/bash

#
# This file contains libs to create package archive
# Be carefull
#

function files_listing(){
	cd build
	find ./ -type f > ../$NAME/files.lst
	find ./ -type l >> ../$NAME/files.lst
	cd ..
}

function files_blacklist(){
	for line in $(cat ./blacklist); do
		cat ./$NAME/files.lst | grep -v "$line" > ./$NAME/files.lst.tmp
		mv ./$NAME/files.lst.tmp ./$NAME/files.lst
	done
	rm ./$NAMEfiles.lst.tmp > /dev/null 2>&1
}

function help(){
	echo "Usage: make.sh (install|package|purge)"
	echo ""
	echo "  install     Build package"
	echo "  package     Create package archive"
	echo "  clean       Clean old archives"
	echo ""
}

#################################
# Make Package
#################################
function package(){
	touch ./control
	chmod +x ./control
	mkdir $NAME

	files_listing
	files_blacklist

	tar cfj ./$NAME/files.bz2 -T ./$NAME/files.lst
	cp ./control $NAME
	cp ./blacklist $NAME
	tar cf $NAME.tar $NAME 
}
#################################

#################################
# Clean
#################################
function clean(){
	rm -rf $NAME
	rm $NAME.tar
	rm files.bz2
	rm files.lst
}
#################################

. control
if [ "$1" == "install" ]; then
	install
elif [ "$1" == "package" ]; then
	package
elif [ "$1" == "clean" ]; then
	clean
else
	help
fi

