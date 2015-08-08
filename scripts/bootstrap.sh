#!/usr/bin/env bash

### Bootstrap the application, starting from python + virtualenv
#
# /local             Python virtualenv
# /node_modules      node.js external modules
# /bower_components  Bower external modules

set -e

pyvenv local
source ./local/bin/activate

./local/bin/pip install --upgrade pip
./local/bin/pip install -r requirements.txt
./local/bin/nodeenv --python-virtualenv
./local/bin/npm install
./node_modules/.bin/bower install
