from ckan import model
from ckanext.ngds.metadata.model.additional_metadata import AdditionalPackageMetadata, AdditionalResourceMetadata
from lxml import etree
from datetime import datetime

class CswPackage(object):
    """
    Class that wraps a CKAN package and provides methods to/from ISO19139 metadata
    """
    
    def __init__(self, package):
        """To create an instance of this class, pass a valid CKAN package as an argument"""
        # Pass in a core CKAN package
        self.package = package
        
        # Find the correlated objects for additional metadata
        self.additional_package_metadata = AdditionalPackageMetadata.by_package(package.id)
        self.additional_resource_metadata = [ AdditionalResourceMetadata.by_resource(resource.id) for resource in package.resources if AdditionalResourceMetadata.by_resource(resource.id) != None ]
                
    def to_iso_xml(self):
        """Create ISO19139 XML in accordance with the USGIN metadata profile"""
        namespaces = {
            "gmd": "http://www.isotc211.org/2005/gmd",
            "gco": "http://www.isotc211.org/2005/gco",
            "gml": "http://www.opengis.net/gml",
            "xlink": "http://www.w3.org/1999/xlink",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance"            
        }
        
        # Helper function party time!!!
        def nsify(ns, element):
            """Return a namespace-qualified element name"""
            return '{%s}%s' % (namespaces[ns], element)
        
        def string_attribute(parent, ns, attrib_name, content):
            """Create an element with a gco:CharacterString sub-element"""
            attrib = etree.SubElement(parent, nsify(ns, attrib_name))
            etree.SubElement(attrib, nsify("gco", "CharacterString")).text = content
        
        def date_attribute(parent, ns, attrib_name, the_date):
            attrib = add_attribute(parent, ns, attrib_name)
            etree.SubElement(attrib, nsify("gco", "DateTime")).text = the_date
            
        def codelist_ele(parent, ns, elename, codelist, value):
            """Create an element that presents a value from a codeList"""
            etree.SubElement(parent, nsify(ns, elename), codeList=codelist, codeListValue=value).text = value            
        
        def add_attribute(parent, ns, attrib_name):
            """Just add a simple child element"""
            return etree.SubElement(parent, nsify(ns, attrib_name))
        
        def add_nested_elements(parent, xpath, text=None):
            """Generate a set of nested elements defined by a simple xpath"""            
            elements = xpath.split("/")
            eles = [ parent ]
            for ele in elements:
                ns = ele.split(":")[0]
                elename = ele.split(":")[1]
                eles.append(add_attribute(eles.pop(), ns, elename))
            if text != None:
                eles.append(add_attribute(eles.pop(), "gco", "CharacterString"))
                eles[0].text = text
            return eles.pop()
        
        def build_responsible_party(parent, responsible_party, role):
            """Build XML representing a ResponsibleParty"""
            party = add_attribute(parent, "gmd", "CI_ResponsibleParty")
            string_attribute(party, "gmd", "individualName", responsible_party.name)
            string_attribute(party, "gmd", "organisationName", responsible_party.organization)
            contact = add_nested_elements(party, "gmd:contactInfo/gmd:CI_Contact")
            add_nested_elements(contact, "gmd:phone/gmd:CI_Telephone/gmd:voice", responsible_party.phone)
            address = add_nested_elements(contact, "gmd:address/gmd:CI_Address")
            string_attribute(address, "gmd", "deliveryPoint", responsible_party.street)
            string_attribute(address, "gmd", "city", responsible_party.city)
            string_attribute(address, "gmd", "administrativeArea", responsible_party.state)
            string_attribute(address, "gmd", "postalCode", responsible_party.zip)
            string_attribute(address, "gmd", "country", "USA")
            string_attribute(address, "gmd", "electronicMailAddress", responsible_party.email)
            role_attr = add_attribute(party, "gmd", "role")
            codelist_ele(role_attr, "gmd", "CI_RoleCode", "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#CI_RoleCode", role)
        
        def distribution_id_for(resource):
            return "distribution-%s" % resource.id
        
        def build_transfer_option(parent, distribution_info):
            transfer_option = etree.SubElement(parent, nsify("gmd", "transferOptions"), id=distribution_id_for(distribution_info.resource))
            online = add_nested_elements(transfer_option, "gmd:MD_DigitalTransferOptions/gmd:onLine")
            
        # Create the root element of the record
        schemaLocation = nsify("xsi", "schemaLocation")
        attributes = { schemaLocation: "http://www.isotc211.org/2005/gmd http://schemas.opengis.net/csw/2.0.2/profiles/apiso/1.0.0/apiso.xsd" }
        record = etree.Element(nsify("gmd", "MD_Metadata"), nsmap=namespaces, **attributes)
        
        # Information about the metadata record itself
        string_attribute(record, "gmd", "fileIdentifier", self.package.id) # File Identifier
        string_attribute(record, "gmd", "language", "eng") # Language
        char_set = add_attribute(record, "gmd", "characterSet")
        codelist_ele(char_set, "gmd", "MD_CharacterSetCode", 
            "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#MD_CharacterSetCode",
            "utf8"
        )
        hierarchy = add_attribute(record, "gmd", "hierarchyLevel")
        codelist_ele(hierarchy, "gmd", "MD_ScopeCode",
            "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#MD_ScopeCode",
            "dataset"    
        )
        string_attribute(record, "gmd", "hierarchyLevelName", "Dataset")
        metadata_contact = add_attribute(record, "gmd", "contact")
        build_responsible_party(metadata_contact, self.additional_package_metadata.maintainer, "pointOfContact")
        date_attribute(record, "gmd", "dateStamp", self.package.metadata_modified.isoformat())
        string_attribute(record, "gmd", "metadataStandardName", "ISO-NAP-USGIN")
        string_attribute(record, "gmd", "metadataStandardVersion", "1.1.4")
        string_attribute(record, "gmd", "dataSetUri", "http://path/to/package/page?")
        
        # Identification Information
        idInfo = add_nested_elements(record, "gmd:identificationInfo/gmd:MD_DataIdentification")
        
        ## Citation
        citation = add_nested_elements(idInfo, "gmd:citation/gmd:CI_Citation")
        string_attribute(citation, "gmd", "title", self.package.title)
        date_wrapper = add_nested_elements(citation, "gmd:date/gmd:CI_Date")
        pub = datetime.combine(self.additional_package_metadata.pub_date, datetime.min.time())
        date_attribute(date_wrapper, "gmd", "date", pub.isoformat())
        date_type = add_attribute(date_wrapper, "gmd", "dateType")
        codelist_ele(date_type, "gmd", "CI_DateTypeCode",
            "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode",
            "publication"
        )
        author = add_attribute(citation, "gmd", "citedResponsibleParty")
        build_responsible_party(author, self.additional_package_metadata.author, "originator")
        ### gmd:otherCitationDetails as a place to put a "formal" citation?
        
        ## Other ID info
        string_attribute(idInfo, "gmd", "abstract", self.package.notes)
        status = add_attribute(idInfo, "gmd", "status") # Pacakage has "state" which may play into this
        codelist_ele(status, "gmd", "MD_ProgressCode", "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#MD_ProgressCode", "completed")
        
        ## Keywords
        keywords = add_nested_elements(idInfo, "gmd:descriptiveKeywords/gmd:MD_Keywords")
        [ string_attribute(keywords, "gmd", "keyword", tag.name) for tag in self.package.get_tags() ]
        
        ## Dataset language
        string_attribute(idInfo, "gmd", "language", "eng")
        
        ## Topic category -- this doesn't look right
        topic = add_attribute(idInfo, "gmd", "topicCategory")        
        add_attribute(topic, "gmd", "MD_TopicCategoryCode").text = "geoscientificInformation"
        
        ## Extent
        extent = add_nested_elements(idInfo, "gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox")
        add_nested_elements(extent, "gmd:extentTypeCode/gco:Boolean").text = "1" # Is this really valid?
        
        ## Distribution Information
        distInfo = add_nested_elements(record, "gmd:distributionInfo/gmd:MD_Distribution")
        
        ### Build an useful dictionary for working through distributions
        distribute_obj = {} # key = distributor_id, value = list of resource_infos
        for resource_info in self.additional_resource_metadata:
            dist_id = str(resource_info.distributor_id)
            if dist_id not in distribute_obj.keys():
                distribute_obj[dist_id] = { "distributor": resource_info.distributor, "distributions": [] }
            distribute_obj[dist_id]["distributions"].append(resource_info)
        ### Loop through and add distributors and references to their distributions
        for dist_id, dist_info in distribute_obj.items():
            distributor = add_nested_elements(distInfo, "gmd:distributor/gmd:MD_Distributor")
            distContact = add_attribute(distributor, "gmd", "distributorContact")
            build_responsible_party(distContact, dist_info["distributor"], "distributor")
            for dist in dist_info["distributions"]:
                reference = { nsify("xlink", "href"): "#%s" % distribution_id_for(dist.resource) }
                etree.SubElement(distributor, nsify("gmd", "distributorTransferOptions"), **reference)
        ### Loop through one more time and add distributions
        [ build_transfer_option(distInfo, resource_info) for resource_info in self.additional_resource_metadata ]
        
            
        
        # Quality Information
        qualInfo = add_nested_elements(record, "gmd:dataQualityInfo/gmd:DQ_DataQuality")
        
        # Usage Constraints
        usageInfo = add_nested_elements(record, "gmd:metadataConstraints/gmd:MD_Constraints")
        
        # Finally, return the string representation of the record
        return etree.tostring(record)
        
    @classmethod
    def from_iso_xml(cls, xml):
        """Create a CKAN Package from the given XML string"""
        pass
        
def add_csw_model():
    """Simply append the CswPackage class to CKAN.model"""
    model.CswPackage = CswPackage
    