''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

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
	[ckan.celery_task]
	tasks = ckanext.ngds.contentmodel.celery_import:task_imports

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
