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
	namespace_packages=['ckanext', 'ckanext.ngds','ckanext.ngds.ngdsui'],
	package_data={'':['templates/*.*','templates/**/*.*','public/**/*.*']},
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]	
	# NGDS UI plugin.
	ngdsui=ckanext.ngds.ngdsui.plugin:NgdsuiPlugin
	
	""",
)