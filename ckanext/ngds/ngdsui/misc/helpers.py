from ckan.lib.base import model


def get_responsible_party_name(id):
	"""
	Get the name of a responsible party for an id.
	"""
	
	if(id):
		try:
			name = model.ResponsibleParty.get(id).name
		except(DataError):
			return ""
		return name
	else:
		return ""