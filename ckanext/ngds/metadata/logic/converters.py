def convert_to_authors(key, data, errors, context):
    extras = data.get(('extras',), [])
    if not extras:
        data[('extras',)] = extras
    extras.append({'key': key[-1], 'value': data[key]})

def convert_to_keywords(key, data, errors, context):
    pass

def convert_to_geo_extent(key, data, errors, context):
    pass

def convert_to_distributors(key, data, errors, context):
    pass

def convert_to_links(key, data, errors, context):
    pass

def convert_to_metadata_contact(key, data, errors, context):
    pass

def convert_to_harvest_info(key, data, errors, context):
    pass