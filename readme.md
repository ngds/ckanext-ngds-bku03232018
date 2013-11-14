# ckanext-ngds

This [CKAN extension](http://docs.ckan.org/en/ckan-2.0.3/extensions.html) contains a number of functions that build
intergration with the [National Geothermal Data System (NGDS)](http://geothermaldata.org/).

## Plugins

This extension provides a number of plugins, each of which encapsulates a different aspect of NGDS functionality:

- **ngdsui**: This plugin represents the core of ckanext-ngds functionality. It makes UI adjustments,
performs validation of NGDS-specific metadata fields, and provides integration with NGDS standard data models defined
 by http://schemas.usgin.org/models.

- **metadata**: Builds additional tables required by ckanext-ngds

- **csw**: Provides access to metadata through the [OGC CSW Protocol](http://www.opengeospatial.org/standards/cat), and maintains [ISO-19139](http://www.iso.org/iso/catalogue_detail.htm?csnumber=32557) metadata
documents that conform to the [USGIN profile](http://lab.usgin.org/sites/default/files/profile/file/u4/USGIN_ISO_Metadata_1.1.4.pdf).

- **ngds_harvester**: Provides a customized [CKAN Harvester](https://github
.com/okfn/ckanext-harvest#the-ckan-harvester) that translates between ISO-19139 documents and
[NGDS-specific CKAN Datasets](https://github.com/ngds/ckanext-ngds/wiki/The-NGDS-Package-and-Resource-Schema).

- **geoserver**: Integration with [Geoserver](http://geoserver.org), allowing uploaded CSV files and shapefiles to be
exposed as [WMS and WFS data services](http://opengeospatial.org).

## Extension Dependencies

This extension is dependent on other extensions provided by the [Open Knowledge Foundation](http://okfn.org).

- [ckanext-datastorer](https://github.com/okfn/ckanext-datastorer): On-the-fly conversion of uploaded tabular datasets
to database tables that can be accessed via [CKAN's Data API](http://docs.ckan.org/en/ckan-2.0.3/datastore-api.html).

- [ckanext-spatial](https://github.com/okfn/ckanext-spatial): Functionality that supports spatial metadata.

- [ckanext-harvest](https://github.com/okfn/ckanext-harvest): Support for harvesting metadata content from one CKAN
instance to another.

- [ckanext-importlib](https://github.com/okfn/ckanext-importlib): Supports bulk upload of datasets into CKAN.

## Fundamental Operating Modes

This extension is designed to run two different types of CKAN sites to serve two different purposes within the NGDS.
Depending on the operating mode, a different set of plugins need to be enabled. Some dependencies on external CKAN
extensions are required as well.

- **Node**: By default a site configured as a *Node*. In this configuration, the site's focus is similar to what we
usually think of a CKAN site as doing: An organization who wishes to provide geothermal information to the NGDS would
 use this mode. Members of the organization can upload files, create and maintain metadata records,
 and create [OGC data services]
 (http://opengeospatial.org) which conform to [NGDS standard data models](http://schemas.usgin.org/models).

    - NGDS Plugins: `metadata`, `csw`, `ngdsui`, `geoserver`
    - External Plugins: `datastorer` (ckanext-datastorer), `spatial_metadata` and `spatial_query` (ckanext-spatial)

- **Central**: In this situation the site's purpose is not to upload new datasets, or to generate new data services.
Rather, the site's purpose is to aggregate metadata from a number of *Nodes*, thus providing a single point from
which a search can be performed across a large number of *Nodes*.

    - NGDS Plugins: `metadata`, `csw`, `ngdsui`, `ngds_harvester`
    - External Plugins: `spatial_metadata`, `spatial_harvest_metadata_api`, and `spatial_query` (ckanext-spatial);
    `harvest` (ckanext-harvest)

## Installation

The installation of an entire CKAN system configured for ckanext-ngds on a clean,
Ubuntu 12.04 server can be accomplished using a [simple installation script]().

For users who wish to install ckanext-ngds alongside an existing CKAN system, or for developers interested in working
 with the code in this repository, [documentation is in progress]().
