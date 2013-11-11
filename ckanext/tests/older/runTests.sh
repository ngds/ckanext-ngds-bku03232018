#!/bin/sh

WORKSPACE=$(pwd)
PYENV_HOME=$WORKSPACE/pyenv/
CKAN_HOME=$WORKSPACE/pyenv/src/ckan


echo Activating pyenv...
. $PYENV_HOME/bin/activate


cd $CKAN_HOME
echo Installing TEST requirements...
pip install -r pip-requirements-test.txt

pip install nosexcover
pip install nosexunit

echo running NOSE tests...
nosetests --with-xunit --verbose --process-restartworker --process-timeout=30 --
no-skip --ckan ckan
