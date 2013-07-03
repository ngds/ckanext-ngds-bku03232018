from ckanext.ngds.tests.ngds_test_case import NgdsTestCase
from ckanext.ngds.csw.logic.view import iso_metadata
from dateutil import parser as date_parser
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


def validate_some_xpath(xml, xpath, expected):
    try: ns = xml.nsmap
    except: ns = xml.getroot().nsmap
    derived_value = xml.xpath(xpath, namespaces=ns)[0].text
    assert(derived_value == expected)


class ViewsTestCase(NgdsTestCase):

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
        validate_some_xpath(metadata, "//gmd:fileIdentifier/gco:CharacterString", p.get("id", None))

    def test_xml_maintainer(self):
        """Test that XML output contains the proper maintainer information"""
        pass

    def test_xml_mod_date(self):
        """Test that XML output contains the proper modification date"""
        p = self.add_package("mod-date-test")
        metadata = validate("mod-date-test")
        validate_some_xpath(
            metadata,
            "//gmd:dateStamp/gco:DateTime",
            date_parser.parse(p.get("metadata_modified", "")).replace(microsecond=0).isoformat()
        )

    def test_xml_datasetURI(self):
        """Test that XML output contains the proper dataset uri"""
        pass

    def test_xml_title(self):
        """Test that XML output contains the proper title"""
        name = "title-test"
        p = self.add_package(name)
        metadata = validate(name)
        validate_some_xpath(metadata, "//gmd:CI_Citation/gmd:title/gco:CharacterString", p.get("title", None))

    def test_xml_creators(self):
        """Test that XML output contains the proper creators"""
        pass

    def test_xml_notes(self):
        """Test that XML output contains the proper description"""
        name = "description-test"
        p = self.add_package(name)
        metadata = validate(name)
        validate_some_xpath(
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
        pass

    def test_xml_extent(self):
        """Test that XML output contains the proper extent info"""
        name = "extent-test"

        polygon = json.dumps({
            "type": "Polygon",
            "coordinates": [
                [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ]
            ]
        })

        p = self.add_package(
            name,
            {"extras": [{"key": "spatial", "value": polygon}]}
        )
        metadata = validate(name)
        validate_some_xpath(metadata, "//gmd:westBoundLongitude/gco:Decimal", "100.0")
        validate_some_xpath(metadata, "//gmd:eastBoundLongitude/gco:Decimal", "101.0")
        validate_some_xpath(metadata, "//gmd:northBoundLatitude/gco:Decimal", "1.0")
        validate_some_xpath(metadata, "//gmd:southBoundLatitude/gco:Decimal", "0.0")

    def test_xml_distributors(self):
        """Test that XML output contains the proper distributors listed"""
        pass

    def test_xml_distributor_info(self):
        """Test that XML output contains the proper relationships between distributors and their distributions"""
        pass

    def test_xml_transfer_options(self):
        """Test that XML output contains all the proper distributions"""
        pass