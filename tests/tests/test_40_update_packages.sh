#!/bin
set -e
set -u

ROOT="${1}"

PKG_ROOT="$ROOT/home/packages"
REPO_ROOT="$ROOT/home/repo"
BRANCH="tests"

export UBIK_CONF="$ROOT/etc/ubik.conf"

cd $PKG_ROOT

function set_install() {
    local PKG="${1}"
    cd $PKG_ROOT/$PKG
    cp $ROOT/../packages/${PKG}.1_control.py control.py >/dev/null
    cd -
}

function build_package() {
    local PKG="${1}"
    cd $PKG_ROOT/$PKG
    rm -rf $PKG*
    ubik-package package
    ubik-package archive
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


# Stop webserver
echo " :: Stop webserver"
WEBPID=$(cat $ROOT/.webpid)
kill -9 $WEBPID

# package_01
build_package "package_01"
send_to_repo "package_01" "i386" "debian" "6"

# package_02
build_package "package_02"
send_to_repo "package_02" "i386" "debian" "6"

# package_14
build_package "package_14"
send_to_repo "package_14" "i386" "debian" "6"

# package_15
build_package "package_15"
send_to_repo "package_15" "i386" "debian" "6"

# package_16
build_package "package_16"
send_to_repo "package_16" "i386" "debian" "6"

rm $REPO_ROOT/$BRANCH/i386/debian/6/package_03.tar

echo " :: Update repositorie"
cd $REPO_ROOT
ubik-repo generate
cd -

# package_04
echo "123" > $REPO_ROOT/$BRANCH/noarch/nodist/novers/package_04.tar

echo " :: Run webserver"
cd $REPO_ROOT
python -m SimpleHTTPServer 8080 &
WEBPID="$!"
echo "    + $WEBPID"
if [ `ps -p$WEBPID | wc -l` -lt 2 ]; then
    echo " :: Failed to start webserver"
    exit 1
else
    echo "$WEBPID" > $ROOT/.webpid
fi
sleep 3