from ckanext.ngds.tests.ngds_test_case import NgdsTestCase
from ckanext.ngds.csw.logic.view import iso_metadata
from dateutil import parser as date_parser
from pylons import config as pylons_config
from lxml import etree
import json
import os


def validate(package_id):
    cache_path = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "schemas.opengis.net"
        )
    )
    cached_schema_path = os.path.join(
        cache_path,
        "csw",
        "profiles",
        "apiso",
        "1.0.0",
        "apiso.xsd"
    )

    cached_iso_path = os.path.join(
        cache_path,
        "iso",
        "19139",
        "20060504"
    )

    class SchemaResolver(etree.Resolver):
        def resolve(self, url, id, context):
            if url == "http://schemas.opengis.net/iso/19139/20060504/gco/gco.xsd":
                return self.resolve_filename(os.path.join(cached_iso_path, "gco", "gco.xsd"), context)
            elif url == "http://schemas.opengis.net/iso/19139/20060504/gmd/gmd.xsd":
                return self.resolve_filename(os.path.join(cached_iso_path, "gmd", "gmd.xsd"), context)
            elif url == "http://schemas.opengis.net/iso/19139/20060504/gml/gml.xsd":
                return self.resolve_filename(os.path.join(cached_iso_path, "gml", "gml.xsd"), context)
            elif url == "http://schemas.opengis.net/iso/19139/20060504/gmx/gmx.xsd":
                return self.resolve_filename(os.path.join(cached_iso_path, "gmx", "gmx.xsd"), context)
            elif url == "http://schemas.opengis.net/iso/19139/20060504/gsr/gsr.xsd":
                return self.resolve_filename(os.path.join(cached_iso_path, "gsr", "gsr.xsd"), context)
            elif url == "http://schemas.opengis.net/iso/19139/20060504/gss/gss.xsd":
                return self.resolve_filename(os.path.join(cached_iso_path, "gss", "gss.xsd"), context)
            elif url == "http://schemas.opengis.net/iso/19139/20060504/gts/gts.xsd":
                return self.resolve_filename(os.path.join(cached_iso_path, "gts", "gts.xsd"), context)
            elif url == "http://schemas.opengis.net/iso/19139/20060504/srv/srv.xsd":
                return self.resolve_filename(os.path.join(cached_iso_path, "srv", "srv.xsd"), context)
            elif url == "http://schemas.opengis.net/xlink/1.0.0/xlinks.xsd":
                return self.resolve_filename(os.path.join(cache_path, "xlink", "1.0.0", "xlinks.xsd"), context)
            else:
                return None

    parser = etree.XMLParser()
    parser.resolvers.add(SchemaResolver())

    schema_doc = etree.parse(cached_schema_path, parser)
    schema = etree.XMLSchema(schema_doc)
    metadata = etree.fromstring(iso_metadata(None, {"id": package_id}))
    schema.assert_(metadata)
    return metadata

def get_xpath(xml, xpath):
    try: ns = xml.nsmap
    except: ns = xml.getroot().nsmap
    return xml.xpath(xpath, namespaces=ns)


class ViewsTestCase(NgdsTestCase):

    def validate_some_xpath(self, xml, xpath, expected):
        results = get_xpath(xml, xpath)
        if isinstance(results, list) and len(results) > 0:
            derived_value = results[0]
        elif isinstance(results, list) and len(results) == 0:
            derived_value = ""
        else:
            derived_value = results

        if hasattr(derived_value, "text"):
            derived_value = derived_value.text

        derived_value = derived_value.strip()

        self.assertEqual(derived_value, expected, "Expected: %s || Found: %s at %s" % (expected, derived_value, xpath))

    def test_returns_harvested_data(self):
        pass

    def test_xml_is_schema_valid(self):
        """Test that the XML output is schema valid"""
        self.add_package("schema-valid-test")
        validate("schema-valid-test")

    def test_xml_id(self):
        """Test that XML output contains the proper ID"""
        p = self.add_package("id-test")
        metadata = validate("id-test")
        self.validate_some_xpath(metadata, "//gmd:fileIdentifier/gco:CharacterString", p.get("id", None))

    def test_xml_hierarchy(self):
        """Test that the XML output contains the proper hierarchy value"""
        p = self.add_package("hierarchy-test", {"extras": [{"key": "data_type", "value": "Wonka"}]})
        metadata = validate("hierarchy-test")
        ds = "Wonka"
        self.validate_some_xpath(
            metadata,
            "//gmd:hierarchyLevel/gmd:MD_ScopeCode",
            ds
        )

    def test_xml_hierarchy_code_list_value(self):
        """Test that the XML output contains the proper hierarchy code list value"""
        p = self.add_package("hierarchy-code-test", {"extras": [{"key": "data_type", "value": "Wonka"}]})
        metadata = validate("hierarchy-code-test")
        ds = "Wonka"
        self.validate_some_xpath(
            metadata,
            "//gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue",
            ds
        )

    def test_xml_hierarchy_level_name(self):
        """Test that the XML output contains the proper hierarchy level name"""
        p = self.add_package("hierarchy-level-test", {"extras": [{"key": "data_type", "value": "Wonka"}]})
        metadata = validate("hierarchy-level-test")
        ds = "Wonka"
        self.validate_some_xpath(
            metadata,
            "//gmd:hierarchyLevelName/gco:CharacterString",
            ds
        )

    def test_xml_maintainer(self):
        """Test that XML output contains the proper maintainer information"""
        name = "mo"
        email = "mo@om.com"
        maintainer = {
            "extras": [
                dict(key="maintainer_name", value=name),
            ],
            "maintainer_email": email
        }
        p = self.add_package("maintainer-test", maintainer)
        metadata = validate("maintainer-test")
        self.validate_some_xpath(
            metadata,
            "//gmd:contact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString",
            name
        )
        self.validate_some_xpath(
            metadata,
            "//gmd:contact//gmd:CI_Contact//gmd:electronicMailAddress/gco:CharacterString",
            email
        )

    def test_xml_mod_date(self):
        """Test that XML output contains the proper modification date"""
        p = self.add_package("mod-date-test")
        metadata = validate("mod-date-test")
        self.validate_some_xpath(
            metadata,
            "//gmd:dateStamp/gco:DateTime",
            date_parser.parse(p.get("metadata_modified", "")).replace(microsecond=0).isoformat()
        )

    def test_xml_set_datasetURI(self):
        """Test that XML output contains the proper dataset uri"""
        p = self.add_package("set-dataset-uri-test", {"extras": [{"key": "other_id", "value": json.dumps(["uri"])}]})
        metadata = validate("set-dataset-uri-test")
        self.validate_some_xpath(metadata, "//gmd:dataSetURI/gco:CharacterString", "uri")

    def test_xml_unset_datasetURI(self):
        p = self.add_package("unset-dataset-uri-test")
        metadata = validate("unset-dataset-uri-test")
        self.validate_some_xpath(
            metadata,
            "//gmd:dataSetURI/gco:CharacterString",
            pylons_config.get("ckan.site_url", "http://default.ngds.com").rstrip("/") + "/dataset/unset-dataset-uri-test"
        )

    def test_xml_unset_pubdate(self):
        p = self.add_package("unset-pub-date", ngds_extras=False)
        metadata = validate("unset-pub-date")
        self.validate_some_xpath(
            metadata,
            "//gmd:citation//gmd:date//gmd:date/gco:DateTime",
            date_parser.parse(p.get("metadata_created", "")).replace(microsecond=0).isoformat()
        )

    def test_xml_title(self):
        """Test that XML output contains the proper title"""
        name = "title-test"
        p = self.add_package(name)
        metadata = validate(name)
        self.validate_some_xpath(metadata, "//gmd:CI_Citation/gmd:title/gco:CharacterString", p.get("title", None))

    def test_xml_creators(self):
        """Test that XML output contains the proper creators"""
        p = self.add_package("authors-test", {
            "extras": [
                {
                    "key": "authors",
                    "value": json.dumps(
                        [
                            {
                                "author_name": "Ryan",
                                "author_email": "nothing@false.com"
                            },
                            {
                                "author_name": "Roger Mebowitz",
                                "author_email": "nothing@waste.com"
                            }
                        ]
                    )
                }
            ]
        })
        metadata = validate("authors-test")
        self.validate_some_xpath(
            metadata,
            "//gmd:citedResponsibleParty[1]//gmd:individualName/gco:CharacterString",
            "Ryan"
        )
        self.validate_some_xpath(
            metadata,
            "//gmd:citedResponsibleParty[1]//gmd:CI_Contact//gmd:electronicMailAddress/gco:CharacterString",
            "nothing@false.com"
        )
        self.validate_some_xpath(
            metadata,
            "//gmd:citedResponsibleParty[2]//gmd:individualName/gco:CharacterString",
            "Roger Mebowitz"
        )
        self.validate_some_xpath(
            metadata,
            "//gmd:citedResponsibleParty[2]//gmd:CI_Contact//gmd:electronicMailAddress/gco:CharacterString",
            "nothing@waste.com"
        )

    def test_xml_notes(self):
        """Test that XML output contains the proper description"""
        name = "description-test"
        p = self.add_package(name)
        metadata = validate(name)
        self.validate_some_xpath(
            metadata,
            "//gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString",
            p.get("notes", None)
        )

    def test_xml_tags(self):
        """Test that XML output contains the proper tags"""
        name = "tags-test"
        expected_tags = ["one", "two", "four"]
        p = self.add_package(name)
        p = self.add_tags(name, expected_tags) # Looses extras!
        metadata = validate(name)
        tags = metadata.xpath("//gmd:keyword/gco:CharacterString", namespaces=metadata.nsmap)
        derived_tags = [tag.text for tag in tags]
        differences_between_package_tags_and_xml_keywords = len(set(expected_tags).difference(derived_tags))
        self.assertEqual(differences_between_package_tags_and_xml_keywords, 0)

    def test_xml_faceted_tags(self):
        """Test that XML output contains the proper faceted tags"""
        name = "facet-test"
        facets = [("Category", "Heatflow"), ("Category=>SubCategory", "Hibbity")]
        p = self.add_package("facet-test")
        p = self.add_facets(name, facets)
        metadata = validate(name)

        xpath = '//gmd:MD_Keywords[gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString="%s"]/gmd:keyword/gco:CharacterString'
        self.validate_some_xpath(metadata, xpath % "Category", "Heatflow")
        self.validate_some_xpath(metadata, xpath % "Category=>SubCategory", "Hibbity")

    def test_xml_language(self):
        """Test that XML output contains the right language"""
        p = self.add_package("language-test", {"extras":[dict(key="language", value="drublic")]})
        metadata = validate("language-test")
        self.validate_some_xpath(metadata, "//gmd:MD_DataIdentification//gmd:language/gco:CharacterString", "drublic")

    def test_xml_extent(self):
        """Test that XML output contains the proper extent info"""
        name = "extent-test"

        polygon = json.dumps({
            "type": "Polygon",
            "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]]
        })

        p = self.add_package(
            name,
            {"extras": [{"key": "spatial", "value": polygon}]}
        )
        metadata = validate(name)
        self.validate_some_xpath(metadata, "//gmd:westBoundLongitude/gco:Decimal", "100.0")
        self.validate_some_xpath(metadata, "//gmd:eastBoundLongitude/gco:Decimal", "101.0")
        self.validate_some_xpath(metadata, "//gmd:northBoundLatitude/gco:Decimal", "1.0")
        self.validate_some_xpath(metadata, "//gmd:southBoundLatitude/gco:Decimal", "0.0")

    def test_xml_distributors(self):
        """Test that XML output contains the proper distributors listed"""
        p = self.add_package("test-distributors")
        dist_one = {"distributor_name": "Roger Mebowitz", "distributor_email": "roger@mebowitz.com"}
        dist_two = {"distributor_name": "Mebow Roginski", "distributor_email": "mebow@roginski.com"}

        resources = [
            dict(
                package_id="test-distributors",
                url="http://google.com",
                distributor=json.dumps(dist_one)
            ),
            dict(
                package_id="test-distributors",
                url="http://this.isnt.real.com/",
                distributor=json.dumps(dist_two)
            )
        ]

        p = self.add_resources("test-distributors", resources)
        metadata = validate("test-distributors")
        result = get_xpath(
                metadata,
                '//gmd:MD_Distribution/gmd:distributor//gmd:individualName[gco:CharacterString="Roger Mebowitz"]'
            )
        self.assertIsNotNone(result)
        self.assertNotEqual(result, [])

        result = get_xpath(
                metadata,
                '//gmd:MD_Distribution/gmd:distributor//gmd:individualName[gco:CharacterString="Mebow Roginski"]'
            )
        self.assertIsNotNone(result)
        self.assertNotEqual(result, [])

    def test_xml_distributor_info(self):
        """Test that XML output contains the proper relationships between distributors and their distributions"""
        name = "test-distributor-trans-opts"
        p = self.add_package(name)
        dist_one = {"distributor_name": "Roger Mebowitz", "distributor_email": "roger@mebowitz.com"}
        dist_two = {"distributor_name": "Mebow Roginski", "distributor_email": "mebow@roginski.com"}

        resources = [
            dict(
                package_id=name,
                url="http://google.com",
                distributor=json.dumps(dist_one)
            ),
            dict(
                package_id=name,
                url="http://this.isnt.real.com/",
                distributor=json.dumps(dist_two)
            )
        ]

        p = self.add_resources(name, resources)
        metadata = validate(name)

        xpath = '//gmd:MD_Distributor[gmd:distributorContact//gmd:individualName/gco:CharacterString="%s"]/gmd:distributorTransferOptions/@xlink:href'

        for res in p.get("resources", []):
            dist = json.loads(res.get("distributor", {})).get("distributor_name")
            self.validate_some_xpath(metadata, xpath % dist, "#distribution-%s" % res.get("id", ""))

    def test_xml_transfer_options(self):
        """Test that XML output contains all the proper distributions"""
        name = "test-count-trans-opts"
        p = self.add_package(name)
        dist_one = {"distributor_name": "Roger Mebowitz", "distributor_email": "roger@mebowitz.com"}
        dist_two = {"distributor_name": "Mebow Roginski", "distributor_email": "mebow@roginski.com"}

        resources = [
            dict(
                package_id=name,
                url="http://google.com",
                distributor=json.dumps(dist_one)
            ),
            dict(
                package_id=name,
                url="http://this.isnt.real.com/",
                distributor=json.dumps(dist_two)
            )
        ]

        p = self.add_resources(name, resources)
        metadata = validate(name)

        self.assertEqual(len(get_xpath(metadata, "//gmd:transferOptions")), 2)

    def test_xml_offline_resource_dist_name(self):
        """Test that attributes are correctly assigned in offline resources"""
        name = "offline-name-test"
        p = self.add_package(name)
        dist = dict(
            package_id=name,
            url="http://nothing.com/",
            distributor=json.dumps(dict(distributor_name="Roger Mebowitz", distributor_email="roger@mebowitz.com")),
            is_online="false",
            description="description",
            ordering="ordering",
            resource_type="resource_type"
        )
        p = self.add_resource(name, dist)
        metadata = validate(name)
        self.validate_some_xpath(metadata, "//gmd:MD_Distributor//gmd:individualName/gco:CharacterString", "Roger Mebowitz")

    def test_xml_offline_resource_dist_email(self):
        """Test that attributes are correctly assigned in offline resources"""
        name = "offline-email-test"
        p = self.add_package(name)
        dist = dict(
            package_id=name,
            url="http://nothing.com/",
            distributor=json.dumps(dict(distributor_name="Roger Mebowitz", distributor_email="roger@mebowitz.com")),
            is_online="false",
            description="description",
            ordering="ordering",
            resource_type="resource_type"
        )
        p = self.add_resource(name, dist)
        metadata = validate(name)
        self.validate_some_xpath(
            metadata,
            "//gmd:MD_Distributor//gmd:CI_Contact//gmd:electronicMailAddress/gco:CharacterString",
            "roger@mebowitz.com"
        )

    def test_xml_offline_resource_ordering(self):
        """Test that attributes are correctly assigned in offline resources"""
        name = "offline-ordering-test"
        p = self.add_package(name)
        dist = dict(
            package_id=name,
            url="http://nothing.com/",
            distributor=json.dumps(dict(distributor_name="Roger Mebowitz", distributor_email="roger@mebowitz.com")),
            is_online="false",
            description="description",
            ordering="ordering",
            resource_type="resource_type"
        )
        p = self.add_resource(name, dist)
        metadata = validate(name)
        self.validate_some_xpath(
            metadata,
            "//gmd:MD_Distributor//gmd:orderingInstructions/gco:CharacterString",
            "ordering"
        )

    def test_xml_offline_resource_type(self):
        """Test that attributes are correctly assigned in offline resources"""
        name = "offline-resource-test"
        p = self.add_package(name)
        dist = dict(
            package_id=name,
            url="http://nothing.com/",
            distributor=json.dumps(dict(distributor_name="Roger Mebowitz", distributor_email="roger@mebowitz.com")),
            is_online="false",
            description="description",
            ordering="ordering",
            resource_type="resource_type"
        )
        p = self.add_resource(name, dist)
        metadata = validate(name)
        self.validate_some_xpath(
            metadata,
            "//gmd:MD_Distributor//gmd:MD_Format//gmd:name/gco:CharacterString",
            "resource_type"
        )

    def test_xml_offline_resource_link(self):
        """Test that attributes are correctly assigned in offline resources"""
        name = "offline-link-test"
        p = self.add_package(name)
        dist = dict(
            package_id=name,
            url="http://nothing.com/",
            distributor=json.dumps(dict(distributor_name="Roger Mebowitz", distributor_email="roger@mebowitz.com")),
            is_online="false",
            name="name",
            description="description",
            ordering="ordering",
            resource_type="resource_type"
        )
        p = self.add_resource(name, dist)
        metadata = validate(name)
        res = p["resources"][0]
        self.validate_some_xpath(
            metadata,
            "//gmd:MD_Distributor/gmd:distributorTransferOptions/@xlink:href",
            "#distribution-%s" % res["id"]
        )

    def test_xml_offline_resource_medium(self):
        """Test that attributes are correctly assigned in offline resources"""
        name = "offline-medium-test"
        p = self.add_package(name)
        dist = dict(
            package_id=name,
            url="http://nothing.com/",
            distributor=json.dumps(dict(distributor_name="Roger Mebowitz", distributor_email="roger@mebowitz.com")),
            is_online="false",
            name="name",
            description="description",
            ordering="ordering",
            resource_type="resource_type"
        )
        p = self.add_resource(name, dist)
        metadata = validate(name)
        res_id = "distribution-%s" % p["resources"][0]["id"]
        self.validate_some_xpath(
            metadata,
            '//gmd:MD_DigitalTransferOptions[@id="%s"]/gmd:offLine//gmd:mediumNote/gco:CharacterString' % res_id,
            "%s -- %s" % (p["resources"][0]["name"], p["resources"][0]["description"])
        )

    def test_xml_online_url(self):
        """Test that attributes are correctly assigned in online resources"""
        name = "online-url-test"
        p = self.add_package(name)
        dist = dict(
            package_id=name,
            url="http://nothing.com/",
            distributor=json.dumps(dict(distributor_name="Roger Mebowitz", distributor_email="roger@mebowitz.com")),
            is_online="true",
            name="name",
            description="description",
            protocol="OGC:WMS",
            layer_name="habbi"
        )
        p = self.add_resource(name, dist)
        metadata = validate(name)
        res_id = "distribution-%s" % p["resources"][0]["id"]
        self.validate_some_xpath(
            metadata,
            '//gmd:MD_DigitalTransferOptions[@id="%s"]//gmd:linkage/gmd:URL' % res_id,
            "http://nothing.com/"
        )

    def test_xml_online_protocol(self):
        """Test that attributes are correctly assigned in online resources"""
        name = "online-protocol-test"
        p = self.add_package(name)
        dist = dict(
            package_id=name,
            url="http://nothing.com/",
            distributor=json.dumps(dict(distributor_name="Roger Mebowitz", distributor_email="roger@mebowitz.com")),
            is_online="true",
            name="name",
            description="description",
            protocol="OGC:WMS",
            layer_name="habbi"
        )
        p = self.add_resource(name, dist)
        metadata = validate(name)
        res_id = "distribution-%s" % p["resources"][0]["id"]
        self.validate_some_xpath(
            metadata,
            '//gmd:MD_DigitalTransferOptions[@id="%s"]//gmd:protocol/gco:CharacterString' % res_id,
            "OGC:WMS"
        )

    def test_xml_online_description(self):
        """Test that attributes are correctly assigned in online resources"""
        name = "online-description-test"
        p = self.add_package(name)
        dist = dict(
            package_id=name,
            url="http://nothing.com/",
            distributor=json.dumps(dict(distributor_name="Roger Mebowitz", distributor_email="roger@mebowitz.com")),
            is_online="true",
            name="name",
            description="description",
            protocol="OGC:WMS",
            layer_name="habbi"
        )
        p = self.add_resource(name, dist)
        metadata = validate(name)
        res = p["resources"][0]
        res_id = "distribution-%s" % res["id"]
        ele = get_xpath(metadata, '//gmd:MD_DigitalTransferOptions[@id="%s"]//gmd:description/gco:CharacterString' % res_id)
        self.assertTrue(ele[0].text.strip().startswith(res.get("description", "hambone")))

    def test_xml_online_layer(self):
        """Test that attributes are correctly assigned in online resources"""
        name = "online-layer-test"
        p = self.add_package(name)
        dist = dict(
            package_id=name,
            url="http://nothing.com/",
            distributor=json.dumps(dict(distributor_name="Roger Mebowitz", distributor_email="roger@mebowitz.com")),
            is_online="true",
            name="name",
            description="description",
            protocol="OGC:WMS",
            layer_name="habbi"
        )
        p = self.add_resource(name, dist)
        metadata = validate(name)
        res = p["resources"][0]
        res_id = "distribution-%s" % res["id"]
        ele = get_xpath(metadata, '//gmd:MD_DigitalTransferOptions[@id="%s"]//gmd:description/gco:CharacterString' % res_id)
        self.assertTrue(ele[0].text.strip().endswith(res.get("layer_name", "hambone")))