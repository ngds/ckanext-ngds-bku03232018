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

from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-ngds',
	version=version,
	description="Extension for NGDS-related customizations",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='',
	author_email='',
	url='',
	license='',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext'],
	#package_data={'':['templates/*.*','templates/**/*.*','templates/**/**/*.*','public/**/*.*','public/**/**/**/*.*','public/**/**/**/**/*.*','public/**/**/**/**/**/**','public/**/**/*.*']},
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
    message_extractors = {
        'ckanext': [
            ('**.py', 'python', None),
            ('**.html', 'ckan', None),
        ]
    },		
	entry_points=
	"""
	[paste.paster_command]
    # Install NGDS additional tables
	ngds=ckanext.ngds.base.commands.ngds_tables:NgdsTables
	ngdsapi=ckanext.ngds.lib.command:APICommand

	[nose.plugins]
    pylons = pylons.test:PylonsPlugin

	[ckan.plugins]
	# CSW plugin
	csw=ckanext.ngds.csw.plugin:CswPlugin
	
    # NGDS Metadata plugin
	metadata=ckanext.ngds.metadata.plugin:MetadataPlugin
	
	# NGDS Harvest plugin
	ngds_harvester=ckanext.ngds.harvest.harvester.ngds:NgdsHarvester

	# NGDS UI plugin.
	ngdsui=ckanext.ngds.ngdsui.plugin:NgdsuiPlugin

	# Geoserver Plugin.
	geoserver=ckanext.ngds.geoserver.plugin:GeoserverPlugin
	
	# Content Model Management Plugin.
	contentmodel=ckanext.ngds.contentmodel.plugin:ContentModelPlugin
	
    [babel.extractors]
	    ckan = ckan.lib.extract:extract_ckan	
	""",
)
