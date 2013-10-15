''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

from ckanext.spatial.model import ISOElement, ISODocument, ISOResponsibleParty

class NgdsXmlMapping(ISODocument):
    """
    Inherits from ckanext.spatial.model.MappedXmlDocument.
    ckanext.spatial.model.ISODocument is a similar example

    - Invoke with `my_ngds_mapping = NgdsXmlMapping(xml_str=None, xml_tree=None)`
    - Then get values by `my_ngds_mapping.read_values()`
    """

    elements = [
        # Maintainer
        ISOResponsibleParty(
            name="maintainer",
            search_paths=[
                "gmd:contact/gmd:CI_ResponsibleParty"
            ],
            multiplicity="1"
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

        # Authors
        ISOResponsibleParty(
            name="authors",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty"
            ],
            multiplicity="*"
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

    def infer_values(self, values):
        return values
