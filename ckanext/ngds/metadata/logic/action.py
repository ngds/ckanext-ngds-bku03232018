import json
from shapely.geometry import asShape
from lxml import etree
from dateutil import parser as date_parser
from ckanext.ngds.common import plugins as p
from ckanext.ngds.common import logic
from ckanext.ngds.common import base
from ckanext.ngds.common import config

"""
Lifted from ckanext-ngds/ckanext/ngds/csw/logic/view.py
Kudos goes to Ryan Clark on this function and the template that it renders.  It takes any
CKAN package in JSON format and parses it into a dictionary object that can be passed into
a Jinja2 template to render an ISO XML metadata record of the package.
"""
@logic.side_effect_free
def iso_19139(context, data_dict):
    """
    Serialize a CKAN Package as an ISO 19139 XML document

    Gets the package to be converted, processes it, and passes it through a Jinja2 template
    which generates an XML string

    @param context: CKAN background noise
    @param data_dict: Must contain an "id" key which is a pointer to the package to serialize
    @return: ISO19139 XML string
    """

    pkg = logic.action.get.package_show(context, data_dict)

    # ---- Reformat extras so they can be looked up
    pkg["additional"] = {}
    for extra in pkg["extras"]:
        pkg["additional"][extra["key"]] = extra["value"]

    # ---- Remove milliseconds from metadata dates
    pkg["metadata_modified"] = date_parser.parse(pkg.get("metadata_modified", "")).replace(microsecond=0).isoformat()
    pkg["metadata_created"] = date_parser.parse(pkg.get("metadata_created", "")).replace(microsecond=0).isoformat()

    # ---- Make sure that there is a publication date (otherwise you'll get invalid metadata)
    if not pkg["additional"].get("publication_date", False):
        pkg["additional"]["publication_date"] = pkg["metadata_created"]

    # ---- Figure out URIs
    other_ids = pkg["additional"].get("other_id", "[]")
    if len(json.loads(other_ids)) > 0:
        pkg["additional"]["datasetUri"] = json.loads(other_ids)[0]
    else:
        pkg["additional"]["datasetUri"] = config.get("ckan.site_url", "http://default.ngds.com").rstrip("/") + \
            "/dataset/%s" % pkg["name"]

    # ---- Any other identifiers
    pkg['additional']['other_id'] = json.loads(pkg['additional'].get('other_id', '[]'))

    # ---- Load the authors
    authors = pkg["additional"].get("authors", None)
    try:
        pkg["additional"]["authors"] = json.loads(authors)
    except:
        pkg["additional"]["authors"] = [{"name": pkg["author"], "email": pkg["author_email"]}]

    # ---- Load Location keywords
    location = pkg["additional"].get("location", "[]")
    try:
        loc = json.loads(location)
        if not isinstance(loc, list):
            pkg["additional"]["location"] = [loc]
        else:
            pkg["additional"]["location"] = loc
    except:
        pkg["additional"]["location"] = []

    # ---- Reformat facets
    faceted_ones = [t for t in pkg.get("tags", []) if t.get("vocabulary_id") is not None]
    pkg["additional"]["facets"] = {}
    for faceted_tag in faceted_ones:
        vocab = p.toolkit.get_action("vocabulary_show")(None, {"id": faceted_tag.get("vocabulary_id", "")})
        vocab_name = vocab.get("name", None)
        if vocab_name is not None and vocab_name in pkg["additional"]["facets"]:
            pkg["additional"]["facets"][vocab_name].append(faceted_tag.get("display_name"))
        elif vocab_name is not None:
            pkg["additional"]["facets"][vocab_name] = [faceted_tag.get("display_name")]

    # ---- Extract BBOX coords from extras
    pkg["extent"] = {}

    geojson = pkg["additional"].get("spatial", None)

    if geojson is not None:
        try:
            bounds = asShape(json.loads(geojson)).bounds
            pkg["extent"] = {
                "west": bounds[0],
                "south": bounds[1],
                "east": bounds[2],
                "north": bounds[3]
            }
        except:
            # Couldn't parse spatial extra into bounding coordinates
            pass

    # ---- Reorganize resources by distributor, on/offline
    online = {}
    offline = {}
    for resource in pkg.get("resources", []):
        try:
            distributor = json.loads(resource.get("distributor", "{}"))
        except ValueError:
            # This will happen if the content of the distributor field is invalid JSON
            distributor = {}

        if json.loads(resource.get("is_online", "true")):
            resources = online
        else:
            resources = offline

        if distributor != {}:
            name = distributor.get("name", "None")
        else:
            name = "None"

        if name not in resources.keys():
            resources[name] = {
                "distributor": distributor,
                "resources": [resource]
            }
        else:
            resources[name]["resources"].append(resource)

    pkg["additional"]["online"] = [value for key, value in online.iteritems()]
    pkg["additional"]["offline"] = [value for key, value in offline.iteritems()]

    # ---- All done, render the template
    output = base.render("xml/package_to_iso.xml", pkg)

    return output

'''
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
        self.dataset_info["category"] = self.ckan_package.extras.get("dataset_category", "dataset")
        self.dataset_info["title"] = self.ckan_package.title
        self.dataset_info["publication_date"] = self.ckan_package.extras.get("publication_date", self.ckan_package.metadata_modified)
        self.dataset_info["creators"] = self.get_dataset_creators()
        self.dataset_info["abstract"] = self.ckan_package.notes
        self.dataset_info["quality"] = self.ckan_package.extras.get("quality")
        self.dataset_info["status"] = self.ckan_package.extras.get("status", "completed")
        self.dataset_info["keywords"] = self.ckan_package.get_tags()
        self.dataset_info["language"] = self.ckan_package.extras.get("dataset_lang", "eng")
        self.dataset_info["topic"] = "geoscientificInformation"
        self.dataset_info["extent_keyword"] = self.ckan_package.extras.get("spatial_word")
        self.dataset_info["extent"] = self.ckan_package.extras.get("spatial")
        self.dataset_info["usage"] = self.license_text()
        
        ## Distribution info
        self.resources = [ self.make_resource(resource) for resource in self.ckan_package.resources ]
    
    def get_distributor_contact(self, ckan_resource):
        contact_id = ckan_resource.extras.get("distributor")
        if contact_id:
            party = ResponsibleParty.by_id(contact_id)
            return self.build_contact(party, "distributor")
        else:
            return None
        
    def get_metadata_contact(self):
        contact_id = self.ckan_package.extras.get("metadata_contact")
        if contact_id:
            party = ResponsibleParty.by_id(contact_id)
            contact = self.build_contact(party, "pointOfContact")
            return contact
        else: 
            return None

    def get_dataset_creators(self):
        creators = self.ckan_package.extras.get("creators", "") # should later support multiplicity
        #creators = json.loads(creators)
        return [ self.build_contact(ResponsibleParty.by_id(creator), "author") for creator in creators ] # should that hard-wire to author?
    
    def build_contact(self, responsible_party, role):
        return {
            "person": responsible_party,
            "role": role        
        }
        
    def make_resource(self, ckan_resource):
        return {
            "id": ckan_resource.id,
            "name": ckan_resource.name,
            "description": ckan_resource.description,
            "url": ckan_resource.url,
            "distributor": self.get_distributor_contact(ckan_resource),
            "protocol": ckan_resource.extras.get("protocol", None),
            "layer": ckan_resource.extras.get("layer", None),
            "format": ckan_resource.extras.get("format", None),
            "ordering": ckan_resource.extras.get("ordering", None)
        }
    
    def distributionHelper(self):
        obj = {}
        for resource in self.resources:
            if resource["distributor"] is not None:
                distributor_id = resource["distributor"]["person"].id
                if distributor_id not in obj.keys():
                    obj[distributor_id] = { "distributor": resource["distributor"], "resources": [] }
                obj[distributor_id]["resources"].append(resource)
            else:
                if "no-distributor-specified" not in obj.keys():
                    obj["no-distributor-specified"] = { "distributor": None, "resources": [] }
                obj["no-distributor-specified"]["resources"].append(resource)
        return obj
    
    def license_text(self):            
        licenses = { "cc-by": "Creative Commons Attribution",
          "cc-by-sa": "Creative Commons Attribution Share-Alike",
          "cc-zero": "Creative Commons CCZero",
          "cc-nc": "Creative Commons Non-Commercial (Any)",
          "gfdl": "GNU Free Documentation License",
          "notspecified": "License Not Specified",
          "odc-by": "Open Data Commons Attribution License",
          "odc-odbl": "Open Data Commons Open Database License (ODbL)",
          "odc-pddl": "Open Data Commons Public Domain Dedication and Licence (PDDL)",
          "other-at": "Other (Attribution)",
          "other-nc": "Other (Non-Commercial)",
          "other-closed": "Other (Not Open)",
          "other-open": "Other (Open)",
          "other-pd": "Other (Public Domain)",
          "uk-ogl": "UK Open Government Licence (OGL)"
        }
        return licenses[self.ckan_package.license_id]
            
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
                "codeListValue": self.metadata_info["charset"]
            }
            etree.SubElement(charSet, qualifiedName("gmd", "MD_CharacterSetCode"), **attr).text = self.metadata_info["charset"]
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
            voice = etree.SubElement(phone, qualifiedName("gmd", "voice"))
            etree.SubElement(voice, qualifiedName("gco", "CharacterString")).text = person.phone
            
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
                "codeListValue": "pointofContact" #contact["role"]                
            }
            etree.SubElement(role_attr, qualifiedName("gmd", "CI_RoleCode"), **attr).text = contact["role"]
            
            return party
        
        def metadataContact():
            contact = etree.Element(qualifiedName("gmd", "contact"))
            contact_obj = self.metadata_info["contact"]
            if contact_obj:
                contact.append(responsibleParty(contact_obj))
            return contact
        
        def dateStamp():
            date = etree.Element(qualifiedName("gmd", "dateStamp"))
            etree.SubElement(date, qualifiedName("gco", "DateTime")).text = self.metadata_info["updated"].isoformat()
            return date
        
        def metadataStandardName():
            name = etree.Element(qualifiedName("gmd", "metadataStandardName"))
            etree.SubElement(name, qualifiedName("gco", "CharacterString")).text = self.metadata_info["standard"]
            return name
        
        def metadataStandardVersion():
            version = etree.Element(qualifiedName("gmd", "metadataStandardVersion"))
            etree.SubElement(version, qualifiedName("gco", "CharacterString")).text = self.metadata_info["version"]
            return version
        
        def datasetUri():
            uri = etree.Element(qualifiedName("gmd", "dataSetURI"))
            etree.SubElement(uri, qualifiedName("gco", "CharacterString")).text = self.dataset_info["uri"]
            return uri
        
        def title():
            title = etree.Element(qualifiedName("gmd", "title"))
            etree.SubElement(title, qualifiedName("gco", "CharacterString")).text = self.dataset_info["title"]
            return title
        
        def publicationDate():
            date_attr = etree.Element(qualifiedName("gmd", "date"))
            date = etree.SubElement(date_attr, qualifiedName("gmd", "CI_Date"))
            subDate = etree.SubElement(date, qualifiedName("gmd", "date"))
            etree.SubElement(subDate, qualifiedName("gco", "DateTime")).text = self.dataset_info["publication_date"].isoformat()
            dateType = etree.SubElement(date, qualifiedName("gmd", "dateType"))
            attr = {
                "codeList": "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode",
                "codeListValue": "publication"
            }
            etree.SubElement(dateType, qualifiedName("gmd", "CI_DateTypeCode"), **attr).text = "publication"
            return date_attr
        
        def citedResponsibleParties(parent):
            for creator in self.dataset_info["creators"]:
                cited = etree.SubElement(parent, qualifiedName("gmd", "citedResponsibleParty"))
                cited.append(responsibleParty(creator))
        
        def abstract():
            abstract_str = self.dataset_info["abstract"]
            if self.dataset_info["quality"]:
                abstract_str += " QualityStatement: %s" % self.dataset_info["quality"]
                
            abstract = etree.Element(qualifiedName("gmd", "abstract"))
            etree.SubElement(abstract, qualifiedName("gco", "CharacterString")).text = abstract_str
            return abstract
        
        def status():
            status = etree.Element(qualifiedName("gmd", "status"))
            attr = {
                "codeList": "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#MD_ProgressCode",        
                "codeListValue": self.dataset_info["status"]
            }
            etree.SubElement(status, qualifiedName("gmd", "MD_ProgressCode"), **attr).text = self.dataset_info["status"]
            return status
        
        def themeKeywords():
            keyword_attr = etree.Element(qualifiedName("gmd", "descriptiveKeywords"))
            keywords = etree.SubElement(keyword_attr, qualifiedName("gmd", "MD_Keywords"))
            for keyword in self.dataset_info["keywords"]:
                attr = etree.SubElement(keywords, qualifiedName("gmd", "keyword"))
                etree.SubElement(attr, qualifiedName("gco", "CharacterString")).text = keyword.name
            keyword_type = etree.SubElement(keywords, qualifiedName("gmd", "type"))
            attr = {
                "codeList": "",
                "codeListValue": "theme"        
            }
            etree.SubElement(keyword_type, qualifiedName("gmd", "MD_KeywordTypeCode"), **attr).text = "theme"
            return keyword_attr
        
        def extentKeyword():
            keyword_attr = etree.Element(qualifiedName("gmd", "descriptiveKeywords"))
            keywords = etree.SubElement(keyword_attr, qualifiedName("gmd", "MD_Keywords"))
            attr = etree.SubElement(keywords, qualifiedName("gmd", "keyword"))
            etree.SubElement(attr, qualifiedName("gco", "CharacterString")).text = self.dataset_info["extent_keyword"]
            keyword_type = etree.SubElement(keywords, qualifiedName("gmd", "type"))
            attr = {
                "codeList": "",
                "codeListValue": "location"        
            }
            etree.SubElement(keyword_type, qualifiedName("gmd", "MD_KeywordTypeCode"), **attr).text = "location"
            return keyword_attr
        
        def datasetLanguage():
            lang = etree.Element(qualifiedName("gmd", "language"))
            etree.SubElement(lang, qualifiedName("gco", "CharacterString")).text = self.dataset_info["language"]
            return lang
        
        def topicCategory():
            topic = etree.Element(qualifiedName("gmd", "topicCategory"))
            etree.SubElement(topic, qualifiedName("gmd", "MD_TopicCategoryCode")).text = self.dataset_info["topic"]
            return topic
        
        def bbox():
            # Fails if an extent was not specified
            geo = asShape(json.loads(self.dataset_info["extent"]))
            
            bbox = etree.Element(qualifiedName("gmd", "EX_GeographicBoundingBox"))
            
            west = etree.SubElement(bbox, qualifiedName("gmd", "westBoundLongitude"))
            etree.SubElement(west, qualifiedName("gco", "Decimal")).text = str(geo.envelope.bounds[0])
            
            east = etree.SubElement(bbox, qualifiedName("gmd", "eastBoundLongitude"))
            etree.SubElement(east, qualifiedName("gco", "Decimal")).text = str(geo.envelope.bounds[2])
            
            south = etree.SubElement(bbox, qualifiedName("gmd", "southBoundLatitude"))
            etree.SubElement(south, qualifiedName("gco", "Decimal")).text = str(geo.envelope.bounds[1])
            
            north = etree.SubElement(bbox, qualifiedName("gmd", "northBoundLatitude"))
            etree.SubElement(north, qualifiedName("gco", "Decimal")).text = str(geo.envelope.bounds[3])
            
            return bbox
            
        def extent():
            extent = etree.Element(qualifiedName("gmd", "extent"))
            ex_extent = etree.SubElement(extent, qualifiedName("gmd", "EX_Extent"))
            geo = etree.SubElement(ex_extent, qualifiedName("gmd", "geographicElement"))
            geo.append(bbox())
            return extent
        
        def distributionIdFor(resource):
            return "distribution-%s" % resource["id"]
            
        def distributor(dist_info):
            dist_attr = etree.Element(qualifiedName("gmd", "distributor"))
            distributor = etree.SubElement(dist_attr, qualifiedName("gmd", "MD_Distributor"))
            contact = etree.SubElement(distributor, qualifiedName("gmd", "distributorContact"))
            contact.append(responsibleParty(dist_info["distributor"]))
            for resource in dist_info["resources"]:
                attr = { qualifiedName("xlink", "href"): "#%s" % distributionIdFor(resource) }
                etree.SubElement(distributor, qualifiedName("gmd", "distributorTransferOptions"), **attr)
            return dist_attr
        
        def distributors(parent):
            helper = self.distributionHelper()
            for dist_id, dist_info in helper.items():
                if dist_info["distributor"] is not None:
                    parent.append(distributor(dist_info))
                    
        def onlineResource(resource):
            online = etree.Element(qualifiedName("gmd", "CI_OnlineResource"))
            
            link = etree.SubElement(online, qualifiedName("gmd", "linkage"))
            etree.SubElement(link, qualifiedName("gmd", "URL")).text = resource["url"]
            
            if resource["protocol"] is not None:
                protocol = etree.SubElement(online, qualifiedName("gmd", "protocol"))
                etree.SubElement(protocol, qualifiedName("gco", "CharacterString")).text = resource["protocol"] 
            
            name = etree.SubElement(online, qualifiedName("gmd", "name"))
            etree.SubElement(name, qualifiedName("gco", "CharacterString")).text = resource["name"]
            
            description = resource["description"]
            if resource["layer"] is not None: description += "LayerName: " + resource["layer"]
            desc = etree.SubElement(online, qualifiedName("gmd", "description"))
            etree.SubElement(desc, qualifiedName("gco", "CharacterString")).text = description
            
            return online
                    
        def transferOption(resource):
            option = etree.Element(qualifiedName("gmd", "transferOptions"))
            if resource["url"] is not None:
                attr = { "id": "%s" % distributionIdFor(resource) }
                digital = etree.SubElement(option, qualifiedName("gmd", "MD_DigitalTransferOptions"), **attr)
                online = etree.SubElement(digital, qualifiedName("gmd", "onLine"))
                online.append(onlineResource(resource))
            else:
                pass
            
            return option
        
        def transferOptions(parent):         
            for resource in self.resources:
                parent.append(transferOption(resource))
                        
        def usageConstraints():
            usage = etree.Element(qualifiedName("gmd", "useLimitation"))
            etree.SubElement(usage, qualifiedName("gco", "CharacterString")).text = self.dataset_info["usage"]
            return usage
               
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
        record.append(dateStamp())
        record.append(metadataStandardName())
        record.append(metadataStandardVersion())
        record.append(datasetUri())
        
        # Create the identificationInfo section
        idInfo_attr = etree.SubElement(record, qualifiedName("gmd", "identificationInfo"))
        idInfo = etree.SubElement(idInfo_attr, qualifiedName("gmd", "MD_DataIdentification"))
        
        cit_attr = etree.SubElement(idInfo, qualifiedName("gmd", "citation"))
        citation = etree.SubElement(cit_attr, qualifiedName("gmd", "CI_Citation"))
        
        citation.append(title())
        citation.append(publicationDate())
        citedResponsibleParties(citation)
        idInfo.append(status())
        
        idInfo.append(abstract())        
        idInfo.append(themeKeywords())
        if self.dataset_info["extent_keyword"]: idInfo.append(extentKeyword())
        idInfo.append(datasetLanguage())
        idInfo.append(topicCategory())
        idInfo.append(extent())
        
        # Create the distributionInfo section
        distInfo_attr = etree.SubElement(record, qualifiedName("gmd", "distributionInfo"))
        distInfo = etree.SubElement(distInfo_attr, qualifiedName("gmd", "MD_Distribution"))
            
        distributors(distInfo)
        transferOptions(distInfo)
        
        # Constraints
        constraint_attr = etree.SubElement(record, qualifiedName("gmd", "metadataConstraints"))
        constraints = etree.SubElement(constraint_attr, qualifiedName("gmd", "MD_Constraints"))
        constraints.append(usageConstraints())
        
        # Convert to a string and return it.
        return etree.tostring(record, encoding=unicode)
'''