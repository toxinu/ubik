#!/bin/bash
ROOT="${1}"
PKG_ROOT="$ROOT/home/packages"
REPO_ROOT="$ROOT/home/repo"

cd $REPO_ROOT
ubik-repo generate tests --old-format
