from setuptools import setup, find_packages

version = '2.0.0'

setup(
    name='ckanext-ngds',
    version=version,
    description="Extensions for supporting the National Geothermal Data System",
    long_description='''\
    ''',
    classifiers=[],
    keywords='',
    author='Arizona Geological Survey',
    author_email='adrian.sonnenschein@azgs.az.gov',
    url='https://github.com/ngds/ckanext-ngds',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points=
    """
    [ckan.plugins]
    # NGDS Harvest plugin
    ngds_harvester=ckanext.ngds.harvest.harvester.ngds:NgdsHarvester

    # NGDS Admin plugin
    ngds_sysadmin=ckanext.ngds.sysadmin.plugin:SystemAdministrator

    # NGDS UI plugin
    ngds_client=ckanext.ngds.client.plugin:NGDSClient

    [paste.paster_command]
    ngds=ckanext.ngds.commands:NgdsCommand
    """,
)
