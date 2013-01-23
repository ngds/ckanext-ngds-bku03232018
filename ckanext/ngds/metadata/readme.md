## Create additional metadata tables

    paster --plugin=ckanext-ngds metadata initdb --config=/path/to/development.ini
    
### How it works
`setup.py` defines an entry point as:

    [paste.paster_command]
    metadata=ckanext.ngds.metadata.commands.metadata:Metadata
    
`ckanext.ngds.metadata.commands.metadata:Metadata` inherits from `ckan.lib.cli:CkanCommand`. The `initdb` function essentially calls on `ckanext.ngds.metadata.model.additional_metadata.db_setup` to set up the tables.

`ckanext.ngds.metadata.model.additional_metadata` does a number of things:

- defines an `AdditionalMetadata` class that inherits from `ckan.model.domain_object:DomainObject`, and defines two more functions on top of it
- defines three classes for additional metadata content, which inherit from `AdditionalMetadata` and add custom attributes
- defines a function that creates SQLAlchemy table definitions, and sets up a mapping between those tables and the classes defined above
- defines a function that creates tables in PostgreSQL based on those SQLAlchemy table definitions
    
## API for CRUD operations on additional tables

The API follows the standards of [CKAN's Action API](http://docs.ckan.org/en/latest/apiv3.html#action-api). JSON objects are POSTed to a URL to perform RPC-style processes.

POST to `/api/action/additional_metadata`

The POST headers should specify `Content-type: application/json`, and the body should resemble this:

    {
        "process": "create"|"read"|"update"|"delete",
        "model": "ResponsibleParty"|"AdditionalPackageMetadata"|"AdditionalResourceMetadata",
        "data": { ... object representing one of these three models ... }
    }

For example, to create a new ResponsibleParty:

    {
        "process": "create",
        "model": "ResponsibleParty",
        "data" : {
            "name": "Ryan Clark",
            "email": "ryan.clark@azgs.az.gov",
            "phone": "520-209-4139",
            "street": "416 W. Congress St. Ste. 100",
            "city": "Tucson",
            "state": "AZ",
            "zip": "85719"
        }
    }

### How it works

`setup.py` defines an entry point as:

    [ckan.plugins]
    metadata=ckanext.ngds.metadata.plugin:MetadataPlugin
    
The `MetadataPlugin` implements two plugin interfaces:

- IConfigurer: Allows me an entry point that is hit whenever CKAN is run. Makes a call to `ckanext.ngds.metadata.model.additional_metadata.define_tables()`, which puts additional metadata classes and their mapping to database tables into memory
- IAction: Defines an API endpoint that accepts JSON data in a POST body at a given URL. This one works as described above. `/api/action/additional_metadata` is mapped to `ckanext.ngds.metadata.controllers.additional_metadata.dispatch()`

That `dispatch` function is given two things: `context`, which is a bunch of "global" variables about the environment, and `data_dict`, which is the POST body as a Python dict.

`ckanext.ngds.metadata.controllers.addtional_metadata` defines an `AdditionalMetadataController`, which is a base-class for table-specific controllers. It is super reusable and could probably be called a "CrudController" in a more generic sense. 


