
# ckanext-ngds

This [CKAN extension](http://docs.ckan.org/en/ckan-2.0.3/extensions.html) contains a number of functions that build integration with the [National Geothermal Data System (NGDS)](http://geothermaldata.org/).

The National Geothermal Data System (NGDS) supports the storage and search of information resources relevant to the discovery, understanding, and utilization of geothermal energy. It is a network of data providers supplying data and metadata, with an aggregating feature that provides a single entry point for searching resources available through the system. 


## Fundamental Operating Modes

This extension is designed to run two different types of CKAN sites to serve two different purposes within the NGDS. Depending on the operating mode, a different set of plugins need to be enabled. Some dependencies on external CKAN extensions are required as well.

- **Publisher**: A node that is primarily used by a data provider to create metadata, make files avaialble for network access, deploy NGDS services to provide data access, or make metadata available for harvesting. Also refered to simply as __Node__.

    - NGDS Plugins: `metadata`, `csw`, `ngdsui`, `geoserver`
    - External Plugins: `datastorer` (ckanext-datastorer), `spatial_metadata` and `spatial_query` (ckanext-spatial)


- **Aggregator**: A node that is primarily used to collect metadata from NGDS publishing nodes (and possibly from other metadata sources), and provide search and data browsing services to help users find what they need, evaluate it, and get it for their application. Also called __Central__.

    - NGDS Plugins: `metadata`, `csw`, `ngdsui`, `ngds_harvester`, `geoserver`
    - External Plugins: `spatial_metadata`, `spatial_harvest_metadata_api`, `spatial_query` (ckanext-spatial), `csw_harvester`, `harvest`, `ckan_harvester`, `cswserver`, and `harvest` (ckanext-harvest)

## Plugins

This extension provides a number of plugins, each of which encapsulates a different aspect of NGDS functionality:

- **ngdsui**: This plugin represents the core of ckanext-ngds functionality. It makes UI adjustments, performs validation of NGDS-specific metadata fields, and provides integration with NGDS standard data models defined by http://schemas.usgin.org/models.
- **metadata**: Builds additional tables required by ckanext-ngds
- **csw**: Provides access to metadata through the [OGC CSW Protocol](http://www.opengeospatial.org/standards/cat), and maintains [ISO-19139](http://www.iso.org/iso/catalogue_detail.htm?csnumber=32557) metadata documents that conform to the [USGIN profile](http://lab.usgin.org/sites/default/files/profile/file/u4/USGIN_ISO_Metadata_1.1.4.pdf).
- **ngds_harvester**: Provides a customized [CKAN Harvester](https://github.com/okfn/ckanext-harvest#the-ckan-harvester) that translates between ISO-19139 documents and [NGDS-specific CKAN Datasets](https://github.com/ngds/ckanext-ngds/wiki/The-NGDS-Package-and-Resource-Schema).
- **geoserver**: Integration with [Geoserver](http://geoserver.org), allowing uploaded CSV files and shapefiles to be exposed as [WMS and WFS data services](http://opengeospatial.org).

## Extension Dependencies

This extension is dependent on other extensions provided by the [Open Knowledge Foundation](http://okfn.org).

- [ckanext-datastorer](https://github.com/okfn/ckanext-datastorer): On-the-fly conversion of uploaded tabular datasets
to database tables that can be accessed via [CKAN's Data API](http://docs.ckan.org/en/ckan-2.0.3/datastore-api.html).
- [ckanext-spatial](https://github.com/okfn/ckanext-spatial): Functionality that supports spatial metadata.
- [ckanext-harvest](https://github.com/okfn/ckanext-harvest): Support for harvesting metadata content from one CKAN
instance to another.
- [ckanext-importlib](https://github.com/okfn/ckanext-importlib): Supports bulk upload of datasets into CKAN.

## Installation

The installation of an entire CKAN system configured for ckanext-ngds on a clean,
Ubuntu 12.04 server can be accomplished using a simple installation script. See [here](https://github.com/ngds/install-and-run).

For users who wish to install ckanext-ngds alongside an existing CKAN system, or for developers interested in working with the code in this repository see [this wiki](https://github.com/ngds/ckanext-ngds/wiki).


### Run Tests

This extension has 2 subpackages (CLient and Sysadmin). However the instructions below, applied for both of them).

#### Step 1
Before running tests, there are 2 configs files for test, need to be configured regarding the test environment of your machine:
- ckanext-ngds/ckanext/ngds/client_or_sysadmin/test.ini: overrides ckan environment.ini variables or you can point it into a different environment.ini (e.g: use different database for test)
- ckanext-ngds/ckanext/ngds/client_or_sysadmin/tests/tests_config.cfg:
> ckan_host: by default, CKAN Host on your machine
> ckan_web_map_service_url: by default, webMapService (WmsServer service).
> ckan_ngds_sysadmin_search_path: by default, NGDS search URI
> ckan_ngds_client_paths: by default, array of ngds routes to pages (URIs)

#### Step 2
Command line to perform the tests:

```
$ cd ckanext-ngds/ckanext/ngds/client_or_sysadmin/
$ nosetests --ckan --with-pylons=test.ini tests/
```
- --with-pylons it's an option to specify the path to environment.ini to use for the test (override ckan default ini).
- tests/ it's the path to all tests files where located
