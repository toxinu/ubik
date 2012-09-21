#!/bin/bash
set -e
set -u

ROOT="${1}"
PKG_ROOT="$ROOT/home/packages"
REPO_ROOT="$ROOT/home/repo"

cd $REPO_ROOT
ubik-repo generate tests --old-format
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
