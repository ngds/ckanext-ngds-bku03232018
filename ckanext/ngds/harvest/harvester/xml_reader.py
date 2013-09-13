from ckanext.spatial.model import ISOElement, MappedXmlDocument

class NgdsXmlMapping(MappedXmlDocument):
    """
    Inherits from ckanext.spatial.model.MappedXmlDocument.
    ckanext.spatial.model.ISODocument is a similar example

    - Invoke with `my_ngds_mapping = NgdsXmlMapping(xml_str=None, xml_tree=None)`
    - Then get values by `my_ngds_mapping.get_values()`
    """

    elements = [
        # Maintainer
        ISOElement(
            name="maintainer-name",
            search_paths="gmd:contact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString/text()",
            multiplicity="0..1", # "*", "1..*", "1" are other options
        ),
        ISOElement(
            name="maintainer-email",
            search_paths="gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString/text()",
            multiplicity="0..1", # "*", "1..*", "1" are other options
        ),

        # Other ID
        ISOElement(
            name="other_id",
            search_paths="gmd:dataSetURI/gco:CharacterString/text()",
            multiplicity="0..1", # "*", "1..*", "1" are other options
        ),

        # Data Type
        ISOElement(
            name="data_type",
            search_paths="gmd:hierarchyLevelName/gco:CharacterString/text()",
            multiplicity="1", # "*", "1..*", "1" are other options
        ),

        # Pub Date
        ISOElement(
            name="publication_date",
            search_paths="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:DateTime/text()",
            multiplicity="0..1", # "*", "1..*", "1" are other options
        ),

        # Authors <<<
        ISOElement(
            name="",
            search_paths="gmd:dataSetURI/gco:CharacterString/text()",
            multiplicity="0..1", # "*", "1..*", "1" are other options
        ),

        # Quality <<<
        ISOElement(
            name="quality",
            search_paths="gmd:dataSetURI/gco:CharacterString/text()",
            multiplicity="0..1", # "*", "1..*", "1" are other options
        ),

        # Lineage <<<
        ISOElement(
            name="lineage",
            search_paths="gmd:dataSetURI/gco:CharacterString/text()",
            multiplicity="0..1", # "*", "1..*", "1" are other options
        ),

        # Status
        ISOElement(
            name="status",
            search_paths="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:status/gmd:MD_ProgressCode/@codeListValue",
            multiplicity="0..1", # "*", "1..*", "1" are other options
        )
    ]