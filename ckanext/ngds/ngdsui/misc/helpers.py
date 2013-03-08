from ckan.lib.base import model
import ckan.lib.navl.dictization_functions as dictization_functions
DataError = dictization_functions.DataError

def get_responsible_party_name(id):
	"""
	Get the name of a responsible party for an id.
	"""
	# If we don't get an int id, return an empty string.
	if id:
		try:
			id_int = int(id)
		except(ValueError):
			return ""
		responsible_party = model.ResponsibleParty.get(id)
		if responsible_party:
			return responsible_party.name
		else:
			return ""
	else:
		return ""
