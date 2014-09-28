import json
from ckanext.ngds.common import plugins as p


def create_protocol_codes():
    user = p.toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'protocol_codes'}
        p.toolkit.get_action('vocabulary_show')(context, data)
    except p.toolkit.ObjectNotFound:
        data = {'name': 'protocol_codes'}
        vocab = p.toolkit.get_action('vocabulary_create')(context, data)
        for tag in ('OGC:WMS', 'OGC:WFS', 'OGC:WCS', 'OGC:CSW', 'OGC:SOS',
                    'OPeNDAP', 'ESRI', 'other'):
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            p.toolkit.get_action('tag_create')(context, data)

def protocol_codes():
    create_protocol_codes()
    try:
        tag_list = p.toolkit.get_action('tag_list')
        protocol_codes = tag_list(data_dict={'vocabulary_id': 'protocol_codes'})
        return protocol_codes
    except p.toolkit.ObjectNotFound:
        return None

def ngds_package_extras_processor(extras):
    pkg = [extra for extra in extras if extra.get('key') == 'ngds_package'][0]
    md = json.loads(pkg.get('value'))

    authors = []
    for agent in md['citedSourceAgents']:
        agent = agent['relatedAgent']['agentRole']
        author = {
            'Name': agent['individual']['personName'],
            'Position': agent['individual']['personPosition'],
            'Organization': agent['organizationName'],
            'Address': agent['contactAddress'],
            'Phone': agent['phoneNumber'],
            'Email': agent['contactEmail']
        }
        authors.append(author)

    return {
        'citation_date': md['citationDates']['EventDateObject']['dateTime'],
        'authors': authors,
        'geographic_extent': md['geographicExtent'][0],
    }

def ngds_resource_extras_processer(res):
    md = json.loads(res.get('ngds_resource'))
    agent = md['resourceAccessOptions'][0]['distributor']\
        ['relatedAgent']['agentRole']
    distributor = {
        'Name': agent['individual']['personName'],
        'Position': agent['individual']['personPosition'],
        'Organization': agent['organizationName'],
        'Address': agent['contactAddress'],
        'Phone': agent['phoneNumber'],
        'Email': agent['contactEmail']
    }

    return {
        'distributor': distributor,
    }