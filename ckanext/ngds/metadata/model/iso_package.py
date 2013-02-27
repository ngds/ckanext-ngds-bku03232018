from additional_metadata import ResponsibleParty
from lxml import etree

class IsoPackage(object):
    """
    A wrapper around a CKAN Package that helps organize extras and facilitate export to ISO19139
    """
    
    metadata_info = {}
    dataset_info = {}
    resources = []
    
    def __init__(self, ckan_package):
        """Must give us a Package to get things started"""
        self.ckan_package = ckan_package
        
        # So the idea is to take the package and parse it out into what we need for ISO
        
        ## Metadata info
        self.metadata_info["id"] = self.ckan_package.id
        self.metadata_info["language"] = "eng"
        self.metadata_info["charset"] = "utf8"
        self.metadata_info["contact"] = self.get_metadata_contact()
        self.metadata_info["updated"] = self.ckan_package.metadata_modified
        self.metadata_info["standard"] = "ISO-NAP-USGIN"
        self.metadata_info["version"] = "1.1"
        
        ## Dataset info
        self.dataset_info["uri"] = self.ckan_package.extras.get("dataset_uri", "http://path/to/ckan/package")
        self.dataset_info["category"] = self.ckan_package.extras.get("dataset_category", "Dataset")
        self.dataset_info["title"] = self.ckan_package.title
        self.dataset_info["publication_date"] = self.ckan_package.extras.get("publication_date", self.ckan_package.metadata_modified)
        self.dataset_info["creators"] = self.get_dataset_creators()
        self.dataset_info["abstract"] = self.ckan_package.notes
        self.dataset_info["quality"] = self.ckan_package.extras.get("quality", None)
        self.dataset_info["status"] = self.ckan_package.extras.get("status", "completed")
        self.dataset_info["keywords"] = self.ckan_package.get_tags()
        self.dataset_info["language"] = self.ckan_package.extras.get("dataset_lang", "eng")
        self.dataset_info["topic"] = "geoscientificInformation"
        self.dataset_info["extent"] = self.ckan_package.extras.get("spatial", self.ckan_package.extras.get("spatial_word", None))
        self.dataset_info["usage"] = self.ckan_package.license_id
        
        ## Distribution info
        self.resources = [ self.make_resource(resource) for resource in self.ckan_package.resources ]
    
    def get_distributor_contact(self, ckan_resource):
        contact_id = ckan_resource.extras.get("distributor")        
        return self.build_contact(ResponsibleParty.by_id(contact_id), "distributor")
    
    def get_metadata_contact(self):
        contact_id = self.ckan_package.extras.get("metadata_contact")
        party = ResponsibleParty.by_id(contact_id)
        contact = self.build_contact(party, "pointOfContact")
        return contact

    def get_dataset_creators(self):
        creators = self.ckan_package.extras.get("creators", [])
        return [ self.build_contact(ResponsibleParty.by_id(creator["id"]), creator["role"]) for creator in creators ]
    
    def build_contact(self, responsible_party, role):
        return {
            "person": responsible_party,
            "role": role        
        }
        
    def make_resource(self, ckan_resource):
        return {
            "name": ckan_resource.name,
            "description": ckan_resource.description,
            "url": ckan_resource.url,
            "distributor": self.get_distributor_contact(ckan_resource),
            "protocol": ckan_resource.extras.get("protocol", None),
            "layer": ckan_resource.extras.get("layer", None),
            "format": ckan_resource.extras.get("format", None),
            "ordering": ckan_resource.extras.get("ordering", None)
        }
        
    def to_iso_xml(self):
        """Create ISO19139 XML in accordance with the USGIN metadata profile"""
        namespaces = {
            "gmd": "http://www.isotc211.org/2005/gmd",
            "gco": "http://www.isotc211.org/2005/gco",
            "gml": "http://www.opengis.net/gml",
            "xlink": "http://www.w3.org/1999/xlink",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance"            
        }
        
        def qualifiedName(ns, element):
            """Return a namespace-qualified element name"""
            return '{%s}%s' % (namespaces[ns], element)
        
        def fileIdentifier():
            fileId = etree.Element(qualifiedName("gmd", "fileIdentifier"))
            etree.SubElement(fileId, qualifiedName("gco", "CharacterString")).text = self.metadata_info["id"]
            return fileId
        
        def metadataLanguage():
            lang = etree.Element(qualifiedName("gmd", "language"))
            etree.SubElement(lang, qualifiedName("gco", "CharacterString")).text = self.metadata_info["language"]
            return lang
        
        def charSet():
            charSet = etree.Element(qualifiedName("gmd", "characterSet"))
            attr = {
                "codeList": "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#MD_CharacterSetCode",
                "codeListValue": self.dataset_info["charset"]
            }
            etree.SubElement(charSet, qualifiedName("gmd", "MD_CharacterSetCode"), **attr).text = self.dataset_info["charset"]
            return charSet
        
        def hierarchyLevel():
            level = etree.Element(qualifiedName("gmd", "hierarchyLevel"))
            attr = {
                "codeList": "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#MD_ScopeCode",
                "codeListValue": self.dataset_info["category"]
            }
            etree.SubElement(level, qualifiedName("gmd", "MD_ScopeCode"), **attr).text = self.dataset_info["category"]
            return level
        
        def hierarchyLevelName():
            levelName = etree.Element(qualifiedName("gmd", "hierarchyLevelName"))
            etree.SubElement(levelName, qualifiedName("gco", "CharacterString")).text = self.dataset_info["category"]
            return levelName
        
        def responsibleParty(contact):
            person = contact["person"]
            
            party = etree.Element(qualifiedName("gmd", "CI_ResponsibleParty"))
            
            name = etree.SubElement(party, qualifiedName("gmd", "individualName"))
            etree.SubElement(name, qualifiedName("gco", "CharacterString")).text = person.name            
            
            orgName = etree.SubElement(party, qualifiedName("gmd", "organisationName"))
            etree.SubElement(orgName, qualifiedName("gco", "CharacterString")).text = person.organization
            
            contact_attr = etree.SubElement(party, qualifiedName("gmd", "contactInfo"))
            contact = etree.SubElement(contact_attr, qualifiedName("gmd", "CI_Contact"))
            
            phone_attr = etree.SubElement(contact, qualifiedName("gmd", "phone"))
            phone = etree.SubElement(phone_attr, qualifiedName("gmd", "CI_Telephone"))
            etree.SubElement(phone, qualifiedName("gmd", "voice")).text = person.phone
            
            address_attr = etree.SubElement(contact, qualifiedName("gmd", "address"))
            address = etree.SubElement(address_attr, qualifiedName("gmd", "CI_Address"))
            
            delivery = etree.SubElement(address, qualifiedName("gmd", "deliveryPoint"))
            etree.SubElement(delivery, qualifiedName("gco", "CharacterString")).text = person.street
            
            city = etree.SubElement(address, qualifiedName("gmd", "city"))
            etree.SubElement(city, qualifiedName("gco", "CharacterString")).text = person.city
            
            area = etree.SubElement(address, qualifiedName("gmd", "administrativeArea"))
            etree.SubElement(area, qualifiedName("gco", "CharacterString")).text = person.state
            
            zipcode = etree.SubElement(address, qualifiedName("gmd", "postalCode"))
            etree.SubElement(zipcode, qualifiedName("gco", "CharacterString")).text = person.zip
            
            country = etree.SubElement(address, qualifiedName("gmd", "country"))
            etree.SubElement(country, qualifiedName("gco", "CharacterString")).text = person.country
            
            email = etree.SubElement(address, qualifiedName("gmd", "electronicMailAddress"))
            etree.SubElement(email, qualifiedName("gco", "CharacterString")).text = person.email
            
            role_attr = etree.SubElement(party, qualifiedName("gmd", "role"))
            attr = {
                "codeList": "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#CI_RoleCode",
                "codeListValue": contact["role"]                
            }
            etree.SubElement(role_attr, qualifiedName("gmd", "CI_RoleCode"), **attr).text = contact["role"]
            
            return party
        
        def metadataContact():
            contact = etree.Element(qualifiedName("gmd", "contact"))
            contact.append(responsibleParty(self.metadata_info["contact"]))
            return contact
        
        # Create the root element
        schemaLocation = { qualifiedName("xsi", "schemaLocation"): "http://www.isotc211.org/2005/gmd http://schemas.opengis.net/csw/2.0.2/profiles/apiso/1.0.0/apiso.xsd" }
        record = etree.Element(qualifiedName("gmd", "MD_Metadata"), nsmap=namespaces, **schemaLocation)
        
        # Metadata info
        record.append(fileIdentifier())
        record.append(metadataLanguage())
        record.append(charSet())
        record.append(hierarchyLevel())
        record.append(hierarchyLevelName())
        record.append(metadataContact())

        # Convert to a string and return it.
        return etree.tostring(record)
        
        
        
        
        