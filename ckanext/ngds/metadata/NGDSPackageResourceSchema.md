This document describes the metadata associated with a CKAN package, which we (NGDS, USGIN) are thinking of as a repository object that may be compound, i.e. include more than one file as separate part files of the resource.  A repository object may have multiple distributions; in the case of a compound resource that would equate to different servers providing mirrored download access to the various part files. For datasets, the distributions might use different protocols, e.g. file download, WMS, WFS, OData, ESRI map service etc. The component parts and distributions are represented in CKAN-land as 'resources' (an unfortunate choice of language on their part...).

The NGDS extension puts additional requirements on the default CKAN Package and Resource schemas. These are extensions to CKAN's default Package and Resource schema, so fields that are covered in CKAN's Schema Definition are not included here. CKAN does not provide easy-to-find documentation of its internal schema. [An example of a complete representation as JSON is available](http://demo.ckan.org/api/3/action/package_show?id=adur_district_spending). A [JSON schema reverse-engineered from that example 'package'](https://raw.githubusercontent.com/usgin/json-metadata/master/CKAN-demo.jsonSchema.json) is also available. A compilation of metadata elements reverse engineered from JSON package objects from data.gov, the CKAN demo, and from NGDS is available in a [google spreadsheet](https://docs.google.com/spreadsheets/d/1JU0o9IDR6ebQEi1TNYjg2SttqaCtYmORPR7cNzHjzEY/edit#gid=1700091244). This spreadsheet has a rough mapping from the CKAN metadata keys to the [USGIN JSON metadata schema](https://github.com/usgin/json-metadata/blob/master/MetadataJSONschema.json).


## Packages

We require a set of "extras" to be defined for valid NGDS Packages.

- **agents**  In ISO metadata this corresponds to 'CI_ResponsibleParty'. An agent can play the role of author for a resource, contact for a distribution, curator of a resource, metadata originator, metadata steward, etc.  An agent may be a person or an organization; at least one of an e-mail address or telephone number is required to be provided to contact the agent. In some cases the agent may be deceased or no longer exist, in which case contact information is moot (but a resource contact should be provided). A person may be specified by name (e.g. Steve Richard) or by role (e..g. Metadata curator). A person might be affiliated with an organization. An organization might have multiple names, either hierarchical, acronyms, or synonyms (see examples below). A given agent may include more than one person, but they all must have the same organization affiliation (if that is specified) and contact information. If a particular agent role has several different people with different affiliations or contact information, these should be represented as separate agents. Persons or organizations might be identified using a URI; if this is available that is the best way to match instance data. [JSON schema for agent elements](https://github.com/usgin/json-metadata/blob/master/USGINAgentSchema.json) is avaialble.

Examples of agent objects:

simplest:

```
{
        "jmd:organizationName": ["USGS", "United States Geological Survey", "US Geological Survey"],
        "jmd:contactEmail": "someEmail@usgs.gov"
    }
    ``` 

More complex example:
```
{
        "jmd:agentRole": {
            "jmd:conceptPrefLabel": "compiler"
        },
        "jmd:individual": {
            "jmd:personURI": "usgin:personIdentifer",
            "jmd:personName": "Adrian Legg",
          },
        "jmd:organizationName": ["The Fabulous Company", "TFC"],
        "jmd:contactPhoneNumber": "520-888-0000",
        "jmd:contactEmail": "someEmail@fabulous.com"
    }
    ```

- **Agents of interest**

 - **authors**: Agent who created this dataset or publication? an array of Agent objects (see above) May be a person or an organization, and includes a role property on the relation specifying how the agent relates to the resource.
 - **Metadata maintainers**: Who is responsible for maintaining this metadata? A JSON array of agent objects as outlined above. This maps to ISO19115 metadata contact.  For harvested metadata, this is not necessarily the same as the node operator 
 - **Distributor**: who is responsible for maintenance of the online access to the resource; for services deployed on a node, it is the node operator, but for harvested metadata for resources hosted in other locations is is probably someone else.
 - **Resource steward**: who is responsible for maintenance of the resource; this will commonly be the author, but in many cases the originator of the resource is no longer involved and the steward is likely to be some organization with a position contact.


- **dataset_category**: The resource type; in addition to the CKAN resource types specified for the package 'type' property.  String. One of 
  - Catalog
  - Dataset
  - Desktop Application
  - Drawing
  - Map
  - Movie or Video
  - Photograph
  - Physical Artifact
  - Physical Collection
  - Remotely Sensed Image
  - Text Document
  - Web Application
- **dataset_lang**: The language the dataset is compiled in. String. See [the second column of this CSV file](https://github.com/ngds/ckanext-ngds/blob/master/ckanext/ngds/base/resources/db/iso6392_languages.csv) for a list of acceptable values. These are ISO 639-2 language codes that are classified as "living".

- **dataset_uri**: A unique identifier for this dataset. String
- **other_id**: other identifiers for dataset, 

- **lineage**: A description of history of the dataset, including references to source material. String. Maps to resourceLineage/lineageStatement in USGIN JSON metadata schema
- **quality**: A description of the how good the dataset is, including things like how recently it was updated, precision of quantitative measurements, etc. String. Maps to USGIN JSON metadata resourceQuality/qualityStatement with scope=dataset (the default).
- **spatial**: The spatial extent of the dataset or its relevance. This must be a String of [GeoJSON](http://geojson.org, ); This is from ckan/ckanext-spatial/. A bounding box is the expected specification of the footprint.
- **status**: Whether the dataset is finished, in progress or being updated. String. One of  `completed, ongoing, deprecated`

- **keywords**: keywords need to be scoped to a vocabulary using the VocabularyID key in the tag element in CKAN package; in addition a keywordType term is necessary to group keywords related to `place, temporal, thematic, ISO topic category`. Absence of a vocabularyID indicates free-form tags. ckan:VocabularyID maps to USGIN JSON metadata `resourceIndexTerms/keywordReference/referenceURI`.  Suggest putting tags in the CKAN tags element, and adding extension for scoped (type, reference) keywords for more precise scoping.

- **Dates**: 
Dates commonly need more specific scoping than field names imply; ISO metadata includes a date type property; the value can be inferred in some contexts, but in general a date should be associated with a type.

The CKAN package scheme includes these dates. Notes are NGDS interpretation of the content of these elements:

  - package/cache_last_updated :  This is internal to CKAN, NGDS doesn't care.
  - resource/created : create date for the metadata record
  - resource/last_modified : the date when this resource content was last modified  

USGIN/NGDS is interested in the following dates:
  - **publication_date**: The date on which the dataset was published. 'publication' is a pretty nebulous concept.  Date


## Resources

Resources in CKAN do not utilize the "extras" pattern, and so instead these are additional fields that a valid NGDS resource must provide.

### Additions required by all resources
- **distributor**: JSON object `{"name": "John Doe", "email": "john.doe@identifyme.com"}`
- **resource_format**: String. This indicates the "type" of resource we're dealing with. `structured, unstructured, offline, data-service`

### Fields required for any resources that involve uploaded files
- **format**: String. This is the format of an uploaded file, e.g. CSV, TXT, XLS.

### Content-model-aware file upload
- **content_model_uri**: String. Acceptable values defined by http://schemas.usgin.org/contentmodels.json
- **content_model_version**: String. Acceptable values defined by http://schemas.usgin.org/contentmodels.json

### Other file upload
- *no further additions*

### Linked data service
- **protocol**: String `OGC:WMS, OGC:WFS, OGC:WCS, OGC:CSW, OGC:SOS, OPeNDAP, ESRI, other`
- **layer**: String

### Offline
- **ordering_procedure**: String