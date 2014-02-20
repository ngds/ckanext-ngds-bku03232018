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

    #Path where this instance will be installed

    #Path where application and data are installed.
    APPS=/opt/ngds/node

    #Tomcat Installation Path
    #CATALINA_HOME=/usr/share/tomcat
    CATALINA_HOME=$APPS/tomcat
    
    # Github Account Details
    # Only required if you also want to push software changes. Otherwise leave blank
    GIT_UNAME=
    GIT_PWD=

    ## The following properties can be left as it is for trying out this script.
    
    #CKAN Site URL
    site_url='http://sample.ckan.org'

    #Application Deployment setup(central|node).
    deployment_type="node"

    # CKAN DB username
    pg_id_for_ckan=node_ckan_default
    # CKAN DB password
    pg_pw_for_ckan=pass
    #CKAN DB name
    pg_db_for_ckan=node_ckan_default
    #Datastore DB Username
    pg_id_datastore=_node_datastore_default
    #Datastore DB pass
    pg_pw_datastore=pass
    #Datastore Database Name
    pg_db_for_datastore=node_datastore_default

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
    run_or_die $PYENV_DIR/bin/pip install -e 'git+https://github.com/okfn/ckan.git@ckan-2.0.1#egg=ckan'
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

    run_or_die $PYENV_DIR/bin/pip install -e git+https://github.com/okfn/ckanext-harvest.git@release-v2.0#egg=ckanext-harvest

    run_or_die $PYENV_DIR/bin/pip install -r $APPS_SRC/ckanext-harvest/pip-requirements.txt

    $PYENV_DIR/bin/python $CONFIG_UPDATER -f $CKAN_ETC/default/development.ini -a -k ckan.plugins -v "harvest ckan_harvester"

    run_or_die $PYENV_DIR/bin/paster --plugin=ckanext-harvest harvester initdb -c $CKAN_ETC/default/development.ini
    #pasterr "--plugin=ckan sysadmin add harvest"
    #TODO: Check whether user 'harvest' needs to be created. if so find how to pass the password as part of paster command.
}

# -------------------------------------------------------------------------------------------------
# install_ckanext_spatial
#
# Installs the spatial extension.
function install_ckanext_spatial() {

    run_or_die $PYENV_DIR/bin/pip install -e git+https://github.com/okfn/ckanext-spatial.git#egg=ckanext-spatial

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
# run
#
# This is the main function of the installer.  It calls the individual installer steps one after
# the other.
# For developers: You may outcomment steps while debugging the installer.
# 
function run() {

    setup_env

    install_ckan

    install_datastore

    install_datastorer

    install_postgis

    install_ckanext_harvest

    install_ckanext_spatial

    install_ckanext_importlib    

    install_ngds
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
echo "To start the system ..."
echo " - start tomcat: cd $CATALINA_HOME/bin ; ./catalina.sh run"
echo " - browse to: http://localhost"
echo " "
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
