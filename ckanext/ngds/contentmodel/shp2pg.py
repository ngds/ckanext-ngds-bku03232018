''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

__author__ = 'adriansonnenschein'

import sys
import ogr
import zipfile
import os
import json
import urllib2
import pylons
import re
import glob
from ckan.model.resource import Resource
from ckan.logic import (tuplize_dict, clean_dict, parse_params, flatten_to_string_key, get_action, check_access, NotAuthorized)
from ckan.lib.navl.dictization_functions import DataError, unflatten, validate
from ckan.lib.base import (request, render, BaseController, model, abort, h, g, c)

import logging
log = logging.getLogger(__name__)

class ZipfileHandler:
	"""Handles zipfiles."""

	zipfile = 'zipfile'

	def __init__(self, inputZip):
		if (zipfile.is_zipfile(inputZip)):
			self.zipfile = inputZip
			log.debug("Path is a .zip directory.")
		else:
			log.error("ERROR: Not a .zip file")
			sys.exit(1)

	def Unzip(self):
		unZippedDir = self.zipfile[:-4]+"_UNZIPPED"
		with zipfile.ZipFile(self.zipfile) as zf:
			log.debug("Extracting .zip directory")
			zf.extractall(unZippedDir)
			log.debug("Completed extracting .zip directory")

	def directoryCheck(self):
		valid = []
		invalid = []
		validMandatory = [".shp",".shx",".dbf"]
		validOptional = [".prj",".sbn",".sbx",".fbn",".fbx",".ain",".aih",".ixs",".mxs",".atx",".cpg"]
		with zipfile.ZipFile(self.zipfile) as zf:
			for info in zf.infolist():
				f = info.filename
				if os.path.splitext(f)[1] in validMandatory:
					valid.append(f)
					pass
				elif os.path.splitext(f)[1] in validOptional:
					pass
				elif f.endswith(".shp.xml"):
					pass
				else:
					invalid.append(f)
			if len(valid) != 3:
				log.error("ERROR: Missing a required filetype ('.shp', '.shx', '.dbf')-- ABORTING")
				sys.exit(1)
			if len(invalid) != 0:
				log.error("ERROR: One or more invalid filetype(s) were found in .zip directory-- ABORTING")
				sys.exit(1)
			else:
				log.debug("Shapefile is a valid dataset.")


class ShapefileToPostGIS:
	"""Handles the process of converting a shapefile to a PostGIS table."""

	allFields = []

	host = 'host'
	dbname = 'dbname'
	user = 'user'
	password = 'password'

	shapefile = 'shapefile'
	thisSchema = 'thisSchema'

	def __init__(self, path):
		writeurl = pylons.config.get('ckan.datastore.write_url', 'postgresql://ckanuser:password@localhost/datastore_db')
		self.host = re.search('@(.*)/', writeurl).group(1)
		self.dbname = re.search('(?=/[^/]*$).*', writeurl).group(0)[1:]
		self.user = re.search('://(.*):', writeurl).group(1)
		self.password = re.search('(?=:[^:]*$)(.*)@', writeurl).group(1)[1:]

		searchDir = path[:-4]+"_UNZIPPED"
		os.chdir(searchDir)
		for shp in glob.glob("*.shp"):
			self.shapefile = shp

		log.debug(self.shapefile)

	def fields(self, uri):
		url = "http://schemas.usgin.org/contentmodels.json"
		reader = urllib2.urlopen(url).read()
		data=json.loads(str(reader))
		fieldInfo = [version["field_info"] for version in data for version in version["versions"] if version["uri"] == uri]
		self.allFields = [rec["name"] for rec in fieldInfo for rec in rec if rec["name"] != "OBJECTID"]

		whichSchema = re.search('(?=[^/]*.\d).*$', uri).group(0)
		self.thisSchema = re.sub(r'([.//])', r'_', whichSchema)


	def shp2pg(self):
		inputDriver = ogr.GetDriverByName("ESRI Shapefile")
		dataSource = inputDriver.Open(self.shapefile, 0)
		sourceLayer = dataSource.GetLayerByIndex(0)
		sourceRecord = sourceLayer.GetNextFeature()
		layerDefn = sourceLayer.GetLayerDefn()
		outputDriver = ogr.GetDriverByName("PostgreSQL")
		outputDB = outputDriver.Open("PG: host=" + self.host + " port=5432 dbname=" + self.dbname +" user=" + self.user +" password=" + self.password)

		if outputDB is None:
			log.error("Could not open the database or GDAL is not correctly installed.")
			sys.exit(1)
		else:
			log.debug("Successfully connected to the database!")

		options = ["OVERWRITE=YES"]

		tableName = self.thisSchema.encode('utf-8')

		newLayer = outputDB.CreateLayer(tableName,sourceLayer.GetSpatialRef(),ogr.wkbUnknown,options)

		for i in range(layerDefn.GetFieldCount()):
			fieldName = sourceLayer.GetLayerDefn().GetFieldDefn(i).GetNameRef()
			fieldTypeInt = sourceLayer.GetLayerDefn().GetFieldDefn(i).GetType()
			for newField in self.allFields:
				if fieldName[:10] == newField[:10].lower():
					newLayer.CreateField(ogr.FieldDefn(str(newField), fieldTypeInt))
		newLayerDefn = newLayer.GetLayerDefn()
		x = 0
		while sourceRecord is not None:
			newFeature = ogr.Feature(newLayerDefn)
			newFeature.SetFrom(sourceRecord)
			newLayer.CreateFeature(newFeature)
			if x % 128 == 0:
				newLayer.CommitTransaction()
				newLayer.StartTransaction()
			sourceRecord = sourceLayer.GetNextFeature()
			x = x + 1
		newLayer.CommitTransaction()
		outputDB.Destroy()
