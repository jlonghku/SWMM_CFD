#!/bin/sh
cd ${0%/*} || exit 1
# install openfoam and set env path
sudo sh -c "wget -O - https://dl.openfoam.org/gpg.key | apt-key add -"
sudo add-apt-repository http://dl.openfoam.org/ubuntu
sudo apt-get update
sudo apt-get -y install openfoam8
echo 'source /opt/openfoam8/etc/bashrc' >>~/.bashrc
. ~/.bashrc

# install pyswmm
sudo apt -y install python3-pip
pip3 install pyswmm==0.6.2 numpy

# get the permission of openfoam modification
sudo chmod 755 -R $WM_PROJECT_DIR/*
# install the new externalCoupledMixedNew boundary
sudo cp -rf externalCoupledMixedNew $FOAM_SRC/finiteVolume/fields/fvPatchFields/derived/
wclean $FOAM_SRC/finiteVolume/fields/fvPatchFields/derived/externalCoupledMixedNew/
wmake $FOAM_SRC/finiteVolume/fields/fvPatchFields/derived/externalCoupledMixedNew/
