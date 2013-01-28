## Create additional NGDS tables

    paster --plugin=ckanext-ngds ngds initdb --config=/path/to/development.ini
    
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


