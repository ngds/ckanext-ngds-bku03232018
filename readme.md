# New NGDS Metadata Tables

## Installation

Execute the following commands:
- fetch latest code from ckan (git fetch)
- activate the extension's code (python setpu.py develop)
- edit development.ini and add the following extensions= `ckan.plugins= stats datastore datawatch ngdsui metadata csw ngdsharvest`


## package_additional_metadata:

*Additional metadata information attached to a CKAN "package" or "dataset"*

Data fields:

- package_id: Foreign Key pointing at a CKAN "package". Primary Key field.
- author_id: Foreign Key to a responsible_party who created the dataset
- maintainer_id: Foreign Key to a responsible_party who is responsible for dataset maintenance
- pub_date: The date that the dataset was published
- resource_type: From USGIN-profile picklist

## resource_additional_metadata:

*Additional metadata information about a CKAN "resource", which is a link or uploaded file that is connected to a CKAN "package"*

Data Fields:

- resource_id: ForeignKey pointing at a CKAN "resource". Primary Key field.
- distributor_id: ForeignKey pointing at a responsible_party who distributes this file, or representation of the dataset

## responsible_party

*Table that is essentially a registry of people and their contact information.*

Data Fields:

- id: Integer Primary Key
- name: Person's full name
- organization: An organization name
- email: A person or organization's email address
- phone: A person or organization's phone number
- street: Street address
- state: State
- city: City
- zip: Zipcode

# New NGDS Harvesting Tables

## harvest_node

*Table in which each row represents some endpoint that we want to harvest from*

Data Fields:

- id: Integer Primary key
- url: The URL for the harvest endpoint
- title: A Title for the harvest node, for bookkeeping purposes.
- node_admin_id: Foreign Key to responsible party who runs the remote node
- frequency: How often we want to harvest from that endpoint. Should be one of `manual|daily|weekly|monthly`

## harvested_record

*Correlation table between a package generated through a harvest with the node it was harvested from. Also keeps the full XML text*

Data Fields:

- id: Integer Primary key
- package_id: Foreign Key to the package that was created through a harvesting mechanism
- harvest_node_id: Foreign Key to the harvest node that this resource was harvested from
- harvested_xml: Text dump of the XML file itself

# Paster `initdb` command

A paster function to create these tables in the database. Once `metadata` and `ngdsharvest` are added to the list of plugins in `development.ini`, tables can be created by issuing the following command:

    paster --plugin=ckanext-ngds ngds initdb --config=/path/to/development.ini

# HTTP API for CRUD-operations on additional tables.

Following the precedent set by CKAN's "Action API", this API functions by POST requests to a particular URL including JSON in the body. This runs an RPC-style function on the server and returns a JSON result.

## General form of required POST body:

    {
        "model": "The name of the model that will be affected",
        "process": "One of create|read|update|delete",
        "data": { ... JSON object representing the data to act on ... }
    }                   

## API Endpoints:
Metadata tables are adjusted at the URL: `/api/action/additional_metadata`

Harvest tables are adjusted at the URL: `/api/action/ngds_harvest`

## API examples:
### Create a ResponsibleParty

    {
        "model": "ResponsibleParty",
        "process": "create",
        "data": {
            "name": "Ryan Clark",
            "email": "ryan.clark@azgs.az.gov",
            "organization": "Arizona Geological Survey",
            "phone": "520-209-4139",
            "street": "416 W. Congress St. Ste. 100",
            "city": "Tucson",
            "state": "AZ",
            "zip": "85701"
        }
    }

### Read a ResponsibleParty

    {
        "model": "ResponsibleParty",
        "process": "read",
        "data": { "id": "4" }
    }

### Update a ResponsibleParty

    {
        "model": "ResponsibleParty",
        "process": "update",
        "data": {
            "id": "4",
            "email": "ryan.clark.j@gmail.com"
        }
    }


