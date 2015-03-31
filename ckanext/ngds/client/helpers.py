from ckanext.ngds.common import config

def ngds_aggregator_url():
    ngds_aggregator_url = config.get('ngds.aggregator_url', 'http://www.geothermaldata.org')
    return ngds_aggregator_url


