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

version = '2.0.0a'

setup(
	name='ckanext-ngds',
	version=version,
	description="Extensions for supporting the National Geothermal Data System",
	long_description='''\
	''',
	classifiers=[],
	keywords='',
	author='Arizona Geological Survey',
	author_email='',
	url='http://geothermaldata.org',
	license='MIT',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext'],
    include_package_data=True,
	zip_safe=False,
	install_requires=[],
    entry_points=
	"""
	[ckan.plugins]
    # NGDS Metadata plugin
	ngds_metadata=ckanext.ngds.metadata.plugin:MetadataPlugin

	# NGDS Harvest plugin
	ngds_harvester=ckanext.ngds.harvest.harvester.ngds:NgdsHarvester

	# NGDS UI plugin.
	ngds_client=ckanext.ngds.client.plugin:NGDSClient

	# NGDS System Admin plugin
	sysadmin=ckanext.ngds.sysadmin.plugin:NGDSSystemAdmin

	[paste.paster_command]
    # Install NGDS additional tables
	ngds=ckanext.ngds.base.commands.ngds_tables:NgdsTables
	ngdsapi=ckanext.ngds.lib.command:APICommand
	""",
)
