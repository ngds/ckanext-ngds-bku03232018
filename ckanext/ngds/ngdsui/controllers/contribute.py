from ckan.lib.base import *
from ckan.lib.navl.dictization_functions import DataError, unflatten, validate
from ckan.lib.base import (request,
                           render,
                           BaseController,
                           model,
                           abort, h, g, c)
from ckan.logic import get_action
from ckan.logic import (tuplize_dict,
                        clean_dict,
                        parse_params,
                        flatten_to_string_key)

class ContributeController(BaseController):

 	def index(self):
		
		"""
		Renders contribute page.
		"""

		nodes = model.HarvestNode.get_all()

		c.harvested_nodes = nodes
		
		return render('contribute/contribute.html')		

	def harvest(self):
		"""
		Create new Harvest node.
		"""
		
		return render('contribute/harvest_new.html')

	def save(self):
		"""
		Create new Harvest node.
		"""
		data = clean_dict(unflatten(tuplize_dict(parse_params(
            request.params))))

		print "Harvest the data: ",data

		data_dict = {'model':'HarvestNode'}
		data_dict['data']=data
		data_dict['process']='create'
		

		print "Data dict: ",data_dict

		context = {'model': model}

		get_action('ngds_harvest')(context, data_dict)		

		return self.index()

 	def read(self):
		
		"""
		Fetches the details about a particular node.
		"""

		node_id = 2

		node = model.HarvestNode.by_id(node_id)

		c.selected_node = node

		return render('contribute/contribute.html')	