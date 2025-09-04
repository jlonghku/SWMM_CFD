#!/bin/sh
path=$(dirname $(readlink -f $0))
#cd ${0%/*}"/"$1 || exit 1
cd $1 || exit 1
. $WM_PROJECT_DIR/bin/tools/RunFunctions
application="$(getApplication)"
cd $path || exit 1 # Run from this directory 
$application -case $1
