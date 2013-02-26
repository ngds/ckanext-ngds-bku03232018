## Create additional NGDS tables

    paster --plugin=ckanext-ngds ngds initdb --config=/path/to/development.ini

## Metadata Content for ISO+USGIN Compliance
I've written this a comprehensive list of content required to generate a compliant USGIN-profile for ISO19139 XML doc. For each bit of content, I have:
- indicated where the content can be read from existing information collected by CKAN, if it exists
- specified a hard-coded value where appropriate for our application
- flagged **Additional Content** that must be added to the persistence layer
- specified default values for additional content where appropriate
- given suggestions for user-interface widgets when the user will have to specify additional information that is not collected in the default CKAN interface
- indicated how I intend to implement the persistence of any additional content
For hard-wired values, the user will not have to enter any content or be aware of its existence. Only those marked as **Additional Content** may require user-input.

### Information about the Metadata Record itself
The metadata record is the XML document that is created by our software

1. Unique ID: An identifier for the metadata record itself
    - `ckan.model.Package.id`
2. Language: What language is the metadata record itself written in?
    - `eng`
3. Character encoding: The character encoding for the metadata record itself.
    - `utf-8`
4. Contact: Who is responsible for creating/maintaining this metadata record?
    - **Additional content** -- a ResponsibleParty
    - Default value: nothing, must be selected by editor
    - *UI suggestion*: typeahead to choose existing ResponsibleParty or else a form to make a new one
    - Associated role hard-wired to `pointOfContact`
    - *Persistence via* correlation table between package and responsible_party
5. Updated date: When was the metadata record last updated?
    - `ckan.model.Package.metadata_modified`
6. Standard name: What profile of ISO does this metadata record use?
    - `ISO-NAP-USGIN`
7. Standard version: What version of the profile does this metadata record use?
    - `1.1.4`

### Information about the Dataset
The dataset is sort of the "intellectual work" that is being described. Contrast it to the "resources" that are files, journal articles, data services or other representations of the dataset.

1. URI: Any alternative identifier for the dataset. Could be an ISBN number or DOI
    - **Additional content**
    - Default value: `ckan.model.Package URL`
    - *UI suggestion*: optional input to enter a value, placeholder is the default value
    - *Persistence via* `ckan.model.Package.extras`
2. Category: A high-level category for the dataset
    - **Additional content**
    - Default value: `Dataset`
    - *UI-suggestion*: a combobox containing these options
        - TBD
    - *Persistence via* `ckan.model.Package.extras`
3. Title: The title of the dataset.
    - `ckan.model.Package.title`
4. Publication date: The date the dataset was published
    - **Additional content**
    - Default value: `ckan.model.Package.metadata_created`
    - *UI-suggestion*: optional date picker
    - *Persistence via* `ckan.model.Package.extras`
5. Creators: The folks who are credited with making the dataset. They might be authors, editors, etc.
    - **Additional content** -- a ResponsibleParty plus a "role"
    - Default value: nothing for the ResponsibleParty, which must be specifed. Role defaults to `author`
    - *Multiple values allowed*: a dataset commonly has more than one author
    - *UI-suggestion*: typeahead to choose existing ResponsibleParty or else a form to make a new one. Role picklist for each creator with the following options:
        - author
        - co-author
        - editor
        - contributor
    - *Persistence via* correlation table between package and responsible_party
6. Abstract: A long-text description of the dataset
    - `ckan.model.Package.notes`
7. Quality: A text string indicating the percieved quality of the dataset
    - **Additional Content**
    - Default value: none, optional
    - *UI-suggestion*: textbox for entering optional content
    - *Persistence via* `ckan.model.Package.extras`
7. Status: Some datasets are done while others are continually updated...
    - **Additional Content**
    - Default value: `completed`
    - *UI-suggestion*: a combobox with the following options:
        - completed
        - ongoing
        - deprecated
    - *Persistence via* `ckan.model.Package.extras`
8. Keywords: tags that describe the dataset themes
    - `ckan.model.Package.get_tags()`
9. Language: what language is the dataset written in?
    - **Additional Content**
    - Default value: `english`
    - *UI-suggestion*: a typeahead with all the langauges identified by that silly ISO standard
    - *Persistence via* `ckan.model.Package.extras`
10. Topic: categorize the dataset into a very specific ISO category
    - `geoscientificInformation`
11. Extent: *where* is the dataset about?
    - **Additional Content**
    - Default value: none, must be specified
    - *UI-suggestion*: user may either enter a Location keyword (e.g. "California" or "The Geysers") or use a map to draw a bounding geometry (point, box or arbitray polygon)
    - *Persistence via* `ckan.model.Package.extras`
12. Usage constraints: some information about any usage constraints
    - `ckan.model.Package.license_id`
    
### Information about *Online* Resources
Resources are the files or data services are uploaded or linked to. They are digital manifestations of the dataset. Each metadata record may provide access to multiple resources.

1. URL: What is the URL for the resource?
    - `ckan.model.Resource.url`
    - *Note*: For a data service, this URL should point at a self-descriptive document (OGC GetCapabilities or ESRI "REST" endpoint)
2. Name: A short description of the resource, commonly used as the text within an anchor tag in an HTML doc
    - `ckan.model.Resource.name`
3. Description: Longer text description of the resource
    - `ckan.model.Resource.description`
4. Distributor: Who is responsible for distribution of this resource?
    - **Additional Content** -- a ResponsibleParty
    - Default value: none, must be specified
    - *UI-suggestion*: typeahead to choose existing ResponsibleParty or else a form to make a new one.
    - Associated role hard-wired to `distributor`
    - *Persistence via* correlation table between resource and responsible_party
5. Protocol: For services, indicate what kind of data service this is
    - **Additional Content**
    - Default value: none, must be specified if linking to a data service
    - *UI-suggestion*: a combobox with the following options, only applicable to service links:
        - WMS
        - WFS
        - WCS
        - ESRI Map Service
    - *Persistence via* `ckan.model.Resource.extras` if possible
6. Layer: For services with multiple layers, indicate the name of the layer that corresponds to this dataset
    - **Additional Content**
    - Default value: none, optional
    - *UI-suggestion*: an input for the layer name, only applicable to service links 
    - *Persistence via* `ckan.model.Resource.extras` if possible
    
### Information about *Offline* Resources
Sometimes, people want to write metadata records for things that are only available to order, or view a phyical copy. These are "offline" resources.

1. Name: A short description of the resource, commonly used as the text within an <a> tag
    - `ckan.model.Resource.name`
2. Description: Longer text description of the resource
    - `ckan.model.Resource.description`
3. Distributor: Who is responsible for distribution of this resource?
    - **Additional Content** -- a ResponsibleParty
    - Default value: none, must be specified
    - *UI-suggestion*: typeahead to choose existing ResponsibleParty or else a form to make a new one.
    - Associated role hard-wired to `distributor`
    - *Persistence via* correlation table between resource and responsible_party
4. Format: Categorization of the types of things that might exist as offline resources
    - **Additional Content**
    - Default value: 
    - *UI-suggestion*: a combobox with the following options:
        - TBD
    - *Persistence via* `ckan.model.Resource.extras` if possible
5. Ordering procedure: text describing how to order something, if appropriate
    - **Additional Content**
    - Default value: none, optional
    - *UI-suggestion*: textbox
    - *Persistence via* `ckan.model.Resource.extras` if possible
    
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

