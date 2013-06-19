
def is_spatialized(resource):
    is_spatialized = False
    try:
        if resource.get('layer_name') and resource.get('layer_name') != 'None':
            is_spatialized = True
        print is_spatialized
    except Exception as ex:
        is_spatialized = False
    return is_spatialized