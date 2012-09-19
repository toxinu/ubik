#!/bin
set -e
set -u

ROOT="${1}"

# i386
# debian
# 6

# package_01 : 	deps=[package_02]
#		arch=i386
#		dist=debian
#		vers=6
#
# package_02 : 	deps=[]
#		arch=i386
#		dist=debian
#		vers=6
#
# package_03 : 	deps=[package_03]
#		arch=i386
#		dist=debian
#		vers=6
#
# package_04 : 	deps=[package_05]
#		arch=noarch
#		dist=nodist
#		vers=novers
#
# package_05 : 	deps=[]
#		arch=noarch
#		dist=nodist
#		vers=novers
#
# package_06 : 	deps=[package_03]
#		arch=noarch
#		dist=nodist
#		vers=novers

PKG_ROOT="$ROOT/home/packages"
REPO_ROOT="$ROOT/home/repo"
BRANCH="tests"

mkdir -p $PKG_ROOT
ubik-repo create $REPO_ROOT
mkdir -p $REPO_ROOT/tests/{noarch,i386,x86_64}
mkdir -p $REPO_ROOT/tests/noarch/nodist/novers
mkdir -p $REPO_ROOT/tests/i386/debian/{5,6}
mkdir -p $REPO_ROOT/tests/x86_64/nodist/novers
cd $PKG_ROOT

function create_package() {
	local PKG="${1}"
	cd $PKG_ROOT
	ubik-package create $PKG
	cd -
	set_bin "$PKG"
	set_install "$PKG"
}

function set_deps() {
	local PKG="${1}"
	local DEPS="${2}"
	cd $PKG_ROOT/$PKG
	if [[ $(uname -s) =~ "[Dd]arwin" ]]; then
		sed -i "" "s#REQUIRES=""#REQUIRES=\"$DEPS\"#g" control >/dev/null
	else
		sed -i "s#REQUIRES=""#REQUIRES=\"$DEPS\"#g" control >/dev/null
	fi
	cd -
}

function set_bin() {
	local PKG="${1}"
	cd $PKG_ROOT/$PKG
	mkdir -p src/bin >/dev/null
	echo -e '#!/bin/bash'"\necho \"Im $PKG\"" > src/bin/$PKG
	chmod +x src/bin/$PKG
	cd -
}

function set_install() {
	local PKG="${1}"
	cd $PKG_ROOT/$PKG
	if [[ $(uname -s) =~ "[Dd]arwin" ]]; then
		sed -i "" "s#true#cp -R \$SRC/* \$DST#g" make.sh >/dev/null
	else
		sed -i "s#true#cp -R \$SRC/* \$DST#g" make.sh >/dev/null
	fi
	cd -
}

function build_package() {
	local PKG="${1}"
	cd $PKG_ROOT/$PKG
	./make.sh install
	./make.sh package
	cd -
}

function send_to_repo() {
	local PKG="${1}"
	local ARCH="${2}"
	local DIST="${3}"
	local VERS="${4}"
	mkdir -p $REPO_ROOT/$BRANCH/$ARCH/$DIST/$VERS >/dev/null
	cp $PKG_ROOT/$PKG/$PKG.tar $REPO_ROOT/$BRANCH/$ARCH/$DIST/$VERS
}

# package_01
create_package "package_01"
set_deps "package_01" "package_02"
build_package "package_01"
send_to_repo "package_01" "i386" "debian" "6"

# package_02
create_package "package_02"
build_package "package_02"
send_to_repo "package_02" "i386" "debian" "6"

# package_03
create_package "package_03"
build_package "package_03"
send_to_repo "package_03" "i386" "debian" "6"

# package_04
create_package "package_04"
set_deps "package_04" "package_05"
build_package "package_04"
send_to_repo "package_04" "noarch" "nodist" "novers"

# package_05
create_package "package_05"
build_package "package_05"
send_to_repo "package_05" "noarch" "nodist" "novers"

# package_06
create_package "package_06"
set_deps "package_06" "package_06"
build_package "package_06"
send_to_repo "package_06" "noarch" "nodist" "novers"

# package_07
create_package "package_07"
build_package "package_07"
send_to_repo "package_07" "x86_64" "debian" "6"

# package_08
create_package "package_08"
build_package "package_08"
send_to_repo "package_08" "i386" "ubuntu" "12.04"

# package_09
create_package "package_09"
build_package "package_09"
send_to_repo "package_09" "i386" "debian" "5"

# package_10
create_package "package_10"
set_deps "package_10" "jambon"
build_package "package_10"
send_to_repo "package_10" "i386" "debian" "6"

# package_11
create_package "package_11"
set_deps "package_11" "package_07"
build_package "package_11"
send_to_repo "package_11" "i386" "debian" "6"

# package_12
create_package "package_12"
set_deps "package_12" "package_08"
build_package "package_12"
send_to_repo "package_12" "i386" "debian" "6"

# package_13
create_package "package_13"
set_deps "package_13" "package_09"
build_package "package_13"
send_to_repo "package_13" "i386" "debian" "6"
