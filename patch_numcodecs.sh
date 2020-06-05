#!/bin/bash

git clone https://github.com/zarr-developers/numcodecs.git
cd numcodecs
git submodule update --init --recursive
git apply ../0001-Create-free-mutex-in-init-destroy.patch
git config --global user.email "a@a.net"
git config --global user.name "fix"
git commit -am "fix"
pip install .
pip freeze | grep numcodecs