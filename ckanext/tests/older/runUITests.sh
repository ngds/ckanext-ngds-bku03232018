#!/bin/sh

WORKSPACE=$(pwd)
PYENV_HOME=$WORKSPACE/pyenv/
CKAN_HOME=$WORKSPACE/pyenv/src/ckan
CKANEXT_HOME=$WORKSPACE/pyenv/src/ckanext
#SELENIUM_TESTS_HOME=$WORKSPACE/selenium_tests
SELENIUM_TESTS_HOME=$WORKSPACE/ui/harvest
SELENIUM_HOME=$WORKSPACE/selenium

# Create virtualenv and install necessary packages
if [ ! -d $PYENV_HOME/bin ];
then
  virtualenv --no-site-packages $PYENV_HOME
fi

echo Activating pyenv...
. $PYENV_HOME/bin/activate

echo install dependencies
cd $PYENV_HOME
pip install -U selenium
pip install selenose
cd

#echo start selenium server
#cd $SELENIUM_HOME
#. se.sh&
#cd


echo run tests
echo do not forget to start ckan server with the command:
echo paster serve development.ini within pyenv/src/ckan
cd $SELENIUM_TESTS_HOME
# starts selenium server and runs the test
nosetests --with-selenium-server test_harvest_config.py

cd $WORKSPACE