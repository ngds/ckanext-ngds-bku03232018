""" NGDS_HEADER_BEGIN

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey

Please refer the the README.txt file in the base directory of the NGDS project:
https://github.com/ngds/ckanext-ngds/blob/master/README.txt

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero
General Public License as published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.  https://github.com/ngds/ckanext-ngds
ngds/blob/master/LICENSE.md or
http://www.gnu.org/licenses/agpl.html

NGDS_HEADER_END """

#! /usr/bin/env python

#  Hey! This sucks, doesn't it?
import sys, os, subprocess, re
import ConfigParser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

paths = os.environ["PATH"].split(os.pathsep)
paths.append("/usr/local/bin")

# Find nosetests
for p in paths:
    nosetests = os.path.join(p, "nosetests")
    if os.path.exists(nosetests):
        break

# Find the config file and learn about DB connections
config = [arg.split("=")[1] for arg in sys.argv if arg.split("=")[0] == "--with-pylons"]
if len(config) == 0:
    print "You must specify the path to your .ini file with --with-pylons=/path/to/file.ini"
    sys.exit(1)

# A log file, just in case we need it
#with open("your-last-test.log", "w+") as log:
# Make sure that database is all set up
parser = ConfigParser.RawConfigParser()
parser.read(config[0])
db_url = parser.get("app:main", "sqlalchemy.url")
pattern = "://(?P<user>.+?):(?P<pass>.+?)@(?P<host>.+?)(:(?P<port>\d+))?/(?P<database>.+)$"
details = re.search(pattern, db_url)

print "Starting call for database connection"
# Connection to the database engine
conn = (details.group("user"), details.group("pass"), details.group("host"), details.group("port") or "5432")
Session = sessionmaker(bind=create_engine("postgresql://%s:%s@%s:%s/postgres" % conn))
base_session = Session(autocommit=True)

# Drop the database if it is there.
base_session.connection().connection.set_isolation_level(0)
try:
    base_session.execute("DROP DATABASE %s;" % details.group("database"))
    print "DROPPED DATABASE %s" % details.group("database")
except ProgrammingError:
    pass
base_session.connection().connection.set_isolation_level(1)

# Recreate the database
base_session.connection().connection.set_isolation_level(0)
try:
    base_session.execute("CREATE DATABASE %s;" % details.group("database"))
    print "CREATED DATABASE %s" % details.group("database")
except Exception as ex:
    print "Exception while trying to create database: %s" % ex.orig
    raise ex
    sys.exit(1)
base_session.connection().connection.set_isolation_level(1)

# Connect to the new database
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session(autocommit=True)

# Create PostGIS tables
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "postgis.sql"), "r") as pg:
    session.execute(pg.read())
print "Executed postgis sql"
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "spatial_ref_sys.sql")) as sr:
    session.execute(sr.read())
print "Executed spatial sql"
session.close()

#print "GEOMETRY_COLUMNS EXISTS: %s" % str(engine.dialect.has_table(engine.connect(), "geometry_columns"))
#print "SPATIAL_REF_SYS EXISTS: %s" % str(engine.dialect.has_table(engine.connect(), "spatial_ref_sys"))

# Building arguments
args = [ nosetests ]
args = args + sys.argv[1:]
args.append("--nologcapture")

# Run nosetests
p = subprocess.Popen(args)
p.wait()

"""
# Drop the database
base_session.connection().connection.set_isolation_level(0)
try:
    base_session.execute("DROP DATABASE %s;" % details.group("database"))
except ProgrammingError:
    pass
base_session.connection().connection.set_isolation_level(1)
base_session.close()
"""
