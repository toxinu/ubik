#!/bin/bash
set -e
set -u

ROOT="${1}"
PKG_ROOT="$ROOT/home/packages"
REPO_ROOT="$ROOT/home/repo"

set +u
source $ROOT/bin/activate
set -u

cd $REPO_ROOT
ubik-repo generate tests
echo " :: Run webserver"
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
