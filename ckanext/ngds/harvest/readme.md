## How does ISO Metadata get served?
1. A native CKAN **Package** is saved or updated. This triggers an `IDomainModification.notify` plugin function to execute.
2. An **IsoPackage** is created from the **Package** through a simple initialization routine: `iso = IsoPackage(ckan_package)`. The **IsoPackage** simplifies access to the parts of the **Package** and related **ResponsibleParties** that are needed to generate ISO19139 XML.
3. A **CswRecord** is created via a class method: `new_record = CswRecord.from_iso_package(iso)`. This function
    - Builds the attributes required by **pycsw**, including full-text XML generated from `IsoPackage.to_iso_xml()`
    - Stores the database object that **pycsw** looks at to provide via the CSW protocol
4. A custom URL (`/csw`) is mapped to `ckanext.ngds.csw.csw_wrapper:CswController.csw`. Requests to this URL are passed on to pycsw, which performs the logic of interpretting and responding in accordance with the CSW specification.

## How does harvesting work?
1. A **HarvestNode** is stored in the database. This represents a remote CSW (or a "node-in-a-box") that will be harvested.
2. `HarvestNode.do_harvest()` is called. This function:
    - Makes a series of CSW *GetRecords* requests to determine all the IDs that are available on the remote node
    - For each ID, makes a CDW *GetRecordById* request that gets the full XML document for each record
    - **CatalogueServiceWeb** does the CSW requests, and parses each document as a **MD_Metadata** instance. These are **owslib** classes.
3. For each **MD_Metadata**, we use `HarvestedRecord.from_md_metadata()` to:
    - Read the **MD_Metadata** to create a native CKAN **Package**
    - Generate and save a **IsoPackage** object from the **Package**
    - Generate and save a **CswRecord** object from the **IsoPackage** via `CswRecord.from_iso_package`
    - Generate and save a **HarvestedRecord** object to track the relationship between harvested **Packages** and the **HarvestNode** they came from
    
## What classes are involved?
- **ckan.model.Package**: CKAN's native object representing a metadata object. We populate it with a number of "extra" attributes that are used to make a complete ISO19139 metadata record.
- **ckanext.ngds.metadata.model.ResponsibleParty**: Complete contact information for an individual. Handled as a first-order object so that people can re-use contact information and update it when appropriate.
- **ckanext.ngds.metadata.model.IsoPackage**: These objects are not persisted in the database, but are simply wrappers around CKAN **Packages** that facilitate the creation of ISO19139 XML documents.
- **ckanext.ngds.csw.model.CswRecord**: These database records are what **pycsw** serves via standard CSW protocols. They are generated from **IsoPackages**.
- **owslib.iso.MD_Metadata**: These objects are not persisted in the database, but are parsed versions of ISO19139 XML documents. They can only be created from XML files, so you cannot make them directly from CKAN **Packages**.
- **ckanext.ngds.harvest.model.HarvestNode**: These database records are essentially pointers to remote CSW servers from which we want to harvest metadata. Harvesting is initiated in code by calling `do_harvest()` on a **HarvestNode** instance.
- **ckanext.ngds.harvest.model.HarvestedNode**: These database records store the relationship between **Packages** that were harvested and the **HarvestNode** they came from. They can be created via a class method `HarvestedRecord.from_md_metadata()`, which is passed a **owslib.iso.MD_Metadata** instance as a parameter.

 


