from ckanext.spatial.harvesters import CSWHarvester
import json

class NgdsHarvester(CSWHarvester):
    """
    Inherits from ckanext-spatial's CSW Harvester,
        which inherits from ckanext.spatial.harvesters:SpatialHarvester
        which inherits from ckanext.harvest.harvester:HarvesterBase
    """

    def info(self):
        """Return some information about this particular harvester"""
        return {
            'name': 'ngds',
            'title': 'NGDS CSW Server',
            'description': 'CSW Server offering metadata that conforms to the NGDS ISO Profile'
        }

    def get_package_dict(self, iso_values, harvest_object):
        """
        Override's ckanext.spatial.harvesters.SpatialHarvester.get_package_dict

        This function generates the package dictionary from the harvested object. This package_dict
        will be fed to the `package_create` action.
        """

        # First lets generate exactly the same package dict that the reqular harvester would.
        package_dict = super(NgdsHarvester, self).get_package_dict(iso_values, harvest_object)

        # Then lets customize the package_dict further
        extras = package_dict['extras']

        # Published or unpublished
        package_dict['private'] = False

        # Maintainer
        maintainer = {"key": "maintainer", "value": json.dumps([{"name": "from XML", "email": "from XML"}])}
        extras.append(maintainer)

        # Any otherID
        other_id = {"key": "other_id", "value": "from XML"}
        extras.append(other_id)

        # The data type
        data_type = {"key": "data_type", "value": "from XML"}
        extras.append(data_type)

        # Pub date
        publication_date = {"key": "publication_date", "value": "from XML"}
        extras.append(publication_date)

        # Authors
        authors = {"key": "authors", "value": json.dumps([{"name": "from XML", "email": "from XML"}])}
        extras.append(authors)

        # Quality
        quality = {"key": "quality", "value": "from XML"}
        extras.append(quality)

        # Lineage
        lineage = {"key": "lineage", "value": "from XML"}
        extras.append(lineage)

        # Status
        status = {"key": "status", "value": "from XML"}
        extras.append(status)

        # Facets
        # Need info on how these should look

        # Resources
        for res in package_dict.get('resources',[]):
            res['protocol'] = res.get('resource_locator_protocol', '')

            format = res.get('format')
            if format == 'wfs':
                res['protocol'] = 'OGC:WFS'
            elif format == 'wms':
                res['protocol'] = 'OGC:WMS'
            elif format == 'arcgis_rest':
                res['protocol'] = 'ESRI'

            res['layer'] = "get this from XML"

        # When finished, be sure to return the dict
        return package_dict

