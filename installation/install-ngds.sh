#!/bin/bash
#
# ___NGDS_HEADER_BEGIN___
#
# National Geothermal Data System - NGDS
# https://github.com/ngds
#
# File: <filename>
#
# Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey
#
# Please Refer to the README.txt file in the base directory of the NGDS
# project:
# https://github.com/ngds/ckanext-ngds/README.txt
#
# ___NGDS_HEADER_END___

#
# A few notes on logging
#   * echo commands are written to the console and logged to $LOGFILE
#     simultaneously via the tee command ('| tee -a $LOGFILE').
#   * commands that are logged have both their stdout and stderr
#     written to $LOGFILE via redirection ('&>>$LOGFILE')

this_script=`basename $0`
MYUSERID=ngds


#
# configure_properties
#
# Update this section to load required properties or path for NGDS Installation.
# This section can be moved outside this script later so that user doesn't need to 
# edit this script to file for the installation.
#
function configure_properties() {
    
    #Path where application and data are installed.
    APPS=/opt/local

    #Tomcat Installation Path
    CATALINA_HOME=/usr/share/tomcat
    
    #Github Account Details
    GIT_UNAME=
    GIT_PWD=

    ## The following properties can be left as it is for trying out this script.
    
    #CKAN Site URL
    site_url='http://sample.ckan.org'

    #Application Deployment setup(central|node).
    deployment_type="central"

    # CKAN DB username
    pg_id_for_ckan=ckan_default
    # CKAN DB password
    pg_pw_for_ckan=pass
    #CKAN DB name
    pg_db_for_ckan=ckan_default
    #Datastore DB Username
    pg_id_datastore=datastore_default
    #Datastore DB pass
    pg_pw_datastore=pass
    #Datastore Database Name
    pg_db_for_datastore=datastore_default

    #Application defult admin user for setup.
    ADMIN_NAME=admin
    ADMIN_PWD=admin
    ADMIN_EMAIL=temp_admin@admin.com

    #Server Name details for HTTP server to register with.
    SERVER_NAME=127.0.0.1
    SERVER_NAME_ALIAS=localhost    
}

function setup_env() {

    configure_properties

    # Absolute path to this script
    SCRIPT=$(readlink -f "$0")
    SCRIPTPATH=$(dirname "$SCRIPT")

    #Config file update script
    CONFIG_UPDATER=$SCRIPTPATH/update_config.py

    # Prepare temporary directory for downloads and the like
    TEMPDIR="tmp_install-ngds-$timestamp.tmp"
    run_or_die mkdir -p $TEMPDIR
    chown $MYUSERID:$MYUSERID $TEMPDIR

    #DOWLOADS="/home/ngds/install/downloads"

    APPS_BIN=$APPS/bin
    APPS_ETC=$APPS/etc
    APPS_LIB=$APPS/lib

    #Python Environment Directory
    PYENV_DIR=$APPS_BIN/default

    CKAN_ETC=$APPS_ETC/ckan

    APPS_SRC=$PYENV_DIR/src

    CKAN_LIB=$APPS_LIB/ckan/default

    sudo mkdir -p $CKAN_LIB
    sudo chown -R $MYUSERID:$MYUSERID $CKAN_LIB    

    #Directory where CKAN will store uploaded files.
    FILESTORE_DIRECTORY=$CKAN_LIB/filestore

    SOLR_CATALINA_BASE=$APPS_ETC/tomcat/solr
    GEOSERVER_CATALINA_BASE=$APPS_ETC/tomcat/geoserver

    SOLR_LIB=$APPS_LIB/solr
    GEOSERVER_LIB=$APPS_LIB/geoserver
    NGDS_SCRIPTS=$APPS_ETC/ngds/scripts
    sudo mkdir -p $SOLR_LIB $SOLR_CATALINA_BASE $GEOSERVER_CATALINA_BASE $NGDS_SCRIPTS $GEOSERVER_LIB
    sudo chown -R $MYUSERID:$MYUSERID $SOLR_LIB $NGDS_SCRIPTS $GEOSERVER_LIB
    sudo chown -R $MYUSERID:$MYUSERID $SOLR_CATALINA_BASE $GEOSERVER_CATALINA_BASE
}

function check_downloads() {
  for pkg in \
      jetty-distribution-9.0.5.v20130815.tar.gz \
      solr-4.4.0.tgz ;do
    if [ ! -f $DOWLOADS/$pkg ] ;then
      #mkdir -p $DOWLOADS
      #scp -p ${DOWNLOAD}/${pkg} $DOWLOADS
      echo "Please download $pkg distribution for the installation to proceed."
      exit 0
    fi
  done
}

#
# print_help
#
function print_help () {
    cat <<EOHELP
Use $this_script to install NGDS and components upon which it depends.  Note
that this script requires administrative privileges to install various 
components.

[sudo] $this_script -f <configuration file>

where <configuration file> is a file containing configuration details. For
details about the parameters contained in this file see the '-g' option
below.

Alternately, $this_script can be invoked with the following flags:

-h Displays this help

-g Emits a sample configuration file with explanations of the parameters
   You can customize this file for your particular installation.
EOHELP
}


#
# print_config_file
#
function print_config_file () {

configure_properties
    cat <<EOCONFIG
# NGDS Installation Configuration File
#
# <License details>
#
# <Link to NGDS web site and details>
# 
# Use this file to set the parameters for installing the NGDS web application.

#
# Deployment type
# 
# The web application can be deployed in one of two ways: As a repository
# node, or as an aggregating catalog. The default and typical deployment type
# is the repository node. When deployed this way (by setting deployment_type
# to repository_node) the web application allows the user to upload and share
# their data with the world. When deployed as an aggregating catalog the web
# application harvests the metadata (but not to the data) of registered
# repository nodes and serves as a search engine that spans those nodes(node|central).
deployment_type=$deployment_type

# CKAN requires login credentials for the PostgreSQL database
pg_id_for_ckan=$pg_id_for_ckan
pg_pw_for_ckan=$pg_pw_for_ckan
pg_db_for_ckan=$pg_db_for_ckan
pg_id_datastore=$pg_id_datastore
pg_pw_datastore=$pg_pw_datastore
pg_db_for_datastore=$pg_db_for_datastore

# Application installation path. All application binary,liba and onfig options 
# will go under this directory
APPS=$APPS

# Tomcat Installation Path
CATALINA_HOME=$CATALINA_HOME
    
#CKAN Site URL
site_url=$site_url

#Application defult admin user for setup.
ADMIN_NAME=$ADMIN_NAME
ADMIN_PWD=$ADMIN_PWD
ADMIN_EMAIL=$ADMIN_EMAIL

#Server Name details for HTTP server to register with.
SERVER_NAME=$SERVER_NAME
SERVER_NAME_ALIAS=$SERVER_NAME_ALIAS

EOCONFIG
}

#
# run_or_die
#
# runs a command and returns if it succeeds; otherwise it exits with
#   the failing command's return value.  Appropriate messages are written.
# params: a command passed in as an unquoted string (exactly as it would be
#   typed on the command line)
# example invocation: run_or_die apt-get install
# assumptions: It is assumed that $LOGFILE is the path to a log file into which
#   to write log messages.
#
function run_or_die() {
    if [ -z $LOGFILE ]; then {
        LOGFILE="/dev/null"
    }
    fi
    echo "$this_script: running '$*'" | tee -a $LOGFILE
    # Execute the command and redirect both stdout and stderr to the LOGFILE
    $* &>>$LOGFILE
    # Using tee here causes $? to get the return value of tee, not that of
    # the command itself.
#    $* 2>>$LOGFILE #| tee -a $LOGFILE
    local ret=$?
    if [ $ret -ne 0 ]; then {
        echo "$this_script: '$*' failed." | tee -a $LOGFILE 
        echo "$this_script: See the log file '$LOGFILE' to fix the issue and try again."
        exit $ret
    }
    else {
        echo "$this_script: '$*' succeeded." | tee -a $LOGFILE
        return
    }
    fi
}

# Install CKAN
# These steps (and the numbering indicated below) correspond to the
# instructions at http://docs.ckan.org/en/ckan-2.0/install-from-source.html
#
function install_ckan() {
    # Step 1: Install the required packages
    run_or_die apt-get -y update
    #run_or_die apt-get -y upgrade
    run_or_die apt-get -y install python-dev
    run_or_die apt-get -y install postgresql-9.1-postgis
    run_or_die apt-get -y install libpq-dev
    run_or_die apt-get -y install python-pip
    run_or_die apt-get -y install python-virtualenv
    run_or_die apt-get -y install git-core
    
    # TODO
    # Here we might want to get just the solr WAR file and install it into Tomcat
    # instead of having a whole other Java container running.
    run_or_die apt-get -y install solr-jetty
    # TODO
    # Here we might want to try using the Oracle JDK and even adding in the
    # native iamging extensions to improve map creation and handling.
    # TODO
    # What if Oracle's JDK is already installed? Will this install OpenJDK?
    # Should we be testing for that?
    run_or_die apt-get -y install openjdk-6-jdk

    # The following steps are taken directly from the CKAN 2.0.1 installation
    # instructions.
    #
    #
    # Step 2: Install CKAN into a Python environment
    # Step 2a
    run_or_die mkdir -p $PYENV_DIR
    run_or_die chown $MYUSERID:$MYUSERID $PYENV_DIR
    run_or_die mkdir -p $CKAN_ETC/default
    run_or_die chown -R $MYUSERID:$MYUSERID $CKAN_ETC
    run_or_die virtualenv --no-site-packages $PYENV_DIR
    . $PYENV_DIR/bin/activate
    #
    # Step 2b
    # TODO
    # Make sure this git URL is correct.
    run_or_die $PYENV_DIR/bin/pip install -e 'git+https://github.com/okfn/ckan.git@ckan-2.0.1#egg=ckan'
    #
    # Step 2c
    # TODO
    # Before running this step, make sure pip-requirements.txt contains the full
    # set of requirements needed by NGDS.
    run_or_die $PYENV_DIR/bin/pip install -r $APPS_SRC/ckan/pip-requirements.txt
    run_or_die $PYENV_DIR/bin/pip install -r $APPS_SRC/ckan/pip-requirements-test.txt
    deactivate
    . $PYENV_DIR/bin/activate
    
    run_or_die $PYENV_DIR/bin/pip install configobj
    #
    #
    # Step 3: Setup a PostgreSQL database
    # Note: We do not test whether PostgreSQL's encoding is UTF8.
    # TODO
    # Handle parameterized ckan username and password
    #run_or_die sudo -u postgres createuser -S -D -R -P $pg_id_for_ckan
    echo "CREATE ROLE $pg_id_for_ckan ENCRYPTED PASSWORD '$pg_pw_for_ckan' NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN;" > $TEMPDIR/default_ckan_user.sql
    run_or_die sudo -u postgres psql -d postgres -f $TEMPDIR/default_ckan_user.sql
    run_or_die sudo -u postgres createdb -O $pg_id_for_ckan $pg_db_for_ckan -E utf-8
    #
    #
    # Step 4: Create a CKAN config file
    pushd $APPS_SRC/ckan
    run_or_die $PYENV_DIR/bin/paster make-config ckan $CKAN_ETC/default/development.ini
    popd
    #
    # Generate an awk script to modify the development.ini
    #echo "/^sqlalchemy\.url/ { sub(/sqlalchemy\.url = postgresql:\/\/[^:]+:[^@]+@localhost\/.+$/, \"sqlalchemy.url = postgresql://$pg_id_for_ckan:$pg_pw_for_ckan@localhost/$pg_db_for_ckan\") }; { print }" > $TEMPDIR/modify-development-ini.awk
    #
    # Modify a copy of the development.ini
    #awk -f $TEMPDIR/modify-development-ini.awk $CKAN_ETC/default/development.ini > $TEMPDIR/development.ini
    #Update the parameter value in development.ini
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -k sqlalchemy.url -v "postgresql://$pg_id_for_ckan:$pg_pw_for_ckan@localhost/$pg_db_for_ckan"


    #
    # Backup the original development.ini and install the modified one.
    #run_or_die mv $CKAN_ETC/default/development.ini $CKAN_ETC/default/development.ini.ORIG
    #run_or_die cp $TEMPDIR/development.ini $CKAN_ETC/default/development.ini

    #
    # Update some of the default parameter values
    #
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -k ckan.auth.create_unowned_dataset -v 'false'
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -k ckan.auth.create_dataset_if_not_in_organization -v 'false'
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -k ckan.auth.user_create_groups -v 'false'
    #run_or_die $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -k ckan.auth.user_create_organizations -v 'false'
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -k ckan.auth.user_delete_groups -v 'false'
    #run_or_die $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -k ckan.auth.user_delete_organizations -v 'false'
    ## TODO: Not sure whether to set ckan.auth.create_user_via_api as True???


    #
    # Step 5: Setup Solr
    # TODO
    # fill this in when on-line again
    #
    # Step 6: Create database tables
    pushd $APPS_SRC/ckan
    run_or_die $PYENV_DIR/bin/paster db init -c $CKAN_ETC/default/development.ini
    popd

    #
    #
    # Step 7: Set up the DataStore
    # TODO
    # fill this in when on-line again

    #
    #
    # Step 8: Link to who.ini
    # TODO
    # fix this in when on-line again
    run_or_die ln -s $APPS_SRC/ckan/who.ini $CKAN_ETC/default/who.ini #TODO what's the rest of this path?

    #
    #
    # Step 9: Run CKAN in the development web server
    # Run the dev server (without Apache httpd)
    pushd $APPS_SRC/ckan
    #run_or_die $PYENV_DIR/bin/paster serve $CKAN_ETC/default/development.ini
    popd

    #
    #
    # Step 10: Run the CKAN tests
    # TODO
    # See the Testing for Developers link    
}

#
# setup_datastore
#
# Sets up the datastore extension in CKAN.
# See http://docs.ckan.org/en/latest/datastore.html
function install_datastore() {
    #Setup Site URL
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -k ckan.site_url -v $site_url

    #Add the datastore plugin to the config file.
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -a -k ckan.plugins -v datastore 

    #Create users and databases
    echo "CREATE ROLE $pg_id_datastore ENCRYPTED PASSWORD '$pg_pw_datastore' NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN;" > $TEMPDIR/default_datastore_user.sql
    run_or_die sudo -u postgres psql -d postgres -f $TEMPDIR/default_datastore_user.sql
    run_or_die sudo -u postgres createdb -O $pg_id_for_ckan $pg_db_for_datastore -E utf-8

    #Update URLs
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -k ckan.datastore.write_url -v "postgresql://$pg_id_for_ckan:$pg_pw_for_ckan@localhost/$pg_db_for_datastore"    
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -k ckan.datastore.read_url -v "postgresql://$pg_id_datastore:$pg_pw_datastore@localhost/$pg_db_for_datastore"    

    #Set Permissions
    pushd $APPS_SRC/ckan
    run_or_die $PYENV_DIR/bin/paster datastore set-permissions postgres -c $CKAN_ETC/default/development.ini
    popd

    #Setup Filestore
    run_or_die sudo mkdir -p $FILESTORE_DIRECTORY

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -k ofs.impl -v pairtree
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -k ofs.storage_dir  -v $FILESTORE_DIRECTORY

    ##Set the permissions of the storage_dir. www-data is the Apache User which should have full access to this directory.
    run_or_die sudo chown www-data $FILESTORE_DIRECTORY
    run_or_die sudo chmod u+rwx $FILESTORE_DIRECTORY
}

#
# Setup Datastorer extension.
# Refer the installation instructions https://github.com/okfn/ckanext-datastorer
#
function install_datastorer() {

    run_or_die $PYENV_DIR/bin/pip install -e git+https://github.com/okfn/ckanext-datastorer.git#egg=ckanext-datastorer

    run_or_die $PYENV_DIR/bin/pip install -r $APPS_SRC/ckanext-datastorer/pip-requirements.txt

    #Add datastorer to the list of plugins.
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -a -k ckan.plugins -v datastorer

    run_or_die echo "Finished installing ckanext-datastorer."

    ##TODO: Need to check installing supervisor module as described in the installation instructions.
}

#
# Setup Postgis and spatial.
# Followed the URL : http://docs.ckan.org/projects/ckanext-spatial/en/latest/install.html
#

function install_postgis() {

    run_or_die apt-get -y install libxml2-dev
    run_or_die apt-get -y install libxslt1-dev
    run_or_die apt-get -y install libgeos-c1

    run_or_die sudo -u postgres psql -d $pg_db_for_ckan -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
    run_or_die sudo -u postgres psql -d $pg_db_for_ckan -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql

    echo "ALTER TABLE spatial_ref_sys OWNER TO $pg_id_for_ckan;" > $TEMPDIR/grants_on_template_postgis.sql    
    echo "ALTER TABLE geometry_columns OWNER TO $pg_id_for_ckan;" >> $TEMPDIR/grants_on_template_postgis.sql    

    run_or_die sudo -u postgres psql -d $pg_db_for_ckan -f $TEMPDIR/grants_on_template_postgis.sql

    # Download libxml and setup.
    wget ftp://xmlsoft.org/libxml2/libxml2-2.9.0.tar.gz -O $TEMPDIR/libxml.tar.gz
    pushd $TEMPDIR
    run_or_die tar zxvf libxml.tar.gz
    pushd libxml2-2.9.0
    libxmlso_file_loc=$(find /usr -name "libxml2.so" | head -1)
    libxmlso_path=${libxmlso_file_loc%/*}
    echo "libxml path : $libxmlso_path"
    run_or_die ./configure --libdir=$libxmlso_path
    echo $libxmlso_path
    run_or_die make
    run_or_die sudo make install
    popd
    popd        

    run_or_die xmllint --version

    echo "Finished installing postgis"
}


function install_ckanext_harvest() {

    run_or_die apt-get -y install rabbitmq-server

    run_or_die $PYENV_DIR/bin/pip install -e git+https://github.com/okfn/ckanext-harvest.git@release-v2.0#egg=ckanext-harvest

    run_or_die $PYENV_DIR/bin/pip install -r $APPS_SRC/ckanext-harvest/pip-requirements.txt

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -a -k ckan.plugins -v "harvest ckan_harvester"
 
    run_or_die $PYENV_DIR/bin/paster --plugin=ckanext-harvest harvester initdb -c $CKAN_ETC/default/development.ini
    #pasterr "--plugin=ckan sysadmin add harvest"    
    #TODO: Check whether user 'harvest' needs to be created. if so find how to pass the password as part of paster command.
}


function install_ckanext_spatial() {

    run_or_die $PYENV_DIR/bin/pip install -e git+https://github.com/okfn/ckanext-spatial.git#egg=ckanext-spatial

    run_or_die $PYENV_DIR/bin/pip install -r $APPS_SRC/ckanext-spatial/pip-requirements.txt

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -a -k ckan.plugins -v "spatial_metadata spatial_query"
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -k ckanext.spatial.search_backend -v "solr"

    run_or_die $PYENV_DIR/bin/paster --plugin=ckanext-spatial spatial initdb -c $CKAN_ETC/default/development.ini
}

function install_ckanext_importlib() {
    run_or_die $PYENV_DIR/bin/pip install -e git+https://github.com/okfn/ckanext-importlib.git#egg=ckanext-importlib
    yes i | $PYENV_DIR/bin/pip install -r $APPS_SRC/ckanext-importlib/pip-requirements.txt
}

function install_ngds() {

    install_gdal

    run_or_die $PYENV_DIR/bin/pip install -e git+https://$GIT_UNAME:$GIT_PWD@github.com/ngds/ckanext-ngds.git#egg=ckanext-ngds

    run_or_die $PYENV_DIR/bin/pip install -r $APPS_SRC/ckanext-ngds/pip-requirements.txt    

    configure_ngds   

    run_or_die sudo mv $CKAN_ETC/default/development.ini $CKAN_ETC/default/development.ini.bak
}

function install_gdal() {
    . $PYENV_DIR/bin/activate
    run_or_die sudo apt-get -y install python-software-properties
    run_or_die sudo apt-add-repository -y ppa:ubuntugis/ubuntugis-unstable
    run_or_die sudo apt-get update
    run_or_die sudo apt-get -y --force-yes install libgdal-dev gdal-bin

    run_or_die $PYENV_DIR/bin/pip install --no-install GDAL

    pushd $PYENV_DIR/build/GDAL
    $PYENV_DIR/bin/python  setup.py build_ext --include-dirs=/usr/include/gdal/

    run_or_die $PYENV_DIR/bin/pip install --no-download GDAL
    popd
}


function configure_ngds() {

    deployment_file=$CKAN_ETC/default/central.ini

    if [ "$deployment_type" = "node" ]
        then
            deployment_file=$CKAN_ETC/default/node.ini
    fi

    run_or_die sudo cp $CKAN_ETC/default/development.ini $deployment_file

    NGDS_CUSTOM_PATH=$CKAN_ETC/default/ngds
    NGDS_CONFIG_PATH=$NGDS_CUSTOM_PATH/config
    NGDS_SRC=$APPS_SRC/ckanext-ngds
    NGDS_CUSTOM_PUBLIC=$NGDS_CUSTOM_PATH/public

    $PYENV_DIR/bin/python $APPS_SRC/ckanext-ngds/scripts/ngds_config_file.py -f $deployment_file -d $deployment_type -r $NGDS_SRC

    #$PYENV_DIR/bin/python /home/ngds/install/configobjtest.py -f $deployment_file -d $deployment_type -r $NGDS_SRC


    #Move configuration files to the etc/default path.
    run_or_die sudo mkdir -p $NGDS_CUSTOM_PATH
    sudo chown -R $MYUSERID:$MYUSERID $NGDS_CUSTOM_PATH
    run_or_die sudo mkdir -p $NGDS_CONFIG_PATH
    run_or_die sudo mkdir -p $NGDS_CUSTOM_PUBLIC/assets


    run_or_die sudo cp $APPS_SRC/ckanext-ngds/facet-config.json $NGDS_CONFIG_PATH/
    run_or_die sudo cp $APPS_SRC/ckanext-ngds/contributors_config.json $NGDS_CONFIG_PATH/

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "solr_url" -v "http://127.0.0.1:8983/solr"

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "ngds.facets_config" -v "$NGDS_CONFIG_PATH/facet-config.json"
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "ngds.contributors_config" -v "$NGDS_CONFIG_PATH/contributors_config.json"

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "ngds.resources_dir" -v "$NGDS_SRC/ckanext/ngds/base/resources"

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "ckan.i18n_directory" -v "$NGDS_SRC"

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "extra_public_paths" -v "$NGDS_CUSTOM_PUBLIC"

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "ckan.locales_offered" -v "en es de"

    run_or_die sudo cp $NGDS_SRC/ckanext/ngds/ngdsui/public/assets/banner_image0.png $NGDS_CUSTOM_PUBLIC/assets/
    run_or_die sudo cp $NGDS_SRC/ckanext/ngds/ngdsui/public/assets/usgs.png $NGDS_CUSTOM_PUBLIC/assets/
    run_or_die sudo cp $NGDS_SRC/ckanext/ngds/ngdsui/public/assets/smu.png $NGDS_CUSTOM_PUBLIC/assets/
    run_or_die sudo cp $NGDS_SRC/ckanext/ngds/ngdsui/public/assets/boise.png $NGDS_CUSTOM_PUBLIC/assets/
    run_or_die sudo cp $NGDS_SRC/ckanext/ngds/ngdsui/public/assets/aasg.png $NGDS_CUSTOM_PUBLIC/assets/

    #$PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -a -k "ckan.plugins" -v "resource_proxy pdf_preview ngdsui metadata csw "

    if [ "$deployment_type" = "node" ]
        then
            BULKUPLOAD_DIRECTORY=$CKAN_LIB/bulkupload
            run_or_die sudo mkdir -p $BULKUPLOAD_DIRECTORY
            run_or_die sudo cp $APPS_SRC/ckanext-ngds/ckanclient.cfg $NGDS_CONFIG_PATH/
            $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k ngds.client_config_file -v "$NGDS_CONFIG_PATH/ckanclient.cfg"
            $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k ngds.bulk_upload_dir -v "$BULKUPLOAD_DIRECTORY/"
            
            #$PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -a -k "ckan.plugins" -v "geoserver"
            #TODO: How to update geoserver related parameters.
        else
            run_or_die sudo cp $APPS_SRC/ckanext-ngds/home_images.cfg $NGDS_CONFIG_PATH/
            $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k ngds.home_images_config_path -v "$NGDS_CONFIG_PATH/home_images.cfg"
            #$PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -a -k "ckan.plugins" -v "spatial_harvest_metadata_api csw_harvester"
    fi
    
    run_or_die $PYENV_DIR/bin/paster --plugin=ckanext-ngds ngds initdb -c $deployment_file

    $PYENV_DIR/bin/paster --plugin=ckan user add $ADMIN_NAME password=$ADMIN_PWD email=$ADMIN_EMAIL -c $deployment_file
    $PYENV_DIR/bin/paster --plugin=ckan sysadmin add $ADMIN_NAME -c $deployment_file 
}

function deploy_in_webserver() {
    
    #run_or_die cp $CKAN_ETC/default/central.ini $CKAN_ETC/default/production.ini
    run_or_die cp $deployment_file $CKAN_ETC/default/production.ini

    run_or_die apt-get -y install apache2 libapache2-mod-wsgi

    #run_or_die apt-get -y install postfix

    WSGI_SCRIPT=$CKAN_ETC/default/apache.wsgi

    create_wsgi_script > $WSGI_SCRIPT

    create_apache_config > /etc/apache2/sites-available/ckan_default

    run_or_die a2ensite ckan_default
    run_or_die service apache2 reload      
}

function create_wsgi_script() {
    
#WSGI_SCRIPT=$CKAN_ETC/default/apache.wsgi

cat <<EOF
import os
activate_this = os.path.join('$PYENV_DIR/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from paste.deploy import loadapp
config_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'production.ini')
from paste.script.util.logging_config import fileConfig
fileConfig(config_filepath)
application = loadapp('config:%s' % config_filepath)
EOF
}

function create_apache_config() {
    
#APACHE_CONFIG_FILE=/etc/apache2/sites-available/ckan_default

cat <<EOF
<VirtualHost 0.0.0.0:80>
    ServerName $SERVER_NAME
    ServerAlias $SERVER_NAME_ALIAS
    WSGIScriptAlias / $WSGI_SCRIPT

    # Pass authorization info on (needed for rest api).
    WSGIPassAuthorization On

    #TODO The following line should be removed.
    #WSGIRestrictStdout Off

    # Deploy as a daemon (avoids conflicts between CKAN instances).
    WSGIDaemonProcess ckan_default display-name=ckan_default processes=2 threads=15

    WSGIProcessGroup ckan_default

    ErrorLog /var/log/apache2/ckan_default.error.log
    CustomLog /var/log/apache2/ckan_default.custom.log combined
</VirtualHost>
EOF
}

function get_tomcat() {
    wget http://apache.openmirror.de/tomcat/tomcat-7/v7.0.42/bin/apache-tomcat-7.0.42.tar.gz -P $TEMPDIR
    pushd $TEMPDIR
    #pushd /home/ngds/install/download/
    tar -xvf apache-tomcat-7.0.42.tar.gz
    sudo mv apache-tomcat-7.0.42/ $CATALINA_HOME/
    popd
}

function get_solr() {
    wget http://www.apache.org/dist/lucene/solr/4.4.0/solr-4.4.0.tgz -P $TEMPDIR
    pushd $TEMPDIR
    tar -xzvf solr-4.4.0.tgz
    mkdir -p $SOLR_LIB/example/
    pushd solr-4.4.0/example
    cp -r solr $SOLR_LIB/example/
    cp lib/ext/*.jar $CATALINA_HOME/lib/
    popd
    popd    

    cp $TEMPDIR/solr-4.4.0/dist/solr-4.4.0.war $SOLR_LIB/example/solr/solr.war 
}

function setup_solr() {

mkdir $SOLR_CATALINA_BASE/conf $SOLR_CATALINA_BASE/logs $SOLR_CATALINA_BASE/temp $SOLR_CATALINA_BASE/webapps $SOLR_CATALINA_BASE/work
cp $CATALINA_HOME/conf/server.xml $SOLR_CATALINA_BASE/conf/server.xml.TEMPLATE
cat $SOLR_CATALINA_BASE/conf/server.xml.TEMPLATE | \
    sed "s|Server port=\"8005\"|Server port=\"8015\"|" | \
    sed "s|Connector port=\"8080\"|Connector port=\"8983\"|" > $SOLR_CATALINA_BASE/conf/server.xml

rm $SOLR_CATALINA_BASE/conf/server.xml.TEMPLATE

cp $CATALINA_HOME/conf/web.xml $SOLR_CATALINA_BASE/conf

#Download SOlr and extract its contents
get_solr

mkdir $SOLR_CATALINA_BASE/conf/Catalina
chmod 755 -R $SOLR_CATALINA_BASE/conf/Catalina
mkdir $SOLR_CATALINA_BASE/conf/Catalina/localhost

echo -e "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<Context docBase=\"$SOLR_LIB/example/solr/solr.war\" debug=\"0\" privileged=\"true\" allowLinking=\"true\" crossContext=\"true\">\n<Environment name=\"solr/home\" type=\"java.lang.String\" value=\"$SOLR_LIB/example/solr\" override=\"true\" />\n</Context>" | sudo tee -a $SOLR_CATALINA_BASE/conf/Catalina/localhost/solr.xml
mv $SOLR_LIB/example/solr/collection1/conf/schema.xml $SOLR_LIB/example/solr/collection1/conf/schema.xml.bak
cp $NGDS_SRC/installation/schema.xml $SOLR_LIB/example/solr/collection1/conf/schema.xml


create_solr_server_script

}

function create_solr_server_script() {

JAVA_HOME=/usr/lib/jvm/java-6-openjdk # your java
JRE_HOME=/usr/lib/jvm/java-6-openjdk/jre # your jre
CATALINA_BASE=$SOLR_CATALINA_BASE
SOLR_HOME=$SOLR_LIB/example/solr
cat > $NGDS_SCRIPTS/solr-server.sh <<EOF
#!/bin/bash

export JAVA_HOME=$JAVA_HOME
export JRE_HOME=$JRE_HOME
export CATALINA_HOME=$CATALINA_HOME
export CATALINA_BASE=$SOLR_CATALINA_BASE

export CATALINA_OPTS="-server -Xms22m -Xmx40m" 
export SOLR_HOME=$SOLR_HOME

export JAVA_OPTS="-Dsolr.data.dir=\$SOLR_HOME"
export JAVA_OPTS="\$JAVA_OPTS -Dsolr.solr.home=\$SOLR_HOME"
export JAVA_OPTS="\$JAVA_OPTS -Dlog4j.configuration=\$SOLR_HOME/log4j.properties"

PATH=\$PATH:\$JAVA_HOME:\$JRE_HOME:\$CATALINA_HOME/bin
export PATH    

$CATALINA_HOME/bin/catalina.sh "\$@"
EOF
sudo chmod 755 $NGDS_SCRIPTS/solr-server.sh
$NGDS_SCRIPTS/solr-server.sh start
}


function setup_geoserver() {

    mkdir $GEOSERVER_CATALINA_BASE/conf $GEOSERVER_CATALINA_BASE/logs $GEOSERVER_CATALINA_BASE/temp $GEOSERVER_CATALINA_BASE/webapps $GEOSERVER_CATALINA_BASE/work

    cp $CATALINA_HOME/conf/server.xml $GEOSERVER_CATALINA_BASE/conf/server.xml
    cp $CATALINA_HOME/conf/web.xml $GEOSERVER_CATALINA_BASE/conf

    run_or_die apt-get -y install unzip

    run_or_die wget http://sourceforge.net/projects/geoserver/files/GeoServer/2.4.0/geoserver-2.4.0-war.zip -P $TEMPDIR
    #run_or_die cp /home/ngds/Downloads/geoserver-2.4.0-war.zip $TEMPDIR
    pushd $TEMPDIR
    run_or_die unzip geoserver-2.4.0-war.zip -d geoserver
    pushd geoserver

    cp geoserver.war $GEOSERVER_CATALINA_BASE/webapps

    run_or_die unzip geoserver.war "data/*" -d $GEOSERVER_LIB
    popd
    popd    

    run_or_die create_geoserver_script
}

function create_geoserver_script() {

JAVA_HOME=/usr/lib/jvm/java-6-openjdk # your java
JRE_HOME=/usr/lib/jvm/java-6-openjdk/jre # your jre

cat > $NGDS_SCRIPTS/geoserver.sh <<EOF
#!/bin/bash

export JAVA_HOME=$JAVA_HOME
export JRE_HOME=$JRE_HOME
export CATALINA_HOME=$CATALINA_HOME
export CATALINA_BASE=$GEOSERVER_CATALINA_BASE
export GEOSERVER_DATA_DIR=$GEOSERVER_LIB/data
#export GEOSERVER_LOG_LOCATION=$GEOSERVER_LIB/data/logs/geoserver.log

export CATALINA_OPTS=" -server -Xms256m -Xmx512m "
export CATALINA_OPTS=" \$CATALINA_OPTS -DGEOSERVER_DATA_DIR=\$GEOSERVER_DATA_DIR "
#export CATALINA_OPTS=" \$CATALINA_OPTS -DGEOSERVER_LOG_LOCATION=\$GEOSERVER_LOG_LOCATION" 

PATH=\$PATH:\$JAVA_HOME:\$JRE_HOME:\$CATALINA_HOME/bin:\$GEOSERVER_DATA_DIR
export PATH    

$CATALINA_HOME/bin/catalina.sh "\$@"
EOF
sudo chmod 755 $NGDS_SCRIPTS/geoserver.sh
$NGDS_SCRIPTS/geoserver.sh start
}

function create_ngds_scripts() {

cat > $NGDS_SCRIPTS/ngds-celeryd.conf <<EOF
#!/bin/bash
start on runlevel [2345]
stop on runlevel [!2345]
respawn
exec $PYENV_DIR/bin/paster --plugin=ckan celeryd -c $CKAN_ETC/default/production.ini >>/var/log/apache2/ngds-celery.log 2>&1
EOF

sudo chmod 755 $NGDS_SCRIPTS/ngds-celeryd.conf
cp $NGDS_SCRIPTS/ngds-celeryd.conf /etc/init/
service ngds-celeryd start

}


function run1() {
    setup_env
    setup_geoserver
}


function run() {

    setup_env

    install_ckan

    # This is for updating server configuration file (developement.ini)
    run_or_die $PYENV_DIR/bin/pip install configobj

    install_datastore

    install_datastorer

    install_postgis

    install_ckanext_harvest

    install_ckanext_spatial

    install_ckanext_importlib    

    install_ngds

    deploy_in_webserver

    get_tomcat
    
    setup_solr

    setup_geoserver
    
    create_ngds_scripts
}



# # Process command-line arguments
# if [ $# -eq 0 ]; then {
#     print_help
#     exit 0
# }
# # Or enter interactive mode (not yet implemented)
# fi


# (See http://www.gnu.org/software/bash/manual/bashref.html#Shell-Builtin-Commands for getopts)
while getopts ":hf:g" opt; do
    case $opt in
        h)
            print_help
            exit 0
            ;;
        f)
            ngds_config_file=$OPTARG
            echo "Using config file $ngds_config_file" >&2
            ;;
        g)
            print_config_file
            exit 0
            ;;
        \?)
            echo "Invalid option: -$OPTARG.  Run '$this_script -h' for help." >&2
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument.  Run '$this_script -h' for help." >&2
            exit 1
            ;;
    esac
done

# Prepare the log file
timestamp=`date +%F_%H-%M`
LOGFILE="log_install-ngds-$timestamp.log"
echo "Writing log into file '$LOGFILE'"
echo "Log file generated by $this_script on $timestamp" > $LOGFILE
# TODO
# When run with sudo, whoami returns 'root'. Make sure this doesn't
# prevent future commands from going wrong.  If they do, determine
# a way to get the sudoing user's userid.
chown $MYUSERID:$MYUSERID $LOGFILE



run 2>&1 | tee ${LOGFILE}

function review_and_remove() {
    # Based on Ryan's https://github.com/ngds/dev-info/wiki/Ryan-Installs-ckanext-ngds
    echo "Inside review_and_remove"   

    #
    #
    # Create Databases
    # TODO
    # Try factoring these out into a separate script so that
    # we can call sudo once and run that script as postgres.
    # Also include the above DB commands run as postgres.
    # run_or_die sudo -u postgres createuser -S -D -R -P $pg_id_for_ckan
    # run_or_die sudo -u postgres createuser -s -P ckan_tester
    # run_or_die sudo -u postgres createuser -S -D -R -P datastore_reader
    # run_or_die sudo -u postgres createuser -S -D -R -P datastore_writer
    # run_or_die sudo -u postgres createuser -S -D -R -P datastore_test_reader
    # run_or_die sudo -u postgres createuser -S -d -R -P datastore_test_writer
    # run_or_die sudo -u createdb -E utf8 -O $pg_id_for_ckan -T template_postgis ckan_main
    # run_or_die sudo -u createdb -E utf8 -O ckan_tester -T template_postgis ckan_test
    # run_or_die sudo -u createdb -E utf8 -O datastore_writer -T template_postgis datastore
    # run_or_die sudo -u createdb -E utf8 -O datastore_test_writer -T template_postgis datastore_test    
}

#
# Clean up temporary directory
#run_or_die rm -rf $TEMPDIR

echo "Installation of NGDS is complete." | tee -a $LOGFILE
echo "To start the system ..."
echo "For more information about operating NGDS see the Operations Manual at:"
echo "https://github.com/ngds/dev-info/wiki/NGDS-v1.0-Operations-Guide"

exit

#
# Questions:
# 1. Need to create 'harvest' user??
# 2. Setting up supervisor conf for celery and harvest?
# 3. 
#
#
