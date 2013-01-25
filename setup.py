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
	namespace_packages=['ckanext', 'ckanext.ngds'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
	[paste.paster_command]
	ngds=ckanext.ngds.base.commands.ngds_tables:NgdsTables
	
	[ckan.plugins]
	metadata=ckanext.ngds.metadata.plugin:MetadataPlugin
	""",
)
