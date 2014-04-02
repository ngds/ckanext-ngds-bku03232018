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


# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
#
# Part I: Configuration
# +++++++++++++++++++++
#
# This part contains variables that can be configured by the user. For a first trial we recommend
# to keep the variables as they are.
#


# Edit this variable if you want to use a different linux user than 'ngds' to "own" the directory 
# containing the software distribution
MYUSERID=ngds


# -------------------------------------------------------------------------------------------------
# configure_properties
#
# Update this section to load required properties or path for NGDS Installation.
# This section can be moved outside this script later so that user doesn't need to 
# edit this script to file for the installation.
#
function configure_properties() {
    #Path where application and data are installed.
    APPS=/opt/ngds

    #Tomcat Installation Path
    #CATALINA_HOME=/usr/share/tomcat
    CATALINA_HOME=$APPS/tomcat
    
    # Github Account Details
    # Only required if you also want to push software changes. Otherwise leave blank
    GIT_UNAME=
    GIT_PWD=

    ## The following properties can be left as it is for trying out this script.
    
    #CKAN Site URL
    site_url='http://127.0.0.1'

    #Application Deployment setup(central|node).
    deployment_type="node"

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
    # PyCSW DB username
    pg_id_for_pycsw=ckan_default
    # PyCSW DB pass
    pg_pw_for_pycsw=pass
    #PyCSW Database Name
    pg_db_for_pycsw=pycsw_ckan_default

    #Application defult admin user for setup.
    ADMIN_NAME=admin
    ADMIN_PWD=admin
    ADMIN_EMAIL=temp_admin@admin.com

    #Server Name details for HTTP server to register with.
    SERVER_NAME=127.0.0.1
    SERVER_NAME_ALIAS=localhost    
}

# -------------------------------------------------------------------------------------------------
# DO NOT CHANGE VARIABLES below this point!
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# setup_env
#
# Does the following:
#  - Derives variables from the configuration variables
#  - Creates temporary installation folder
#  - creates the final installation folder and changes ownership
#

function setup_env() {

    configure_properties

    # Export Java path
    export JAVA_HOME="/usr/lib/jvm/java-6-oracle"

    # Absolute path to this script
    SCRIPT=$(readlink -f "$0")
    SCRIPTPATH=$(dirname "$SCRIPT")

    #Config file update script
    CONFIG_UPDATER=$SCRIPTPATH/update_config.py

    # Prepare temporary directory for downloads and the like
    TEMPDIR="tmp_install-ngds-$timestamp.tmp"
    run_or_die mkdir -p $TEMPDIR
    chown $MYUSERID:$MYUSERID $TEMPDIR

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

    # SOLR_CATALINA_BASE=$APPS_ETC/tomcat/solr
    SOLR_CATALINA_BASE=$APPS_ETC/XXX/solr
    SOLR_HOME=$APPS/solr

    GEOSERVER_CATALINA_BASE=$APPS_ETC/tomcat/geoserver

    SOLR_LIB=$APPS_LIB/solr
    GEOSERVER_LIB=$APPS_LIB/geoserver
    NGDS_SCRIPTS=$APPS/scripts

    # @cjk: to be removed. Not needed anymore
    sudo mkdir -p $SOLR_CATALINA_BASE
    sudo chown -R $MYUSERID:$MYUSERID  $SOLR_CATALINA_BASE

    sudo mkdir -p $SOLR_LIB $GEOSERVER_CATALINA_BASE $NGDS_SCRIPTS $GEOSERVER_LIB
    sudo chown -R $MYUSERID:$MYUSERID $SOLR_LIB $NGDS_SCRIPTS $GEOSERVER_LIB
    sudo chown -R $MYUSERID:$MYUSERID $GEOSERVER_CATALINA_BASE

    # User defined variables for email server:
    # SMTP server to connect to when sending emails
    # Ex: smtp.gmail.com:587
    SMTP_SERVER="undefined"

    # Whether or not to use STARTTLS when connecting to the SMTP server
    # Ex: True
    SMTP_STARTTLS="undefined"

    # Username used to authenticate with the SMTP server
    # Ex: your_username@gmail.com
    SMTP_USER="undefined"

    # Password used to authenticate with the SMTP server
    # Ex: your_password
    SMTP_PASSWORD="undefined"

    # Email address used by CKAN to send emails
    # Ex: user@gmail.com
    SMTP_MAIL_FROM="undefined"

    # Connection parameters for Geoserver, in the form:
    # "geoserver://{username}:{password}@{geoserver_rest_api_url}"
    GEOSERVER_REST_URL="geoserver://admin:geoserver@localhost:8080/geoserver/rest"
}

# -------------------------------------------------------------------------------------------------
# install_prereqs
#
# Install tools needed for this script to proceed (as opposed to
# tools specific to any given component that is being installed.)
# Note: We expect that a JDK is already installed and a JAVA_HOME
#       environment variable is set.
#       We recommend to use the Hotspot JDK and not OpenJDK.
#
function install_prereqs(){
    run_or_die sudo apt-get --assume-yes --quiet update
    run_or_die apt-get --assume-yes --quiet install build-essential
    run_or_die apt-get --assume-yes --quiet install unzip
}

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
#
# Part II: Helper Functions
# +++++++++++++++++++++++++
#
# This part contains helper functions to execute downloads, check completenes, etc.
#


# @cjk: To be deleted.
# -------------------------------------------------------------------------------------------------
#function check_downloads() {
#  for pkg in \
#      jetty-distribution-9.0.5.v20130815.tar.gz \
#      solr-4.4.0.tgz ;do
#    if [ ! -f $DOWLOADS/$pkg ] ;then
#      #mkdir -p $DOWLOADS
#      #scp -p ${DOWNLOAD}/${pkg} $DOWLOADS
#      echo "Please download $pkg distribution for the installation to proceed."
#      exit 0
#    fi
#  done
#}


# -------------------------------------------------------------------------------------------------
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

# -------------------------------------------------------------------------------------------------
# print_config_file
#
# This function is called when the script is started with the parameter -g
# It prints the configuration variables set for this installer.
#
# Otherwise the function is not used anywhere else.
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
pg_id_for_pycsw=$pg_id_for_pycsw
pg_pw_for_pycsw=$pg_pw_for_pycsw
pg_db_for_pycsw=$pg_db_for_pycsw

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


# -------------------------------------------------------------------------------------------------
# run_or_die
#
# This is an important helper function!
#
# Runs a command and returns if it succeeds; otherwise it exits with the
# failing command's return value.  Appropriate messages are written.
#
# Params: a command passed in as an unquoted string (exactly as it would be
#         typed on the command line)
#
# Example invocation: run_or_die apt-get install
#
# Assumptions: It is assumed that $LOGFILE is the path to a log file into which
#              to write log messages.
#
function run_or_die() {
    if [ -z $LOGFILE ]; then {
        LOGFILE="/dev/null"
    }
    fi
    echo -n "$this_script: running '$*': " | tee -a $LOGFILE
    # Execute the command and redirect both stdout and stderr to the LOGFILE
    $* &>>$LOGFILE
    # Using tee here causes $? to get the return value of tee, not that of
    # the command itself.
#    $* 2>>$LOGFILE #| tee -a $LOGFILE
    local ret=$?
    if [ $ret -ne 0 ]; then {
        echo "failed." | tee -a $LOGFILE 
        echo "$this_script: See the log file '$LOGFILE' to fix the issue and try again."
        exit $ret
    }
    else {
        echo "succeeded." | tee -a $LOGFILE
        return
    }
    fi
}


# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
#
# Part III: Installation of CKAN, and NGDS
# ++++++++++++++++++++++++++++++++++++++++
#
# This part contains the main functionality: It contains functions that install
# the main components of CKAN and NGDS.
#


# -------------------------------------------------------------------------------------------------
# install_ckan
# These steps (and the numbering indicated below) correspond to the
# instructions at http://docs.ckan.org/en/ckan-2.0/install-from-source.html
#
function install_ckan() {
    # Step 1: Install the required packages
    #run_or_die apt-get -y upgrade
    run_or_die apt-get --assume-yes --quiet install python-dev
    run_or_die apt-get --assume-yes --quiet install postgresql-9.1-postgis
    run_or_die apt-get --assume-yes --quiet install libpq-dev
    run_or_die apt-get --assume-yes --quiet install python-pip
    run_or_die apt-get --assume-yes --quiet install python-virtualenv
    run_or_die apt-get --assume-yes --quiet install git-core
    
    # We now install SOLR in a later step on tomcat. 
    # run_or_die apt-get --assume-yes --quiet install solr-jetty

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
    # Note to developers: The current method of tracking CKAN is to bind NGDS           
    # to a specific versioned GitHub URL of CKAN (as opposed to forking it.)            
    # See https://github.com/ngds/ckanext-ngds/issues/107  
    run_or_die $PYENV_DIR/bin/pip install -e 'git+https://github.com/okfn/ckan.git@ckan-2.0.4#egg=ckan'
    #
    # Step 2c
    # TODO
    # Before running this step, make sure pip-requirements.txt contains the full
    # set of requirements needed by NGDS.
    # TODO
    # Unfortunately pip install tends to crash from time to time. We need a way 
    # to execute the step repeatedly before giving up.

    run_or_die $PYENV_DIR/bin/pip install -r $APPS_SRC/ckan/pip-requirements.txt

    deactivate
    . $PYENV_DIR/bin/activate
    
    run_or_die $PYENV_DIR/bin/pip install configobj

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
    pushd $APPS_SRC/ckan > /dev/null
    run_or_die $PYENV_DIR/bin/paster make-config ckan $CKAN_ETC/default/development.ini
    popd > /dev/null
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
    # Ommitted because we set up SOLR later on top of tomcat
    #

    # Step 6: Create database tables
    pushd $APPS_SRC/ckan > /dev/null
    run_or_die $PYENV_DIR/bin/paster db init -c $CKAN_ETC/default/development.ini
    popd > /dev/null

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
    #pushd $APPS_SRC/ckan > /dev/null
    #run_or_die $PYENV_DIR/bin/paster serve $CKAN_ETC/default/development.ini
    #popd > /dev/null

    #
    #
    # Step 10: Run the CKAN tests
    # TODO
    # See the Testing for Developers link    
}

# -------------------------------------------------------------------------------------------------
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
    pushd $APPS_SRC/ckan > /dev/null
    run_or_die $PYENV_DIR/bin/paster datastore set-permissions postgres -c $CKAN_ETC/default/development.ini
    popd > /dev/null

    #Setup Filestore
    run_or_die sudo mkdir -p $FILESTORE_DIRECTORY

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -k ofs.impl -v pairtree
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -k ofs.storage_dir  -v $FILESTORE_DIRECTORY

    #Set the permissions of the storage_dir. www-data is the Apache User which should have full access to this directory.
    run_or_die sudo chown www-data $FILESTORE_DIRECTORY
    run_or_die sudo chmod u+rwx $FILESTORE_DIRECTORY
}


# -------------------------------------------------------------------------------------------------
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


# -------------------------------------------------------------------------------------------------
# Setup Postgis and spatial.
# Followed the URL : http://docs.ckan.org/projects/ckanext-spatial/en/latest/install.html
#
function install_postgis() {

    run_or_die apt-get --assume-yes --quiet install libxml2-dev
    run_or_die apt-get --assume-yes --quiet install libxslt1-dev
    run_or_die apt-get --assume-yes --quiet install libgeos-c1

    run_or_die sudo -u postgres psql -d $pg_db_for_ckan -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
    run_or_die sudo -u postgres psql -d $pg_db_for_ckan -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql

    echo "ALTER TABLE spatial_ref_sys OWNER TO $pg_id_for_ckan;" > $TEMPDIR/grants_on_template_postgis.sql    
    echo "ALTER TABLE geometry_columns OWNER TO $pg_id_for_ckan;" >> $TEMPDIR/grants_on_template_postgis.sql    

    run_or_die sudo -u postgres psql -d $pg_db_for_ckan -f $TEMPDIR/grants_on_template_postgis.sql

    run_or_die sudo -u postgres psql -d $pg_db_for_datastore -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
    run_or_die sudo -u postgres psql -d $pg_db_for_datastore -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql

    echo "ALTER TABLE spatial_ref_sys OWNER TO $pg_id_for_ckan;" > $TEMPDIR/grants_on_template_postgis.sql
    echo "ALTER TABLE geometry_columns OWNER TO $pg_id_for_ckan;" >> $TEMPDIR/grants_on_template_postgis.sql

    run_or_die sudo -u postgres psql -d $pg_db_for_datastore -f $TEMPDIR/grants_on_template_postgis.sql

    # Download libxml and setup.
    # run_or_die apt-get --assume-yes --quiet install make
    run_or_die wget --no-verbose ftp://xmlsoft.org/libxml2/libxml2-2.9.0.tar.gz --output-document $TEMPDIR/libxml.tar.gz
    pushd $TEMPDIR > /dev/null
    run_or_die tar zxf libxml.tar.gz
    pushd libxml2-2.9.0 > /dev/null
    libxmlso_file_loc=$(find /usr -name "libxml2.so" | head -1)
    libxmlso_path=${libxmlso_file_loc%/*}
    echo "libxml path : $libxmlso_path"
    run_or_die ./configure --libdir=$libxmlso_path
    echo $libxmlso_path
    run_or_die sudo make
    run_or_die sudo make install
    popd > /dev/null
    popd > /dev/null

    run_or_die xmllint --version

    echo "Finished installing postgis"
}


# -------------------------------------------------------------------------------------------------
# install_ckanext_harvest
#
# Installs all components required to harvest from a CSW source
#
function install_ckanext_harvest() {
    run_or_die apt-get --assume-yes --quiet install rabbitmq-server

    run_or_die $PYENV_DIR/bin/pip install -e git+https://github.com/okfn/ckanext-harvest.git@stable#egg=ckanext-harvest

    run_or_die $PYENV_DIR/bin/pip install -r $APPS_SRC/ckanext-harvest/pip-requirements.txt

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -a -k ckan.plugins -v "harvest ckan_harvester"
 
    run_or_die $PYENV_DIR/bin/paster --plugin=ckanext-harvest harvester initdb -c $CKAN_ETC/default/development.ini
}

# -------------------------------------------------------------------------------------------------
# install_ckanext_spatial
#
# Installs the spatial extension.
function install_ckanext_spatial() {

    run_or_die $PYENV_DIR/bin/pip install -e git+https://github.com/okfn/ckanext-spatial.git@stable#egg=ckanext-spatial

    run_or_die $PYENV_DIR/bin/pip install -r $APPS_SRC/ckanext-spatial/pip-requirements.txt

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -a -k ckan.plugins -v "spatial_metadata spatial_query"
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -k ckanext.spatial.search_backend -v "solr"

    run_or_die $PYENV_DIR/bin/paster --plugin=ckanext-spatial spatial initdb -c $CKAN_ETC/default/development.ini
}

# -------------------------------------------------------------------------------------------------
# install_ckanext_importlib
#
# Installs the import library.
function install_ckanext_importlib() {
    run_or_die $PYENV_DIR/bin/pip install -e git+https://github.com/okfn/ckanext-importlib.git#egg=ckanext-importlib
    yes i | $PYENV_DIR/bin/pip install -r $APPS_SRC/ckanext-importlib/pip-requirements.txt
}

# -------------------------------------------------------------------------------------------------
# install_ngds
#
# Installs the NGDS extension. This one requires the installation of GDAL.
function install_ngds() {

    install_gdal

    run_or_die $PYENV_DIR/bin/pip install -e git+https://$GIT_UNAME:$GIT_PWD@github.com/ngds/ckanext-ngds.git#egg=ckanext-ngds

    run_or_die $PYENV_DIR/bin/pip install -r $APPS_SRC/ckanext-ngds/pip-requirements.txt    

    configure_ngds   

    run_or_die sudo mv $CKAN_ETC/default/development.ini $CKAN_ETC/default/development.ini.bak
}



# -------------------------------------------------------------------------------------------------
# install_gdal
#
# We require the installation of a newer version of GDAL than what is installed by default for ubuntu 12.04LTS
# We therefore have to add an additional repository to apt-get.
# This part is tricky and can fail especially when working through a proxy.
# TODO:
# Long term solution: Download the GDAL source code and compile from scratch. Compile takes long but does 
# not require special packages to be present.
function install_gdal() {
    . $PYENV_DIR/bin/activate
    run_or_die sudo apt-get --assume-yes --quiet install python-software-properties
    run_or_die sudo apt-add-repository -y ppa:ubuntugis/ubuntugis-unstable
    run_or_die sudo apt-get update
    run_or_die sudo apt-get -y --force-yes install libgdal-dev gdal-bin

    run_or_die $PYENV_DIR/bin/pip install --no-install GDAL

    pushd $PYENV_DIR/build/GDAL > /dev/null
    $PYENV_DIR/bin/python  setup.py build_ext --include-dirs=/usr/include/gdal/

    run_or_die $PYENV_DIR/bin/pip install --no-download GDAL
    popd > /dev/null
}

# -------------------------------------------------------------------------------------------------
# configure_ngds
#
# This function configures the NGDS extension.
#  - create a production level CKAN ini file
#  - create the directory holding the ngds specific config files (e.g. facets.json)
#  - create the directory holding the NGDS specific assets (e.g. ngds png images)
#  - modify the SOLR configuration to CKAN ini file
#  - add the NGDS specific entries in the CKAN ini file
#  - create bulk upload directory if installed as a node
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

    # $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "solr_url" -v "http://127.0.0.1:8983/solr"
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "solr_url" -v "http://127.0.0.1:8080/solr"

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "ngds.facets_config" -v "$NGDS_CONFIG_PATH/facet-config.json"
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "ngds.contributors_config" -v "$NGDS_CONFIG_PATH/contributors_config.json"

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "ngds.resources_dir" -v "$NGDS_SRC/ckanext/ngds/base/resources"

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "ckan.i18n_directory" -v "$NGDS_SRC"

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "extra_public_paths" -v "$NGDS_CUSTOM_PUBLIC"

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "ckan.locales_offered" -v "en es de"

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "smtp.server" -v "$SMTP_SERVER"
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "smtp.starttls" -v "$SMTP_STARTTLS"
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "smtp.user" -v "$SMTP_USER"
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "smtp.password" -v "$SMTP_PASSWORD"
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "smtp.mail_from" -v "$SMTP_MAIL_FROM"

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $deployment_file -k "geoserver.rest_url" -v "$GEOSERVER_REST_URL"

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


# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
#
# Part IV: Install the production environment
# +++++++++++++++++++++++++++++++++++++++++++
#
# This part installs everything required for the production environment:
#  - apache2
#  - wsgi mod
#  - tomcat
#  - geoserver
#  - SOLR


# -------------------------------------------------------------------------------------------------
# deploy_in_webserver
#
# This function creates the production environment for CKAN. For details check this page:
# http://docs.ckan.org/en/ckan-2.0.1/deployment.html
#
function deploy_in_webserver() {
    
    #run_or_die cp $CKAN_ETC/default/central.ini $CKAN_ETC/default/production.ini
    run_or_die cp $deployment_file $CKAN_ETC/default/production.ini

    run_or_die apt-get --assume-yes --quiet install apache2 libapache2-mod-wsgi

    #run_or_die apt-get --assume-yes --quiet install postfix

    WSGI_SCRIPT=$CKAN_ETC/default/apache.wsgi

    PYCSW_WSGI_SCRIPT=$PYENV_DIR/src/pycsw/csw.wsgi

    create_ckan_wsgi_script > $WSGI_SCRIPT

    create_pycsw_wsgi_script > $PYCSW_WSGI_SCRIPT

    create_apache_config > /etc/apache2/sites-available/ckan_default

    run_or_die a2ensite ckan_default
    run_or_die service apache2 reload
}

# -------------------------------------------------------------------------------------------------
# create_ckan_wsgi_script
#
# Helper function to create the wsgi script for the installation via apache2 and the wsgi mod.
function create_ckan_wsgi_script() {
    
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

# -------------------------------------------------------------------------------------------------
# create_pycsw_wsgi_script
#
# Helper function to create a pycsw wsgi script for the installation via apache2 and the wsgi mod.
function create_pycsw_wsgi_script() {

#PYCSW_WSGI_SCRIPT=$PYENV_DIR/src/pycsw/csw.wsgi

cat <<EOF
from StringIO import StringIO
import os
import sys

activate_this = os.path.join('$PYENV_DIR/bin/activate_this.py')
execfile(activate_this, {"__file__":activate_this})

app_path = os.path.dirname(__file__)
sys.path.append(app_path)

from pycsw import server


def application(env, start_response):
    """WSGI wrapper"""
    config = 'default.cfg'

    if 'PYCSW_CONFIG' in env:
        config = env['PYCSW_CONFIG']

    if env['QUERY_STRING'].lower().find('config') != -1:
        for kvp in env['QUERY_STRING'].split('&'):
            if kvp.lower().find('config') != -1:
                config = kvp.split('=')[1]

    if not os.path.isabs(config):
        config = os.path.join(app_path, config)

    if 'HTTP_HOST' in env and ':' in env['HTTP_HOST']:
        env['HTTP_HOST'] = env['HTTP_HOST'].split(':')[0]

    env['local.app_root'] = app_path

    csw = server.Csw(config, env)

    gzip = False
    if ('HTTP_ACCEPT_ENCODING' in env and
            env['HTTP_ACCEPT_ENCODING'].find('gzip') != -1):
        # set for gzip compressed response
        gzip = True

    # set compression level
    if csw.config.has_option('server', 'gzip_compresslevel'):
        gzip_compresslevel = \
            int(csw.config.get('server', 'gzip_compresslevel'))
    else:
        gzip_compresslevel = 0

    contents = csw.dispatch_wsgi()

    headers = {}

    if gzip and gzip_compresslevel > 0:
        import gzip

        buf = StringIO()
        gzipfile = gzip.GzipFile(mode='wb', fileobj=buf,
                                 compresslevel=gzip_compresslevel)
        gzipfile.write(contents)
        gzipfile.close()

        contents = buf.getvalue()

        headers['Content-Encoding'] = 'gzip'

    headers['Content-Length'] = str(len(contents))
    headers['Content-Type'] = csw.contenttype

    status = '200 OK'
    start_response(status, headers.items())

    return [contents]

if __name__ == '__main__':  # run inline using WSGI reference implementation
    from wsgiref.simple_server import make_server
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    httpd = make_server('', port, application)
    print "Serving on port %d..." % port
    httpd.serve_forever()
EOF
}


# -------------------------------------------------------------------------------------------------
# create_apache_config
#
# Helper function that creates the apache configuration to serve CKAN via apache2.
function create_apache_config() {
    
#APACHE_CONFIG_FILE=/etc/apache2/sites-available/ckan_default

cat <<EOF
<VirtualHost 0.0.0.0:80>
    ServerName $SERVER_NAME
    ServerAlias $SERVER_NAME_ALIAS
    WSGIScriptAlias /csw $PYCSW_WSGI_SCRIPT
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

# -------------------------------------------------------------------------------------------------
# get_tomcat
#
# Helper function that downloads tomcat and installs it.
function get_tomcat() {
    run_or_die wget --no-verbose http://archive.apache.org/dist/tomcat/tomcat-7/v7.0.42/bin/apache-tomcat-7.0.42.tar.gz --directory-prefix $TEMPDIR
    pushd $TEMPDIR > /dev/null
    #pushd /home/ngds/install/download/
    tar -zxf apache-tomcat-7.0.42.tar.gz
    mv apache-tomcat-7.0.42/ $CATALINA_HOME/
    popd > /dev/null
}

# -------------------------------------------------------------------------------------------------
# get_solr
#
# Helper function that downloads SOLR, and unzips it. It also creates the SOLR home 
# directory (/opt/ngds/solr) and copies the contents of the example directory into 
# the SOLR home directory.
function get_solr() {
    run_or_die wget --no-verbose http://archive.apache.org/dist/lucene/solr/4.6.0/solr-4.6.0.tgz --directory-prefix $TEMPDIR
    pushd $TEMPDIR > /dev/null
    tar -zxf solr-4.6.0.tgz
    #mkdir -p $SOLR_LIB/example/
    pushd solr-4.6.0/example > /dev/null
    mkdir -p $SOLR_HOME
    cp -r solr/* $SOLR_HOME #$SOLR_LIB/example/
    mv $SOLR_HOME/solr.xml $SOLR_HOME/solr.xml.bak
    cp lib/ext/*.jar $CATALINA_HOME/lib/
    popd > /dev/null
    popd > /dev/null

    cp $TEMPDIR/solr-4.6.0/dist/solr-4.6.0.war $SOLR_HOME/solr.war 
}

# -------------------------------------------------------------------------------------------------
# deploy_solr
#
# This function deploys SOLR in tomcat
#  - download SOLr with previous helper function
#  - deploy SOLR in tomcat:
#     * create and put solr.xml into $CATALINA_HOME/conf/Catalina/localhost/
function setup_solr() {
    #Download Solr and extract its contents
    get_solr

    mkdir -p $CATALINA_HOME/conf/Catalina/localhost
    cat > $CATALINA_HOME/conf/Catalina/localhost/solr.xml <<ENDSOLRXML
<?xml version="1.0" encoding="utf-8"?>

<Context docBase="$SOLR_HOME/solr.war" debug="0" crossContext="true">
  <Environment name="solr/home" type="java.lang.String" value="$SOLR_HOME" override="true"/>
</Context>
ENDSOLRXML

    # backup original schema.xml
    mv $SOLR_HOME/collection1/conf/schema.xml $SOLR_HOME/collection1/conf/schema.xml.bak

    #TODO: wget the installation/schema.xml from git directly to avoid having
    # to install ckanext-ngds first.
    cp $APPS/bin/default/src/ckanext-ngds/installation/schema.xml $SOLR_HOME/collection1/conf/schema.xml
}

# -------------------------------------------------------------------------------------------------
# setup_geoserver
#
# This function downloads and unzips geoserver. It then takes the war file and places it 
# into tomcat's webapps folder.
function setup_geoserver() {
    run_or_die wget --no-verbose http://sourceforge.net/projects/geoserver/files/GeoServer/2.4.0/geoserver-2.4.0-war.zip --directory-prefix=$TEMPDIR
    pushd $TEMPDIR > /dev/null
    run_or_die unzip geoserver-2.4.0-war.zip -d geoserver
    pushd geoserver > /dev/null

    mv geoserver.war $CATALINA_HOME/webapps

    popd > /dev/null
    popd > /dev/null

    #run_or_die create_geoserver_script
}

# -------------------------------------------------------------------------------------------------
# create_geoserver_script
#
# This is dead code: We leave it in until the JAVA_OPTS and CATALINA_OPTS have been copied
#  into an appropriate place.
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


# -------------------------------------------------------------------------------------------------
# create_ngds__scripts
#
# this function creates the configuration to start celeryd via upstart.
# It creates a service called ngds-celeryd
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

# Upstart job for ckan harvester gather queue
cat > $NGDS_SCRIPTS/ckan-central-gather.conf <<EOF
#!/bin/bash
start on runlevel [2345]
stop on runlevel [!2345]
respawn
exec $PYENV_DIR/bin/paster --plugin=ckanext-harvest harvester gather_consumer --config=$CKAN_ETC/default/production.ini >> /var/log/ckan-central-gather.log 2>&1
EOF

sudo chmod 755 $NGDS_SCRIPTS/ckan-central-gather.conf
cp $NGDS_SCRIPTS/ckan-central-gather.conf /etc/init/
service ckan-central-gather start

# Upstart job for ckan harvester fetch queue
cat > $NGDS_SCRIPTS/ckan-central-fetch.conf <<EOF
#!/bin/bash
start on runlevel [2345]
stop on runlevel [!2345]
respawn
exec $PYENV_DIR/bin/paster --plugin=ckanext-harvest harvester fetch_consumer --config=$CKAN_ETC/default/production.ini >> /var/log/ckan-central-fetch.log 2>&1
EOF

sudo chmod 755 $NGDS_SCRIPTS/ckan-central-fetch.conf
cp $NGDS_SCRIPTS/ckan-central-fetch.conf /etc/init/
service ckan-central-fetch start

# Upstart job for ckan harvester fetch queue
cat > $NGDS_SCRIPTS/ckan-central-run-harvest.conf <<EOF
#!/bin/bash
start on runlevel [2345]
stop on runlevel [!2345]
respawn
exec $PYENV_DIR/bin/paster --plugin=ckanext-harvest harvester run --config=$CKAN_ETC/default/production.ini >> /var/log/ckan-central-run-harvest.log 2>&1
EOF

sudo chmod 755 $NGDS_SCRIPTS/ckan-central-run-harvest.conf
cp $NGDS_SCRIPTS/ckan-central-run-harvest.conf /etc/init/
service ckan-central-run-harvest start

# Upstart job for tomcat
cat > $NGDS_SCRIPTS/ckan-tomcat.conf <<EOF
#!/bin/bash
start on runlevel [2345]
stop on runlevel [!2345]
respawn
script
    export JAVA_OPTS="-Dfile.encoding=UTF-8 -server -Xms512m -Xmx2048m -XX:NewSize=256m -XX:MaxNewSize=256m -XX:PermSize=256m -XX:MaxPermSize=512m -XX:+DisableExplicitGC"
    chdir /opt/ngds/tomcat/bin/
    exec ./catalina.sh run >> /var/log/ckan-tomcat.log 2>&1
end script
EOF

sudo chmod 755 $NGDS_SCRIPTS/ckan-tomcat.conf
cp $NGDS_SCRIPTS/ckan-tomcat.conf /etc/init/
service ckan-tomcat start

# Upstart job for starting PyCSW server
cat > $NGDS_SCRIPTS/ckan-pycsw-server.conf <<EOF
#!/bin/bash
start on runlevel [2345]
stop on runlevel [!2345]
respawn
exec $PYENV_DIR/bin/python /opt/ngds/bin/default/src/pycsw/csw.wsgi >> /var/log/ckan-pycsw-server.log 2>&1
EOF

sudo chmod 755 $NGDS_SCRIPTS/ckan-pycsw-server.conf
cp $NGDS_SCRIPTS/ckan-pycsw-server.conf /etc/init/
service ckan-pycsw-server start

# Upstart job for loading data into PyCSW
cat > $NGDS_SCRIPTS/ckan-pycsw-loader.conf <<EOF
#!/bin/bash
start on runlevel [2345]
stop on runlevel [!2345]
respawn
exec $PYENV_DIR/bin/paster --plugin=ckanext-spatial ckan-pycsw load -p $PRODUCTION_PYCSW_CONFIG >> /var/log/ckan-pycsw-loader.log 2>&1
post-stop exec sleep 3600
EOF

sudo chmod 755 $NGDS_SCRIPTS/ckan-pycsw-loader.conf
cp $NGDS_SCRIPTS/ckan-pycsw-loader.conf /etc/init/
service ckan-pycsw-loader start
}

# -------------------------------------------------------------------------------------------------
# Create 'public' organization

function create_public_organization() {
    curl -b /tmp/cookies.txt -c /tmp/cookies.txt --data "login=admin&password=admin" http://localhost/en/login_generic
    curl -b /tmp/cookies.txt -c /tmp/cookies.txt --data "title=public&name=public&description=&image_url=&save" http://localhost/organization/new
    rm /tmp/cookies.txt
}

# -------------------------------------------------------------------------------------------------
# Fix permissions in /opt/ngds

function set_permissions() {
    sudo chown -R $MYUSERID.$MYUSERID /opt/ngds

    # Need to make sure Apache user has write permissions to filestore
    sudo chmod ug+rw /opt/ngds/lib/ckan/default
    sudo chown -R www-data.www-data /opt/ngds/lib/ckan/default
}

# -------------------------------------------------------------------------------------------------
# Check and warn on invalid Ubuntu release

function check_release() {
    . /etc/lsb-release
    if [ $DISTRIB_RELEASE != "12.04" ] || [ $DISTRIB_RELEASE != "12.10" ]
        then
            echo "This system is not running Ubuntu 12.04 or Ubuntu 12.10.  This installation may work, but it is untested."
    fi
}

# -------------------------------------------------------------------------------------------------
# Install Java

function install_java() {
    sudo apt-get -y update
    sudo apt-get -y upgrade
    sudo apt-get -y purge openjdk*
    sudo apt-get -y install software-properties-common python-software-properties git git-core
    sudo add-apt-repository -y ppa:webupd8team/java
    sudo apt-get -y update
    sudo apt-get install curl
    sudo apt-get -y install oracle-java6-installer
}

# -------------------------------------------------------------------------------------------------
# Install CSW Server

function install_csw_server() {
    # Install PyCSW v1.8.0
    run_or_die $PYENV_DIR/bin/pip install -e git+https://github.com/geopython/pycsw.git@1.8.0#egg=pycsw
    # Build database for PyCSW in PostgreSQL
    run_or_die sudo -u postgres createdb -O $pg_id_for_pycsw $pg_db_for_pycsw -E utf-8

    # Make PyCSW configuration file
    run_or_die cp $PYENV_DIR/src/pycsw/default-sample.cfg $PYENV_DIR/src/pycsw/default.cfg

    CSW_SERVER_HOME=$PYENV_DIR/src/pycsw
    CSW_DB_PARAMS=postgresql://$pg_id_for_pycsw:$pg_pw_for_pycsw@localhost/$pg_db_for_pycsw
    PYCSW_CONFIG=$PYENV_DIR/src/pycsw/default.cfg
    PYCSW_URL=$site_url/csw

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $PYCSW_CONFIG -s "server" -k "home" -v "$CSW_SERVER_HOME"
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $PYCSW_CONFIG -s "repository" -k "database" -v "$CSW_DB_PARAMS"
    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $PYCSW_CONFIG -s "server" -k "url" -v "$PYCSW_URL"

    run_or_die ln -s $PYENV_DIR/src/pycsw/default.cfg $CKAN_ETC/default/pycsw.cfg

    PRODUCTION_PYCSW_CONFIG=$CKAN_ETC/default/pycsw.cfg

    # Build tables in PyCSW database
    cd $PYENV_DIR/src/ckanext-spatial
    run_or_die $PYENV_DIR/bin/paster --plugin=ckanext-spatial ckan-pycsw setup -p $PYCSW_CONFIG

    # Move PyCSW WSGI script out of the way so that 'create_pycsw_wsgi_script()' can make custom one
    run_or_die mv $PYENV_DIR/src/pycsw/csw.wsgi $PYENV_DIR/src/pycsw/csw.wsgi.bak
}

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
#
# Part V: Run the script
# ++++++++++++++++++++++
#
# This part calls the individual installer functions in the correct order.
# It also provides a helper to process command line options




# -------------------------------------------------------------------------------------------------
# run
#
# This is the main function of the installer.  It calls the individual installer steps one after
# the other.
# For developers: You may comment out steps while debugging the installer.
#

function run() {

    check_release

    sudo apt-get -y upgrade

    install_java

    install_prereqs

    setup_env

    install_ckan

    install_datastore

    install_datastorer

    install_postgis

    install_ckanext_harvest

    install_ckanext_spatial

    install_ckanext_importlib    

    install_ngds

    install_csw_server

    deploy_in_webserver

    get_tomcat
    
    setup_solr

    setup_geoserver
    
    create_ngds_scripts

    set_permissions

    run_or_die a2dissite default

    run_or_die service apache2 reload

    create_public_organization
}


# -------------------------------------------------------------------------------------------------
# # Process command-line arguments

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

# -------------------------------------------------------------------------------------------------
# Prepare the log file
# Absolute path to this script
SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
timestamp=`date +%F_%H-%M`
LOGFILE="$SCRIPTPATH/log_install-ngds-$timestamp.log"
echo "Writing log into file '$LOGFILE'"
echo "Log file generated by $this_script on $timestamp" > $LOGFILE
# TODO
# When run with sudo, whoami returns 'root'. Make sure this doesn't
# prevent future commands from going wrong.  If they do, determine
# a way to get the sudoing user's userid.
chown $MYUSERID:$MYUSERID $LOGFILE


# -------------------------------------------------------------------------------------------------
# Execute the run function

# run_tmp 2>&1 | tee ${LOGFILE}
run 2>&1 | tee ${LOGFILE}

# -------------------------------------------------------------------------------------------------
# Clean up temporary directory and final message of success.

#run_or_die rm -rf $TEMPDIR

echo "Installation of NGDS is complete." | tee -a $LOGFILE
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
