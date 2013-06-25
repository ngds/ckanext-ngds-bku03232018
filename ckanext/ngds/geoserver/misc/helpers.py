from ckanext.ngds.env import ckan_model
def is_spatialized(resource):
    spatialized = False
    resource_id = resource['id']
    package_id=ckan_model.Resource.get(resource_id).resource_group.package_id
    package = ckan_model.Package.get(package_id)
    for resource in package.resources:
        if 'ogc_type' in resource.extras and 'parent_resource' in resource.extras:
            extras = resource.extras
            if extras['parent_resource'] == resource_id\
                and resource.state =='active' and ( extras['ogc_type'].lower() == 'wms' or extras['ogc_type'].lower() == 'wfs'):
                spatialized = True
                break
    return spatialized
