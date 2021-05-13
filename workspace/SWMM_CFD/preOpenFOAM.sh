#!/bin/sh
cd $1 || exit 1
. $WM_PROJECT_DIR/bin/tools/CleanFunctions
cleanCase
. $WM_PROJECT_DIR/bin/tools/RunFunctions
runApplication blockMesh 

