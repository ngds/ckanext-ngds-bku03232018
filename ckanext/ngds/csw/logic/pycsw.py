''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

from ckan.plugins import toolkit
from ckanext.ngds.csw.model.csw_records import CswRecord
from dateutil import parser
from shapely.geometry import asShape
import json

def metadata_to_pycsw(context, data_dict):
    """
    Synchronize a record in the pycsw table with CKAN content

    @param context: CKAN environment nonsense
    @param data_dict: Must contain an "id" object pointer to a CKAN package
    @return: CSW request URL for this object
    """
    def format_keywords(package):
        keywords = [ keyword["name"] for keyword in package["tags"] ]
        extent = [e for e in package["extras"] if e["key"] == "extent_keyword"]
        if len(extent) > 0:
            keywords.append(extent[0]["value"])
        return ",".join(keywords)

    def get_extent(package):
        extent = [e["value"] for e in package["extras"] if e["key"] == "spatial"]
        if len(extent) > 0:
            return asShape(json.loads(extent[0])).wkt
        else:
            return None

    def format_links(resources):
        '''Format links for pycsw usage: "name,description,protocol,url[^,,,[^,,,]]"'''
        links = []
        for resource in resources:
            link = "%s," % resource.get("name", "No Name")
            link += "%s," % resource.get("description", "No Description")
            link += "%s," % resource.get("protocol", "No Protocol")
            link += "%s" % resource.get("url", "No URL")
            links.append(link)

        return "^".join(links)

    def format_datetime(datetime_str):
        return parser.parse(datetime_str).replace(microsecond=0).isoformat()

    # Get the package.
    p = toolkit.get_action("package_show")(context, {"id": data_dict.get("id", "")})

    # Check that we got a dataset back
    if p is not None and p.get("type") != "dataset":
        return None

    # Create inputs for a new CswRecord
    kwargs = {
        "package_id": p["id"],
        "identifier": p["id"],
        "typename": "gmd:MD_Metadata",
        "schema": "http://www.isotc211.org/2005/gmd",
        "mdsource": "local",
        "insert_date": format_datetime(p["metadata_modified"]),
        "xml": toolkit.get_action("iso_metadata")(context, {"id": p["id"]}),
        "anytext": "", # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< AnyText
        "language": "eng",
        "type": "", # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Category
        "title": p["title"],
        "abstract": p["notes"],
        "keywords": format_keywords(p),
        "keywordstype": "theme",
        "parentIdentifier": None,
        "relation": "",
        "time_begin": None,
        "time_end": None,
        "topicategory": "", # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Topic
        "resourcelanguage": "eng",
        "creator": "creator", # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Creator
        "publisher": "publisher", # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Publisher
        "contributor": "contributor", # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Contributor
        "organization": None, # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Organization
        "securityconstraints": None,
        "accessconstraints": "", # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< License
        "otherconstraints": None,
        "date": format_datetime(p["metadata_modified"]),
        "date_revision": format_datetime(p["metadata_modified"]),
        "date_creation": format_datetime(p["metadata_created"]),
        "date_publication": "", # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Publication Date
        "date_modified": format_datetime(p["metadata_modified"]),
        "format": None, # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Format
        "source": None,
        "crs": None,
        "geodescode": None,
        "denominator": None,
        "distancevalue": None,
        "distanceuom": None,
        "wkt_geometry": get_extent(p),
        "servicetype": None, # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Service Type
        "servicetypeversion": None,
        "operation": None,
        "couplingtype": None,
        "operateson": None,
        "operatesonidentifier": None,
        "degree": None,
        "conditionapplyingtoaccessanduse": None,
        "lineage": None, # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Lineage
        "responsiblepartyrole": "distributor", # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Wut?
        "specificationtitle": None,
        "specificationdate": None,
        "spcificationdatetype": None,
        "links": format_links(p["resources"])
    }

    # Make a new CswRecord object
    csw = CswRecord(**kwargs)

    # Check if there's already one in there for this one
    csw = context["session"].merge(csw)

    # Update / Add
    context["session"].add(csw)

    # Commit!
    context["session"].commit()

    # Generate a CSW URL and return it
    url = "/csw? \
        request=GetRecordById \
        &id=%s \
        &service=CSW \
        &version=2.0.2 \
        &outputSchema=http://www.isotc211.org/2005/gmd \
        &elementSetName=full"\

    return (url % (p["id"])).replace(" ", "").replace("\n", "")

def full_sync(context, data_dict):
    """
    Full synchronization between CKAN Packages and pycsw. This may take awhile...

    @param context: CKAN environment
    @param data_dict: Can optionally specify "purge": true if you want the whole table purged first. Default is not to
    @return: String message as to whether or not we succeed
    """

    # If requested, purge the whole table
    if data_dict.get("purge", False):
        context["model"].Session.query(CswRecord).delete()

    for pk in toolkit.get_action("package_list")(context, {}):
        metadata_to_pycsw(context, {"id": pk})
