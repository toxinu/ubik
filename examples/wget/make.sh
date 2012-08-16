#!/bin/bash

#################################
# Variables
#################################
SRC="/usr/local/src/Pkgmgr/examples/wget/src"
DST="/usr/local/src/Pkgmgr/examples/wget/build"
#################################

#################################
# Install
#################################
function install(){
  	cd $SRC
    tar xvf wget-1.13.tar.gz
    cd wget-1.13
    ./configure --prefix=$DST --without-ssl
    make
    make install
}
#################################

if [ -z "$(ls -a | grep .libs.sh)" ]; then
	echo "Need to be in package root"
	exit 1
else
	. .libs.sh
fi

