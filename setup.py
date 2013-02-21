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
	entry_points=\
	"""
	[paste.paster_command]
    # Install NGDS additional tables
	ngds=ckanext.ngds.base.commands.ngds_tables:NgdsTables
	
	[ckan.plugins]
	# CSW plugin
	csw=ckanext.ngds.csw.plugin:CswPlugin
	
    # NGDS Metadata plugin
	metadata=ckanext.ngds.metadata.plugin:MetadataPlugin
	
	# NGDS Harvest plugin
	ngdsharvest=ckanext.ngds.harvest.plugin:NgdsHarvestPlugin

	# NGDS UI plugin.
	ngdsui=ckanext.ngds.ngdsui.plugin:NgdsuiPlugin

    [babel.extractors]
	    ckan = ckan.lib.extract:extract_ckan	
	""",
)
